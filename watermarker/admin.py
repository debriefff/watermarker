from django.contrib import admin

from watermarker import models


class WatermarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_position', 'opacity', 'is_active')
    search_fields = ('title',)
    fieldsets = (
        (None, {'fields': ('title', 'mark', 'opacity', 'position', ('x', 'y'), 'is_active', 'update_hard'),
                'classes': ('wide',)}),
    )


admin.site.register(models.Watermark, WatermarkAdmin)
