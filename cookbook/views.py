from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core import serializers
from models import Recipe, get_fn_recipe_urls

# Create your views here.
def home(request):
	#recipes = Recipe.objects.all()
	search = request.GET.get("search") #search function on site
	search_term = request.GET.get("search_foodnetwork") #search function goes to foodnetwork

	if search_term:
		print "look at me in search_term"
		get_fn_recipe_urls(search_term)
		recipe_search_result_list = Recipe.objects.filter(Q(ingredients__icontains=search_term) | Q(title__icontains=search_term))
		recipes = Recipe.objects.all()
		return render(request, 'cookbook/home.html', {"recipes": recipe_search_result_list})

	if search:
		recipe_search_result_list = Recipe.objects.filter(Q(ingredients__icontains=search) | Q(title__icontains=search))
		recipes = Recipe.objects.all()
		return render(request, 'cookbook/home.html', {"recipes": recipe_search_result_list})

	recipes = Recipe.objects.all()

	paginator = Paginator(recipes, 50)
	page = request.GET.get('page')
	try:
		recipes = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		recipes = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		recipes = paginator.page(paginator.num_pages)


	return render(request, "cookbook/home.html", {"recipes": recipes})

def single_recipe(request, num):
	recipe = Recipe.objects.get(pk=int(num))
	
	if recipe.publisher == "Food Network":
		ingredient_array = recipe.ingredients.split("^^")
		ingredient_array = ingredient_array[:-1]
		print ingredient_array

	else:
		ingredient_array = recipe.ingredients # tidy up formatting 
		ingredient_array = str(recipe.ingredients)
		ingredient_array = ingredient_array.replace("[u","")
		ingredient_array = ingredient_array.replace("]","")
		ingredient_array = ingredient_array.replace("'","")
		ingredient_array = ingredient_array.split(", u")
		#recipe.save()

	return render(request, "cookbook/single_recipe.html", {'recipe':recipe, 'ingredient_array': ingredient_array})