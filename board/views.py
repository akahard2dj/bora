from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from board.models import Category, UserProfile
from board.models import Post
from board.forms import PostForm
from board.forms import UserForm, UserProfileForm


def index(request):
    category_list = Category.objects.all()[:5]
    context_dict = {'categories': category_list}

    return render(request, 'donkey/index.html', context_dict)


def about(request):
    return HttpResponse("BORA Donkey")


@login_required
def category(request, category_name):
    context_dict = {}

    try:
        cat = Category.objects.get(name=category_name)
        context_dict['category_name'] = cat.name

        posts = Post.objects.filter(category=cat)

        context_dict['posts'] = posts
        context_dict['category'] = cat

    except Category.DoesNotExist:
        pass

    return render(request, 'donkey/category.html', context_dict)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'donkey/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/donkey/')
            else:
                return HttpResponse("Your Donkey account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, "donkey/login.html", {})


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/donkey/')


def add_post(request, category_name):
    current_user = UserProfile.objects.get(user=request.user)

    try:
        cat = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            if cat:
                post = form.save(commit=False)
                post.category = cat
                post.user = current_user
                post.save()
                return HttpResponseRedirect('/donkey/category/{}/'.format(cat))
        else:
            print(form.errors)
    else:
        form = PostForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'donkey/add_post.html', context_dict)


@login_required
def post_detail(request, category_name, pk):
    try:
        cat = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        cat = None

    post = get_object_or_404(Post, pk=pk)
    if post.category == cat:
        views = post.views
        post.views = views + 1
        post.save()
        return render(request, 'donkey/post_detail.html', {'post': post, 'category': cat})
    else:
        return HttpResponse('Invalid PK')


@login_required
def post_delete(request, category_name, pk):
    try:
        cat = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        cat = None

    post = get_object_or_404(Post, pk=pk)
    if post.category == cat:
        post.delete()
        return redirect('category', category_name=cat.name)
    else:
        return HttpResponse('Invalid PK')


@login_required
def post_edit(request, category_name, pk):
    current_user = UserProfile.objects.get(user=request.user)
    current_post = Post.objects.get(id=pk)

    try:
        cat = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            if cat:
                post = form.save(commit=False)
                current_post.title = post.title
                current_post.content = post.content
                current_post.save()
                return HttpResponseRedirect('/donkey/category/{}/'.format(cat))
        else:
            print(form.errors)
    else:
        form = PostForm()

    context_dict = {'form': form, 'category': cat, 'post': current_post}

    return render(request, 'donkey/edit_post.html', context_dict)

'''
current_user = UserProfile.objects.get(user=request.user)

    try:
        cat = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            if cat:
                post = form.save(commit=False)
                post.category = cat
                post.user = current_user
                post.save()
                return HttpResponseRedirect('/donkey/category/{}/'.format(cat))
        else:
            print(form.errors)
    else:
        form = PostForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'donkey/add_post.html', context_dict)
'''