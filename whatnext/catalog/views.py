from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MediaItem, UserMedia
from .forms import MediaItemForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST


# checks user role on media management
def can_manage_media(user, media):
    return user.role == "ADMIN" or media.created_by_id == user.id


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

    return render(request, "catalog/admin/add_media.html", {
        "form": form
    })

# edit media view
@login_required
def edit_media(request, media_id):
    media = get_object_or_404(MediaItem, id=media_id)

    if not can_manage_media(request.user, media):
        messages.error(request, "You do not have permission to edit this media.")
        return redirect("catalog:media_list")

    if request.method == "POST":
        form = MediaItemForm(request.POST, request.FILES, instance=media)

        if form.is_valid():
            form.save()
            messages.success(request, "Media successfully updated!")
            return redirect("catalog:media_list")
    else:
        form = MediaItemForm(instance=media)
    
    return render(request, "catalog/admin/edit_media.html", {
        "form": form,
        "media": media
    })

# delete media view
@login_required
def delete_media(request, media_id):
    media = get_object_or_404(MediaItem, id=media_id)

    if not can_manage_media(request.user, media):
        messages.error(request, "You do not have permission to delete this media.")
        return redirect("catalog:media_list")
    
    if request.method == "POST":
        media.delete()
        messages.success(request, "Media successfully deleted!")
        return redirect("catalog:media_list")

    return render(request, "catalog/admin/delete_media.html", {
        "media":media,
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


# edit user media
@login_required
def edit_user_media(request, entry_id):
    
    # ensures users only edit their own entries
    entry = get_object_or_404(UserMedia, id=entry_id, user=request.user)

    if request.method == "POST":
        # saving won't change shared catalog item
        form = UserMediaForm(request.POST, instance=entry)

        if form.is_valid():
            form.save()
            messages.success(request, "Your personal input has been updated")
            return redirect("catalog:my_backlog")
    
    else:
        # existing ratings & reviews appear when reopening form
        form = UserMediaForm(instance=entry)

    return render(request, "catalog/user/edit_user_media.html", {
        "form": form,
        "entry": entry
    })
