from django.contrib import admin
from .models import MovieList, song , video, userprofile

admin.site.register(MovieList)
admin.site.register(song)
admin.site.register(video)
admin.site.register(userprofile)
