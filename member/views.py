from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from cookbook.models import Note, Recipe, Cookbook_Item
from django.contrib.auth.decorators import login_required


# Create your views here.

def create_account(request):
	# return HttpResponse("sign up")
	return render(request, "member/create_account.html")

def register(request):
	username = request.POST.get("username")
	email = request.POST.get("email")
	password = request.POST.get("password")
	first_name = request.POST.get("first_name")
	user = User.objects.create_user(username, email, password)	
	user.first_name = first_name
	user.save()
	return render(request, "member/login.html")

def logout_user(request):
    logout(request)
    print "logged out!"
    return redirect('/cookbook')

def login_user(request):
	return render(request, "member/login.html")


def authenticate_user(request):
	username = request.POST["username"]
	password = request.POST["password"]
	
	user = authenticate(username=username, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return redirect('/cookbook')
		else:
			return HttpResponse("Disabled account")
	else:
		return HttpResponse("invalid login")

def add_recipe(request):
	recipe_id = int(request.GET["recipe_id"])
	user_id = request.user.id
	print "add_recipe here", user_id
	ci = Cookbook_Item()
	#just assign to recipe_id and user_id
	ci.recipe_id = Recipe.objects.get(pk=recipe_id)
	ci.user_id = User.objects.get(pk=user_id)
	ci.save()
	return redirect("member_home")

def remove_recipe(request):
	recipe_id = int(request.GET["recipe_id"])
	user_id = request.user.id
	items_to_delete = Cookbook_Item.objects.filter(user_id = user_id, recipe_id = recipe_id)
	for item in items_to_delete:
		print "item pk here: ", item.pk
		Cookbook_Item.objects.filter(pk = item.pk).delete()
	# ci = Cookbook_Item()
	# ci.recipe_id = Recipe.objects.get(pk=recipe_id)
	# ci.user_id = User.objects.get(pk=user_id)
	# ci.save()
	return HttpResponseRedirect("member_home.html")

def member_home(request):
	user = request.user
	username = request.user.username
	user_id = request.user.id
	user_cookbook = Cookbook_Item.objects.filter(user_id = user_id)
	return render(request, "member/member_home.html", {"user": user, "user_cookbook": user_cookbook})

def member_recipe(request, num):
	recipe = Recipe.objects.get(pk=int(num))

	if recipe.publisher == "Food Network":
		ingredient_array = recipe.ingredients.split("^^")
		ingredient_array = ingredient_array[:-1]
		print ingredient_array
	else:
		ingredient_array = recipe.ingredients
		ingredient_array = str(recipe.ingredients)
		ingredient_array = ingredient_array.replace("[u","")
		ingredient_array = ingredient_array.replace("]","")
		ingredient_array = ingredient_array.replace("'","")
		ingredient_array = ingredient_array.split(", u")
		#recipe.save()

	user = request.user
	notes = Note.objects.filter(user_id = user.pk, recipe_id = int(num))
	
	return render(request, "member/member_recipe.html", {'recipe':recipe, 'notes': notes, "ingredient_array": ingredient_array})

def add_note(request):
	user = request.user
	recipe_note = request.GET.get('recipe_note')
	recipe_id = request.GET.get("recipe_id")
	r = Recipe(pk=recipe_id)
	#refactor to one line using Note.create()
	n = Note.objects.create(user_id = user, note_text = recipe_note, recipe_id = r)
	# n.user_id = user
	# n.note_text = recipe_note
	# n.recipe_id = r
	# n.save()
	
	return HttpResponseRedirect("member/recipe" + str(recipe_id))

def remove_note(request):
	note_id = int(request.GET["note_id"])
	recipe_id = request.GET["recipe_id"]
	#user_id = request.user.id
	#note_to_delete = Note.objects.filter(note_id = note_id)
	Note.objects.filter(pk = note_id).delete()
	# ci = Cookbook_Item()
	# ci.recipe_id = Recipe.objects.get(pk=recipe_id)
	# ci.user_id = User.objects.get(pk=user_id)
	# ci.save()
	return HttpResponseRedirect("member/recipe" + str(recipe_id))



