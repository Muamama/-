
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post, Comment, VoteOption
from .forms import PostForm

def index_view(request):
    popular = Post.objects.order_by('-created_at')[:5]
    return render(request, "index.html", {"popular": popular})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            for text in request.POST.getlist('options[]'):
                if text.strip():
                    VoteOption.objects.create(post=post, text=text.strip())
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, "create_post.html", {"form": form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST' and 'comment' in request.POST:
        Comment.objects.create(post=post, user=request.user, text=request.POST['comment'])
    total_votes = sum(opt.vote_count for opt in post.options.all()) or 1
    return render(request, "post_detail.html", {"post": post, "total": total_votes})

@login_required
def profile_view(request):
    favorites = Post.objects.filter(author=request.user)[:3]
    history = Post.objects.order_by('-created_at')[:5]
    return render(request, "profile.html", {"favorites": favorites, "history": history})

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login_view')
    return render(request, "register.html", {"form": form})

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('index')
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login_view')
