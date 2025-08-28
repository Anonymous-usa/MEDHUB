# statistics/urls.py
from django.urls import path
from .views import OverviewStatsView, InstitutionStatsView

app_name = "statistics"

urlpatterns = [
    # 📊 Общая статистика по системе (только для супер‑админа)
    path(
        "v1/stats/overview/",
        OverviewStatsView.as_view(),
        name="stats-overview"
    ),

    # 🏥 Статистика по конкретному учреждению
    path(
        "v1/stats/institution/<int:pk>/",
        InstitutionStatsView.as_view(),
        name="stats-institution"
    ),
]
