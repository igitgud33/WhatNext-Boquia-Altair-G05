from django.shortcuts import render
from .models import MediaItem

# Create your views here.
def media_list(request):
    media_items = MediaItem.objects.select_related("media_type").all()

    return render(request, "catalog/media_list.html", {
        "media_items": media_items
    })
