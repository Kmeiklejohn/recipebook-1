from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.shortcuts import reverse
from .models import Recipe, Author, User
from .forms import AddAuthor, AddRecipe, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    return render(request, 'index.html', {'recipes': Recipe.objects.all()})


def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    author = get_object_or_404(Author, pk=recipe.author.id)
    return render(request, 'recipe.html',
                  {'recipe': recipe, 'author': author})


def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    recipes = Recipe.objects.filter(author_id=author_id)
    return render(request, 'author.html',
                  {'author': author, 'recipes': recipes})


@login_required()
@staff_member_required(login_url='error')
def add_author(request):
    html_get = 'addauthor.html'
    if request.method == 'POST':
        form = AddAuthor(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['name'],
                email=data['email'],
                password=data['password']
            )
            login(request, user)
            Author.objects.create(
                name=data['name'],
                user=user,
                bio=data['bio']
            )
            return HttpResponseRedirect(reverse('index'))
    else:
        form = AddAuthor()
        return render(request, html_get, {'form': form})


@login_required()
def add_recipe(request):
    html_template = 'addrecipe.html'
    if request.method == 'POST':
        form = AddRecipe(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data['title'],
                author=data['author'],
                description=data['description'],
                time=data['time'],
                instructions=data['instructions']
            )
            return render(request, 'confirmation.html', {'record': 'Recipe!'})
    else:
        form = AddRecipe()
        if not request.user.is_staff:
            form.fields['author'].queryset = Author.objects.filter(
                user=request.user)
        return render(request, html_template, {'form': form})


def login_view(request):
    html_template = 'login.html'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))

    form = LoginForm()
    return render(request, html_template, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def error_view(request):
    return render(request, 'error.html')
