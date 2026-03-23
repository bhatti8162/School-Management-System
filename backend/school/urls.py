from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SchoolViewSet,
    StudentViewSet,
    AttendanceViewSet,
    ResultViewSet,
    ParentGuardianViewSet,
    FeeViewSet,
    StudentSummaryViewSet,
    UniversalSearchViewSet,
)

router = DefaultRouter()
router.register(r'school', SchoolViewSet, basename='school')
router.register(r'family', ParentGuardianViewSet, basename='family')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'attendance', AttendanceViewSet)
router.register(r'results', ResultViewSet)
router.register(r'fees', FeeViewSet)
router.register(r'summary', StudentSummaryViewSet, basename='student-summary')
router.register(r'search', UniversalSearchViewSet, basename='universal-search')

urlpatterns = [
    path('', include(router.urls)),
]