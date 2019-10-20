from django.db import models
from django.contrib.auth.models import User
import requests
from datetime import datetime
from bs4 import BeautifulSoup, SoupStrainer
import urllib2
from bs4.diagnose import diagnose
from lxml import etree
from io import StringIO, BytesIO
import re, urllib2
import requests

# Create your models here.

class Recipe(models.Model):
	title = models.CharField(max_length=240)
	instructions = models.TextField()
	ingredients = models.TextField()
	recipe_all = models.TextField()
	recipe_id_from_api = models.CharField(max_length=30, default="empty")
	category = models.CharField(max_length = 120)
	original_url = models.TextField()
	publisher = models.CharField(max_length = 240)

class Cookbook_Item(models.Model):
	user_id = models.ForeignKey(User)
	recipe_id = models.OneToOneField(Recipe, primary_key=True)
	 
class Note(models.Model):
	user_id = models.ForeignKey(User)
	recipe_id = models.ForeignKey(Recipe)
	cookbook_item_id = models.ForeignKey(Cookbook_Item, default=0)
	note_text = models.TextField(blank=True)
	date_created = models.DateTimeField(auto_now=True)

def get_recipe_data(search_term):

	# This is the aspect of my project that felt meaningful to me during the bootcamp. 
	# Though not technically glamourous or fancy, getting data back from other websites helped me appreciate the power of technology to 
	# connect us to each other - technology's ability to improve our lives as individuals by connecting us to collective resources.
	url = "http://food2fork.com/api/search?key=d4438ab104014743528bec98686f3e42&q=" + search_term

	results = requests.get(url).json()

	i = 0
	recipe_data = {}
	while i<30:
		recipe_data[results["recipes"][i]["recipe_id"]] = {"title": results["recipes"][i]["title"], "publisher": results["recipes"][i]["publisher"], "source_url":results["recipes"][i]["source_url"]}
		i += 1

	for key in recipe_data:
		recipe_url = "http://food2fork.com/api/get?key=d4438ab104014743528bec98686f3e42&rId=" + key
		recipe_results = requests.get(recipe_url).json()
		recipe_data[key]["ingredients"] = recipe_results["recipe"]["ingredients"]

	return recipe_data

def add_recipe_to_db(recipe_data):
	
	recipes_in_db = Recipe.objects.all()
	id_list = []
	
	for recipe in recipes_in_db:
		id_list.append(recipe.recipe_id_from_api)

	for key in recipe_data:

		if key not in id_list:
			r = Recipe(recipe_id_from_api=key, title=recipe_data[key]["title"],  original_url=recipe_data[key]["source_url"], ingredients=recipe_data[key]["ingredients"], publisher=recipe_data[key]["publisher"] )
			r.save()

	return "Added that batch"
	
def get_fn_recipe_urls(search_term):
	
	search_url = 'http://www.foodnetwork.com/search/search-results.html?searchTerm=' + search_term + '&form=global&_charset_=UTF-8'
	page = urllib2.urlopen(search_url).read()
	soup = BeautifulSoup(page, "lxml")
	link_mess= soup.find_all(href=re.compile("/recipes/.*html$")) #includes duplicates and extra stuff
	links = [] 
	for tag in link_mess:
		links.append(tag.get("href"))  # clean addresses but has duplicates

	filtered_links = []
	filtered_links2 = []
	recipe_titles = []
	one_recipe_base_url = "http://www.foodnetwork.com" 

	for each in links:
		#get rid of dupes and eliminate non-recipes
		if each not in filtered_links and each[-11:] == "recipe.html":
			filtered_links.append(each)

	for each in filtered_links:
		filtered_links2.append(one_recipe_base_url + each)

	for link in filtered_links2[:-1]: # don't need index a-z recipe link on end
		page = urllib2.urlopen(link).read()
		soup = BeautifulSoup(page, "lxml")
		
		num_of_ingredients = len(soup.find_all(itemprop="ingredients"))
		i = 0
		ingredient_string = ""
		while i < num_of_ingredients: # get all the ingredients 
			ingredient_string += (soup.find_all(itemprop="ingredients")[i].get_text() + "^^")
			i += 1

		messy_instructions = soup.find(itemprop="recipeInstructions").find_all("p")
		instruction_length = len(messy_instructions)
		title = soup.find(itemprop="name").get_text()
		i = 0
		instruction_string = ""
		while i < instruction_length: # get the instructions
			instruction_string += soup.find(itemprop="recipeInstructions").find_all("p")[i].get_text()
			i += 1
			
		recipes_in_db = Recipe.objects.all() 
		original_url_list = []
			
		for recipe in recipes_in_db:
			original_url_list.append(recipe.original_url)

		# add new Food Network recipe if we do not already have it based on link (recipe names are not always unique enough)
		if link not in original_url_list: 
			r = Recipe(ingredients=ingredient_string, original_url=link, title=title, instructions=instruction_string, publisher="Food Network") 
			r.save()

	return "Ok done"

