from django.db import models
from django.contrib.auth.models import User


class Hashtag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name.startswith("#"):
            self.name = f"#{self.name}"
        super().save(*args, **kwargs)


class Coupon(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, unique=False, blank=True
    )
    name = models.CharField(max_length=32)
    expiring_date = models.DateTimeField(null=True, blank=True)
    discount_amt = models.FloatField(default=0.0)
    score = models.IntegerField(default=0)
    code = models.CharField(max_length=32, blank=False, null=False, default="Coupon")
    comments_amt = models.IntegerField(default=0)
    hashtags = models.ManyToManyField(Hashtag)

    def __str__(self):
        return "%s - %s" % (self.user, self.id)


class Comment(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, unique=False, blank=True
    )
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
