from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Like
from django.http import JsonResponse
import json


from .models import User


def index(request):
    posts = Post.objects.order_by('-timestamp').all()
    return render(request, "network/index.html", {'posts': posts, 'header': 'All Posts'})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            post = Post.objects.create(user=request.user, content=content)
            post.save()
            return redirect('index')
    return redirect('index')


def profile(request, username):
    # Get the User object for the given username, or return a 404 error if not found
    user = get_object_or_404(User, username=username)

    # Get the number of followers for the user
    num_followers = user.followers.count()

    # Get the number of people that the user follows
    num_following = user.following.count()

    # Get all the posts for the user, in reverse chronological order
    posts = user.posts.order_by('-timestamp').all()

    # Render the profile template with the user's information and posts
    return render(request, 'network/profile.html', {
        'viewed_user': user,
        'num_followers': num_followers,
        'num_following': num_following,
        'posts': posts,
    })


@csrf_exempt
@login_required
def follow(request, username):
    """
    View for following a user.
    """
    user = get_object_or_404(User, username=username)
    if request.user != user:
        request.user.following.add(user)
        num_followers = user.followers.count()
        return JsonResponse({'status': 'ok', 'num_followers': num_followers}, status=201)
    return JsonResponse({'status': 'error', 'error_message': 'Cannot follow yourself.'}, status=401)


@csrf_exempt
@login_required
def unfollow(request, username):
    """
    View for unfollowing a user.
    """
    user = get_object_or_404(User, username=username)
    if request.user != user:
        request.user.following.remove(user)
        num_followers = user.followers.count()
        return JsonResponse({'status': 'ok', 'num_followers': num_followers}, status=201)
    return JsonResponse({'status': 'error', 'error_message': 'Cannot unfollow yourself.'}, status=401)


@login_required
def following(request):
    # Get all posts made by users that the current user follows
    following = request.user.following.all()
    posts = Post.objects.filter(user__in=following).order_by('-timestamp')

    # Render the template for the following page with the posts and user information
    return render(request, "network/index.html", {
        "posts": posts,
        'header': 'Posts from People You Follow'
    })

@csrf_exempt
@login_required
def like_post(request):
    print(request.method)
    if request.method == 'POST':
        body = json.loads(request.body)
        post_id = body['post_id']
        post = Post.objects.get(id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
        num_likes = post.likes.count()
        return JsonResponse({'num_likes': num_likes}, status=201)
@csrf_exempt
@login_required
def unlike_post(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        post_id = body['post_id']
        post = Post.objects.get(id=post_id)
        like = Like.objects.filter(user=request.user, post=post)
        if like.exists():
            like.delete()
        num_likes = post.likes.count()
        return JsonResponse({'num_likes': num_likes}, status=201)


def edit_post(request, post_id):
    pass