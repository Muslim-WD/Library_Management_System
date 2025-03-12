from django.contrib import admin
from .models import Book, BorrowedBook

class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'approved', 'returned', 'borrowed_at')
    list_filter = ('approved', 'returned')
    search_fields = ('user__username', 'book__title')

admin.site.register(Book)
admin.site.register(BorrowedBook, BorrowedBookAdmin)
