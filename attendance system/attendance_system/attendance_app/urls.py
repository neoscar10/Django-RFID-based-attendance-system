from django.urls import path
from .views import RegisterCardView, AttendanceListView, attendance_list_view, login_view

urlpatterns = [
    path('api/register-card/', RegisterCardView.as_view(), name='register-card'),
    path('api/attendance-list/', AttendanceListView.as_view(), name='attendance-list'),
    path('', login_view, name='login'),
    path('attendance/', attendance_list_view, name='attendance')

]
