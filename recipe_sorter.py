import re
import json
import os


def get_matches(ingredients, recipe):
    try:
        with open("Recept/"+recipe+"/ingredients.json", "r") as f:
            data = json.load(f)
            found = 0
            nr_ingredients = len(data)

            for ingredients_have in ingredients[:]:
                for ingredients_need in data.values():
                    match = re.search(ingredients_have, ingredients_need.lower())
                    if match is not None:
                        found += 1
                        break
            
            print(recipe)
            print("Matched " + str(100*found/nr_ingredients) + "% of the ingredients")
            print(ingredients)
            print(list(data.values()))
    except:
        print("Something went wrong loading the json for " + recipe)

   

    

ingredients = ['pasta', 'ingefära', 'vitlök', 'gul lök', 'strösocker', 'salt']
for root, dirs, files in os.walk("Recept/"):
    recipes = dirs
    break


for i in range(5):
    get_matches(ingredients, recipes[i])



