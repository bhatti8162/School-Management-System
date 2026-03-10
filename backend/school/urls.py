from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminViewSet,
    StudentViewSet,
    AttendanceViewSet,
    ResultViewSet,
    FeeViewSet,
    StudentSummaryViewSet
)

router = DefaultRouter()
router.register(r'admins', AdminViewSet)
router.register(r'students', StudentViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'results', ResultViewSet)
router.register(r'fees', FeeViewSet)
router.register(r'summary', StudentSummaryViewSet, basename='student-summary')

urlpatterns = [
    path('', include(router.urls)),
]