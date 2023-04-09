from django.contrib import admin

from users.models import User
from .models import Category, Comment, Rating, Review, Title

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Title)
