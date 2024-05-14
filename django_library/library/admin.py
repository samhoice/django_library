from django.contrib import admin

from library.models import Book, Author, Reader

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Reader)