from django.urls import path
from .views import upload_file, success, get_stats

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('success/', success, name='success'),
    path('get_stats/<int:id>/', get_stats, name='get_stats_view_specific'),
]