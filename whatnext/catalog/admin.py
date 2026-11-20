from django.contrib import admin
from .models import MediaType, MediaItem, UserMedia

# Register your models here.
admin.site.register(MediaType)
admin.site.register(MediaItem)
admin.site.register(UserMedia)
