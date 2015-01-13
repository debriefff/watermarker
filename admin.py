from django.contrib import admin
from watermarker import models


class WatermarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_position', 'opacity', 'is_active')
    search_fields = ('title',)


admin.site.register(models.Watermark, WatermarkAdmin)
