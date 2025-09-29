from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Write your review..."}),
        }

from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

# For default User model fields (username, email)
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

# For extra profile fields (phone, address)
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone", "address"]
