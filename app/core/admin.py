from django.contrib import admin
from .models import Book, Log


class BookAdmin(admin.ModelAdmin):
    search_fields = ['name', 'barcode']
    list_display = ('barcode', 'name', 'is_reserved', 'is_deleted', 'return_date', 'created_at', 'updated_at')

admin.site.register(Book, BookAdmin)
admin.site.register(Log)
