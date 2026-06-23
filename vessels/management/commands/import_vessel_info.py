import csv
import time
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from vessels.models import VesselInfo
from vessels.services.docked_client import DockedAPIError
from vessels.services.sync import sync_vessel_info


class Command(BaseCommand):
    help = "Import vessel info from a CSV of IMO numbers via Data Docked API"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to CSV file")
        parser.add_argument(
            "--imo-column",
            default="imo",
            help="CSV column name for IMO (default: imo)",
        )
        parser.add_argument(
            "--delay",
            type=float,
            default=4.1,
            help="Seconds between API calls (15/min limit → use ≥4.0)",
        )
        parser.add_argument(
            "--skip-existing",
            action="store_true",
            help="Skip IMOs already in the database",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print IMOs without calling the API",
        )

    def handle(self, *args, **options):
        csv_path = Path(options["csv_path"])
        if not csv_path.exists():
            raise CommandError(f"File not found: {csv_path}")

        imo_column = options["imo_column"]
        delay = options["delay"]
        skip_existing = options["skip_existing"]
        dry_run = options["dry_run"]

        imos = self._read_imos(csv_path, imo_column)
        self.stdout.write(f"Found {len(imos)} unique IMO(s) in {csv_path}")

        if dry_run:
            for imo in imos:
                self.stdout.write(f"  would sync: {imo}")
            return

        created_count = 0
        updated_count = 0
        skipped_count = 0
        failed = []

        for i, imo in enumerate(imos):
            if skip_existing and VesselInfo.objects.filter(imo=imo).exists():
                skipped_count += 1
                self.stdout.write(f"[{i + 1}/{len(imos)}] skip existing: {imo}")
                continue

            try:
                vessel, created, _ = sync_vessel_info(imo)
                if created:
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"[{i + 1}/{len(imos)}] created: {imo} ({vessel.name})"
                        )
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"[{i + 1}/{len(imos)}] updated: {imo} ({vessel.name})"
                        )
                    )
            except DockedAPIError as exc:
                failed.append((imo, str(exc)))
                self.stderr.write(
                    self.style.ERROR(f"[{i + 1}/{len(imos)}] API error for {imo}: {exc}")
                )
            except Exception as exc:
                failed.append((imo, str(exc)))
                self.stderr.write(
                    self.style.ERROR(f"[{i + 1}/{len(imos)}] failed for {imo}: {exc}")
                )

            if i < len(imos) - 1:
                time.sleep(delay)

        self.stdout.write(
            f"\nDone. created={created_count}, updated={updated_count}, "
            f"skipped={skipped_count}, failed={len(failed)}"
        )
        if failed:
            self.stdout.write("Failures:")
            for imo, err in failed:
                self.stdout.write(f"  {imo}: {err}")

    def _read_imos(self, csv_path, imo_column):
        imos = []
        seen = set()

        with csv_path.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames or imo_column not in reader.fieldnames:
                raise CommandError(
                    f"Column '{imo_column}' not found. Available: {reader.fieldnames}"
                )

            for row in reader:
                imo = (row.get(imo_column) or "").strip()
                if not imo or imo in seen:
                    continue
                seen.add(imo)
                imos.append(imo)

        return imos
