from django.urls import path

from vessels import views

urlpatterns = [
    path("vessels/", views.VesselListView.as_view(), name="vessel-list"),
    path(
        "vessels/<str:imo_or_mmsi>/info/",
        views.VesselInfoView.as_view(),
        name="vessel-info",
    ),
    path(
        "vessels/<str:imo_or_mmsi>/track/",
        views.VesselTrackView.as_view(),
        name="vessel-track",
    ),
    path(
        "vessels/<str:imo_or_mmsi>/weather/",
        views.VesselWeatherView.as_view(),
        name="vessel-weather",
    ),
    path(
        "vessels/<str:imo_or_mmsi>/sync/",
        views.VesselSyncAllView.as_view(),
        name="vessel-sync-all",
    ),
]
