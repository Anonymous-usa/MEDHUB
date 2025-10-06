from django.urls import path, include
from .views import OverviewStatsView, InstitutionStatsView

app_name = "statistics"

stats_patterns = [
    # 📊 Общая статистика по системе (только для супер‑админа)
    path("overview/", OverviewStatsView.as_view(), name="stats-overview"),

    # 🏥 Статистика по конкретному учреждению
    path("institution/<int:pk>/", InstitutionStatsView.as_view(), name="stats-institution"),

]

urlpatterns = [
    path("v1/stats/", include((stats_patterns, app_name))),
]
