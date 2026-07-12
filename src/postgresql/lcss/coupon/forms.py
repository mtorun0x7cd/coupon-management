from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Coupon, Comment, Hashtag


# Form to create a new User
class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


# Form to login a User
class getUserForm(forms.ModelForm):
    class Meta:
        password = forms.CharField(widget=forms.PasswordInput)
        model = User
        widgets = {
            "password": forms.PasswordInput(),
        }
        fields = [
            "username",
            "password",
        ]


class createCouponForm(forms.ModelForm):
    hashtags = forms.CharField(required=False)

    class Meta:
        model = Coupon
        widgets = {
            "expiring_date": forms.DateInput(attrs={"type": "date"}),
        }
        fields = [
            "name",
            "expiring_date",
            "discount_amt",
            "hashtags",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        hashtag_names = self.cleaned_data.get("hashtags", "").split(",")
        hashtags = []
        for name in hashtag_names:
            hashtag, created = Hashtag.objects.get_or_create(
                name="#" + name.strip().replace(" ", "")
            )
            if created:
                print("Created new hashtag: ", hashtag)
            else:
                print("Found existing hashtag: ", hashtag)
            hashtags.append(hashtag)
        if hashtags:
            instance.save()
            instance.hashtags.set(hashtags)
        else:
            instance.save()
        return instance


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))

    class Meta:
        model = Comment
        fields = ("text",)


class CouponSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False)
