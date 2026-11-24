from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MediaItem, UserMedia
from .forms import MediaItemForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST


# Create your views here.
def media_list(request):
    media_items = MediaItem.objects.select_related("media_type").all()

    return render(request, "catalog/media_list.html", {
        "media_items": media_items
    })

@login_required
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

# add to backlog message
@login_required
@require_POST

def add_to_backlog(request, media_id):
    media = get_object_or_404(MediaItem, id=media_id)

    entry, created = UserMedia.objects.get_or_create(
        user = request.user,
        media = media
    )

    if created:
        messages.success(request, "Added to your backlog!")
    else:
        messages.info(request, "This item already exists in your backlog.")

    return redirect("catalog:media_list")

# backlog page
@login_required
def my_backlog(request):
    backlog_items = UserMedia.objects.filter(user=request.user).select_related("media", "media__media_type")

    return render(request, "catalog/my_backlog.html", {
        "backlog_items": backlog_items,
        "status_choices": UserMedia.Status.choices
    })

# update status
@login_required
@require_POST

def update_backlog_status(request, entry_id):
    entry = get_object_or_404(
        UserMedia,
        id=entry_id,
        user=request.user
    )

    new_status = request.POST.get("status")

    valid_statuses = UserMedia.Status.values

    if new_status in valid_statuses:
        entry.status = new_status
        entry.save()
        messages.success(request, "Backlog status updated!")
    else:
        messages.error(request, "Invalid status selected.")

    return redirect("catalog:my_backlog")

# remove from backlog (deletes only user's UserMedia entry)
@login_required
@require_POST
def remove_from_backlog(request, entry_id):
    entry = get_object_or_404(
        UserMedia,
        id=entry_id,
        user=request.user
    )

    entry.delete()
    messages.success(request, "Media removed from your backlog.")

    return redirect("catalog:my_backlog")