from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MediaItem
from .forms import MediaItemForm

# Create your views here.
def media_list(request):
    media_items = MediaItem.objects.select_related("media_type").all()

    return render(request, "catalog/media_list.html", {
        "media_items": media_items
    })

def add_media(request):
    if request.method == "POST":
        form = MediaItemForm(request.POST, request.FILES)

        if form.is_valid():
            media = form.save(commit=False)
            media.created_by = request.user
            media.save()

            messages.success(request, "Media successfully added!")
            return redirect("catalog:media_list")

    else:
        form = MediaItemForm()

    return render(request, "catalog/add_media.html", {
        "form": form
    })