from django import forms
from .models import MediaItem, UserMedia

# shared catalog info
class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = ['media_type', 'title', 'description', 'release_date', 'cover_image']
        widgets = {
            "release_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

# user's personal rating, review, & notes
class UserMediaForm(forms.ModelForm):
    class Meta:
        model = UserMedia
        
        # ensures user only access these fields
        fields = ['rating', 'review', 'notes']
        widgets = {
            "ratings": forms.Select(
                choices=[
                    ("", "Select a rating"),
                    (1, "1 Star"),
                    (2, "2 Stars"),
                    (3, "3 Stars"),
                    (4, "4 Stars"),
                    (5, "5 Stars"),
                ]
            ),
            "review": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Write your review..."
            }),
            "notes": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Add your personal notes..."

            })
        }