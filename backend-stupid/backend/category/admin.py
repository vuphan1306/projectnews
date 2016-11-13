"""Modifying admin page."""
from django.contrib import admin
from .models import Category

admin.site.register(Category)
