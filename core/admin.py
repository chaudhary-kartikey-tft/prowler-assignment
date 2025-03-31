from django.contrib import admin

from .models import Check, Finding, Scan


@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'started_at', 'ended_at')
    list_filter = ('status', 'started_at', 'ended_at')
    search_fields = ('id',)
    ordering = ('-started_at',)


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'scan', 'created_time')
    list_filter = ('created_time',)
    search_fields = ('uid', 'title', 'scan__id')
    ordering = ('-scan__started_at', '-created_time',)


@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'severity', 'status', 'status_code', 'parent_check', 'created_time')
    list_filter = ('severity', 'status', 'created_time')
    search_fields = ('uid', 'parent_check__uid')
    ordering = ('-parent_check__scan__started_at', '-parent_check__created_time', '-created_time',)
