from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from board.models import Category
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
        category = Category.objects.get(name=category_name)
        context_dict['category_name'] = category.name

        posts = Post.objects.filter(category=category)

        context_dict['posts'] = posts
        context_dict['category'] = category

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
            print(userform.errors, profile_form.errors)
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
    try:
        category = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        category = None

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            if category:
                post = form.save(commit=False)
                post.category = category
                post.save()
                return category(request, category_name)
        else:
            print(form.errors)
    else:
        form = PostForm()

    context_dict = {'form': form, 'category': category}

    return render(request, 'donkey/add_page.html', context_dict)

