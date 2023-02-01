from django.shortcuts import render, redirect
from .models import Article, Category
from .forms import ArticleForm, LoginForm, RegistrationForm
from django.db.models import Q

from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    categories = Category.objects.all()
    # SELECT * FROM categories;
    # categories = cursor.fetchall()
    articles = Article.objects.all()
    # SELECT * FROM articles;
    # articles = cursor.fetchall()
    context = {
        'title': 'MAIN PAGE',
        'categories': categories,
        'articles': articles.order_by('-created_at')
    }
    # MB so'rov jo'natib, kerakli ma'lumotlarni olib
    # lug'at ma'lumotlar turidagi 'context' nomli o'zgaruvchiga solib
    # index.html saxifasiga ma'lumotlarni joylab
    # foydalunuvchji so'riviga javob
    # sifatida render metodi orqali 'index.html'
    # saxifasi taqdim qilindi
    return render(request, 'index.html', context)


def category_page(request, category_id):
    articles = Article.objects.filter(category_id=category_id)
    # SELECT * FROM articles WHERE category_id = ?, (category_id, )
    # articles = cursor.fetchall()
    category = Category.objects.get(pk=category_id)
    # SELECT * FROM categories WHERE pk = ?, (category_id, )
    # category = cursor.fetchone()
    categories = Category.objects.all()
    # SELECT * FROM categories;
    # categories = cursor.fetchall()
    context = {
        'title': f"Category: {category.title}",
        'articles': articles.order_by('-created_at'),
        'categories': categories
    }
    # MB so'rov jo'natib, kerakli ma'lumotlarni olib
    # lug'at ma'lumotlar turidagi 'context' nomli o'zgaruvchiga solib
    # index.html saxifasiga ma'lumotlarni joylab
    # foydalunuvchji so'riviga javob
    # sifatida render metodi orqali 'index.html'
    # saxifasi taqdim qilindi
    return render(request, 'index.html', context)


def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.data)
            article = Article.objects.create(**form.cleaned_data)
            # print(form.cleaned_data)
            article.save()
            return redirect('index')
    else:
        form = ArticleForm()
    context = {
        'form': form,
        'title': 'Create article'
    }

    return render(request, 'article_form.html', context)


def search_results(request):
    word = request.GET.get('q')

    articles = Article.objects.filter(
        Q(title__icontains=word) | Q(content__icontains=word)
    )

    context = {
        'title': f"Check results !",
        'articles': articles.order_by('-created_at')
    }

    return render(request, 'index.html', context)


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    article.views += 1
    article.save()

    context = {
        'article': article
    }

    return render(request, 'article_detail.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, 'Sign out successfully !')
    return redirect('index')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Sign in successfully !')
                return redirect('index')
            else:
                messages.error(request, 'Username or password is incorrect !')
                return redirect('login')
        else:
            messages.error(request, 'Username or password is incorrect !')
            return redirect('login')
    else:
        form = LoginForm()

    context = {
        'title': 'Sign in',
        'form': form
    }

    return render(request, 'user_login.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sign up successfully !')
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('register')
    else:
        form = RegistrationForm()

    context = {
        'title': 'Sign up',
        'form': form
    }

    return render(request, 'register.html', context)


def update_article(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article', id)
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('register')
    else:
        form = ArticleForm(instance=article)

    context = {
        'title': 'Update article',
        'form': form
    }
    return render(request, 'article_form.html', context)


def delete_article(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        article.delete()
        return redirect('index')

    context = {
        'article': article
    }

    return render(request, 'confirm_delete.html', context)

