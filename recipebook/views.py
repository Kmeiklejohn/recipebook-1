from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.shortcuts import reverse
from .models import Recipe, Author, User
from .forms import AddAuthor, AddRecipe, LoginForm, UpdateForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    return render(request, 'index.html', {'recipes': Recipe.objects.all()})


def recipe(request, recipe_id):
    data = {}
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    author = get_object_or_404(Author, pk=recipe.author.id)
    data.update({'recipe': recipe, 'author':author})
    data.update(edit_recipe(request, recipe))
    if request.method == 'POST':
        update_recipe(request, recipe)
        return HttpResponseRedirect(reverse('recipe', kwargs={"recipe_id": recipe_id}))
    return render(request, 'recipe.html', data)


def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    recipes = Recipe.objects.filter(author_id=author_id)
    return render(request, 'author.html',
                  {'author': author, 'recipes': recipes})

@login_required()
def edit_recipe(request, recipe):
 
    updated = {}
    if request.user.is_staff or request.user.author == recipe.author:
        form = UpdateForm(initial={
                                "title": recipe.title,
                                "description": recipe.description,
                                "instructions": recipe.instructions,
                                "time=": recipe.time})
        updated.update({"form": form})
    favorite = False
    try:
        if recipe in request.user.author.favorites.all():
            favorited = True
    except:
        pass
        updated.update({"favorites": favorited})
    return updated


@login_required()
def profile(request):
    if request.user.author:
        author = request.user.author
        recipes = Recipe.objects.filter(author_id=author)
        favorites = request.user.author.favorites.all()
    return render(request, 'profile.html', {'recipes':recipes, 'author': author, 'favorites':favorites})

def favorite(request, recipe_id):
    """to favorite a recipe"""
    user = request.user.author
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe not in user.favorites.all():
        user.favorites.add(recipe)
    elif recipe in user.favorites.all():
        user.favorites.remove(recipe)
    return HttpResponseRedirect(reverse('profile'))


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

def update_recipe(request, recipe):
    form = UpdateForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        recipe.title = data['title']
        recipe.description = data['description']
        recipe.instructions = data['instructions']
        recipe.time = data['time']
        recipe.save()
    return