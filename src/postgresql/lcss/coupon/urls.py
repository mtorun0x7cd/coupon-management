from django.urls import path
from django.urls import re_path as url
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.loginUser, name="login"),
    path("profile/", views.profile, name="profile"),
    path("changepassword/", views.changepassword, name="changepassword"),
    path("create/", views.create, name="create-thread"),
    path("coupons/<int:coupon_id>/", views.detail, name="detail-thread"),
    path("logout/", views.logoutUser, name="logout"),
    path("add_comment/<int:coupon_id>/", views.add_comment, name="add_comment"),
    path(
        "coupons/<int:coupon_id>/comments/all/", views.all_comments, name="all_comments"
    ),
    path(
        "coupon_by_hashtag/<str:hashtag_name>/",
        views.coupon_by_hashtag,
        name="coupon_by_hashtag",
    ),
    path("search_coupons/", views.search_coupons, name="search_coupons"),
    url(r"^upvote/(?P<id>\d+)/$", views.upvote, name="upvote"),
    url(r"^downvote/(?P<id>\d+)/$", views.downvote, name="downvote"),
    url(r"^delete/(?P<id>\d+)/$", views.delete, name="delete"),
]
