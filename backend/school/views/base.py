from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, serializers

from django.http import HttpResponse
from django.apps import apps
from django.db.models import Q
from datetime import date

from ..permissions import IsSuperAdminOrAssignedSchoolUser