import requests

search_term = "avocado"

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
	

print recipe_data
