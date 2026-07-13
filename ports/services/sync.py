from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from ports.models import PortCallCache
from vessels.services.docked_client import DockedClient
from django.conf import settings

CACHE_TTL = timedelta(days=2)


def _is_cache_fresh(cache_row)->bool:
    """Check if the cache is fresh."""
    if settings.DEBUG:
        print("DEBUG mode: cache is fresh")
        return True
    now = timezone.now()
    return (now - cache_row.created_at < CACHE_TTL) or (
        now - cache_row.updated_at < CACHE_TTL
    )


def _extract_detail(response)->dict:
    if isinstance(response, dict) and "detail" in response:
        return response["detail"]
    return response or {}


def _merge_section(merged, section_key, section_data):
    if not isinstance(section_data, dict) or "list" not in section_data:
        return

    if section_key not in merged:
        merged[section_key] = {
            "total": section_data.get("total"),
            "pages": section_data.get("pages", 1),
            "list": list(section_data.get("list", [])),
        }
        return

    merged[section_key]["list"].extend(section_data.get("list", []))


def _fetch_all_pages(port_call, search_type, vessel_type, client):
    merged = {}
    first_response = client.get_port_calls_by_port(
        port_call,
        offset=0,
        search_type=search_type or None,
        vessel_type=vessel_type or None,
    )
    detail = _extract_detail(first_response)

    for section_key, section_data in detail.items():
        _merge_section(merged, section_key, section_data)

    max_pages = 1
    for section_data in merged.values():
        max_pages = 1 #max(max_pages, section_data.get("pages") or 1) correct this page count

    for offset in range(1, max_pages):
        page_response = client.get_port_calls_by_port(
            port_call,
            offset=offset,
            search_type=search_type or None,
            vessel_type=vessel_type or None,
        )
        page_detail = _extract_detail(page_response)
        for section_key, section_data in page_detail.items():
            _merge_section(merged, section_key, section_data)

    return merged


def get_port_calls_by_port(
    port_call,
    search_type="",
    vessel_type="",
    force=False,
    client=None,
):
    """
    Return port call data for a port, using DB cache when fresh (< 2 days).

    Returns (cache_row, from_cache) where from_cache is True when served
    from the database without calling the Data Docked API.
    """
    cache_row = PortCallCache.objects.filter(
        port_unlocode=port_call,
        search_type=search_type,
        vessel_type=vessel_type,
    ).first()

    if cache_row and not force and _is_cache_fresh(cache_row):
        return cache_row, True

    client = client or DockedClient()
    data = _fetch_all_pages(port_call, search_type, vessel_type, client)

    with transaction.atomic():
        cache_row, _ = PortCallCache.objects.update_or_create(
            port_unlocode=port_call,
            search_type=search_type,
            vessel_type=vessel_type,
            defaults={"data": data},
        )

    return cache_row, False
