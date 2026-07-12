from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect, render
from random import randint
from .forms import (
    createCouponForm,
    createUserForm,
    getUserForm,
    CommentForm,
    CouponSearchForm,
)
from .models import Coupon, Comment, Hashtag


# Form for the signup of a new user
def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
        # return redirect("loggedin")
    else:
        form = createUserForm()
        if request.method == "POST":
            form = createUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                messages.success(request, "Account created for " + user)
                return redirect("login")

    return render(request, "signup.html", {"form": form})


# Form for the login of a user
def loginUser(request):
    form = getUserForm()
    if request.user.is_authenticated:
        return redirect("home")
        # return redirect("loggedin")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, password=password, username=username)

            if user is not None:
                login(request, user)
                return redirect("home")
                # return redirect("loggedin")
            else:
                messages.info(request, "Username or Password is incorrect")

    return render(request, "login.html", {"form": form})


# Form for the profile of the logged in user
@login_required(login_url="login")
def profile(request):
    if request.method == "GET":
        user_coupons = Coupon.objects.filter(user=request.user)
        context_dict = {}
        saving_list = []
        for e in user_coupons:
            saving_list.append(e)

        context_dict["result"] = saving_list

    return render(request, "profile.html", context_dict)


# Form for the home view
def home(request):
    coupons = Coupon.objects.all()
    for coupon in coupons:
        comments = Comment.objects.filter(coupon=coupon)
        coupon.comments_amt = comments.count()
        coupon.save()
    return render(
        request,
        "home.html",
        {"coupons": coupons},
    )


@login_required(login_url="login")
def create(request):
    if request.method == "POST":
        form = createCouponForm(request.POST)
        if form.is_valid():
            coupon = form.save(commit=False)
            coupon.user = request.user
            coupon.code = coupon.name.replace(" ", "") + str(int(coupon.discount_amt))
            coupon.save()
            return redirect("detail-thread", coupon_id=coupon.pk)
    else:
        form = createCouponForm()
    return render(request, "threadcreate.html", {"form": form})


# Form for the detail view of a thread
@login_required(login_url="login")
def detail(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    comments = Comment.objects.filter(coupon=coupon).order_by("-created_date")
    form = CommentForm()
    context = {"coupon": coupon, "comments": comments, "form": form}
    return render(request, "threaddetail.html", context)


# Form to change password
@login_required(login_url="login")
def changepassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user.request.POST)
        if form.is_valid:
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully")
            return redirect("profile")
    else:
        form = PasswordChangeForm(request.user.request.POST)
    return render(request, "changepassword.html", {"form": form})


# Form to logout user
@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect("home")


# Form to upvote a thread
@login_required(login_url="login")
def upvote(request, id):
    coupon = get_object_or_404(Coupon, pk=id)
    if request.method == "POST":
        coupon.score += 1
        coupon.save()
    return redirect("home")


# Form to downvote a thread
@login_required(login_url="login")
def downvote(request, id):
    coupon = get_object_or_404(Coupon, pk=id)
    if request.method == "POST":
        coupon.score -= 1
        coupon.save()
    return redirect("home")


# Form to logout a user
@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect("home")


# Form to delte a thread
@login_required(login_url="login")
def delete(request, id):
    get_object_or_404(Coupon, pk=id).delete()
    return redirect("profile")


@login_required(login_url="login")
def add_comment(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.coupon = coupon
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment was added successfully.")
            return redirect("detail-thread", coupon.id)
    else:
        form = CommentForm()
    return render(request, "add_comment.html", {"form": form})


@login_required(login_url="login")
def all_comments(request, coupon_id):
    coupon = get_object_or_404(Coupon, pk=coupon_id)
    comments = Comment.objects.filter(coupon=coupon).order_by("-created_date")
    return render(
        request, "all_comments.html", {"coupon": coupon, "comments": comments}
    )


def coupon_by_hashtag(request, hashtag_name):
    coupons = Coupon.objects.filter(hashtags__name=hashtag_name)
    context = {"coupons": coupons, "hashtag_name": hashtag_name}
    return render(request, "coupon_by_hashtag.html", context)


def search_coupons(request):
    form = CouponSearchForm(request.GET)
    if form.is_valid():
        search_query = form.cleaned_data.get("search_query")
        if search_query:
            coupons = Coupon.objects.filter(hashtags__name__icontains=search_query)
        else:
            coupons = Coupon.objects.all()
    else:
        coupons = Coupon.objects.all()
    context = {
        "coupons": coupons,
        "coupon_search_form": CouponSearchForm(),
        "hashtag_name": search_query,
    }
    return render(request, "coupon_by_hashtag.html", context)
