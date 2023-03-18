from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Post
from django.http import JsonResponse


from .models import User


def index(request):
    posts = Post.objects.order_by('-timestamp').all()
    return render(request, "network/index.html", {'posts': posts})


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


@login_required
def follow(request, username):
    """
    View for following a user.
    """
    user = get_object_or_404(User, username=username)
    if request.user != user:
        request.user.following.add(user)
        return redirect(request.META.get('HTTP_REFERER', 'profiles'))
    return JsonResponse({'status': 'error', 'error_message': 'Cannot follow yourself.'})

@login_required
def unfollow(request, username):
    """
    View for unfollowing a user.
    """
    user = get_object_or_404(User, username=username)
    if request.user != user:
        request.user.following.remove(user)
        return redirect(request.META.get('HTTP_REFERER', 'profiles'))
    return JsonResponse({'status': 'error', 'error_message': 'Cannot unfollow yourself.'})