#Freestyle Project: Recipes App
#Noemi Higashi


import json
import os
import requests

api_key = (os.environ['MASH_KEY'])

def start():
    print ("""

     _                    _      _   _                       _    _
    | |                  | |    | | ( )                     | |  | |
    | |__   ___ _   _    | | ___| |_|/ ___    ___ ___   ___ | | _| |
    | '_ \ / _ \ | | |   | |/ _ \ __| / __|  / __/ _ \ / _ \| |/ / |
    | | | |  __/ |_| |_  | |  __/ |_  \__ \ | (_| (_) | (_) |   <|_|
    |_| |_|\___|\__, ( ) |_|\___|\__| |___/  \___\___/ \___/|_|\_(_)
                 __/ |/
                |___/

    Welcome to the Recipes App!
    We'll help you to be a chef using the ingredients you already have at home.
    Let's get it started!
    """)



def searching_recipes(ingredients):
    #Requesting Search By Ingredients
    print ("Searching for recipes...")
    print ("----------------------")

    request_url_search = f"https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?ingredients={ingredients}&number=5&ranking=1"
    headers_search= {"X-Mashape-Key":api_key,
    "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"}

    response_search = requests.get(request_url_search,headers=headers_search)
    response_body = json.loads(response_search.text)
    response_txt = str(response_body)


    recipes_list = []
    x=0
    for p in response_body:
        x+=1
        print (" Item #" + str(x) + " " + str(p["title"]))
        if p["missedIngredientCount"] == 1:
            print (" ---> You just need 1 more ingredient to prepare this recipe.")
        elif p["missedIngredientCount"] > 1:
            print (" ---> You need " + str(p["missedIngredientCount"]) + " more ingredients to prepare this recipe.")
        else:
            print (" ---> You have all the ingredients you need to prepare this recipe!")
        print ("----------------------")
        recipes_list.append([p["id"],p["title"]])

    chosen_recipe = input ("Which recipe would you like to cook today? Plese, type the item number: ")

    if int(chosen_recipe) > 5:
        quit ("Ops...  This recipe number is not valid. Please try again.")

    chosen_recipe = int(chosen_recipe) - 1
    chosen_recipe_item = recipes_list[int(chosen_recipe)]
    global chosen_id
    chosen_id = chosen_recipe_item[0]
    global chosen_recipe_name
    chosen_recipe_name = chosen_recipe_item[1]

    print ("""
    ========================================
    """)
    print ("*** "+ str.upper(chosen_recipe_name)+ " ***")


def requesting_ingredients():
    #Requesting Ingredients and Prep Time
    request_url_ingredients = f"https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{chosen_id}/information"
    headers_recipe= {"X-Mashape-Key":api_key,
    "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"}

    response_ingredients = requests.get(request_url_ingredients,headers=headers_recipe)
    global response_body_ingredients
    response_body_ingredients = json.loads(response_ingredients.text)
    response_txt_ingredients = str(response_body_ingredients)

    def prep_time(list):
        time = str(int(list["preparationMinutes"]) + int(list["cookingMinutes"]))
        print ("Ready in " + time + " minutes")

    try:
        prep_time(list=response_txt_ingredients)
    except Exception:
        pass

    print ("""
    INGREDIENTS:""")

    for d in response_body_ingredients["extendedIngredients"]:
        print ("- " + str(d["original"]))


def requesting_instructions():
    #Requesting recipe detailed instructions
    request_url_recipe = f"https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{chosen_id}/analyzedInstructions?stepBreakdown=true"
    headers_recipe= {"X-Mashape-Key":api_key,
    "X-Mashape-Host": "spoonacular-recipe-food-nutrition-v1.p.mashape.com"}

    response_recipe = requests.get(request_url_recipe,headers=headers_recipe)
    global response_body_recipe
    response_body_recipe = json.loads(response_recipe.text)


    print ("""
    INSTRUCTIONS:""")



def steps (list):
    x=0
    for p in list:
        x=x+1
        print ("-----------------")
        print ("(Part " + str(x) + ") " + str(p["name"]))
        print ("-----------------")
        for s in p["steps"]:
            print (str(s["number"]) +" - " + str(s["step"]))

    print ("""
========================================""")




#Writing the Cookbook
def write_products_to_file(ingredients, instructions):
    filepath = os.path.join(os.path.dirname(__file__),"..","db","recipes_list.txt")
    print(f"ADDING THIS RECIPE TO FILE: '{filepath}' ")
    response_txt = str(list)
    with open(filepath, "a") as File_object:
        File_object.write("***" + str(chosen_recipe_name)+ "***\n")
        File_object.write ("----------------- \n")
        File_object.write ("INGREDIENTS:"+ "\n")
        for d in ingredients["extendedIngredients"]:
            File_object.write("- " + str(d["original"])+ "\n")
        File_object.write ("----------------- \n")
        File_object.write ("INSTRUCTIONS:"+ "\n")
        x=0
        for p in instructions:
            x=x+1
            File_object.write("(Part " + str(x) + ") " + str(p["name"]) + "\n")
            for s in p["steps"]:
                File_object.write (str(s["number"]) +" - " + str(s["step"]) + "\n")
        File_object.write("================================ \n" + "\n"+ "\n")



#--------------------------------
#Running Application

def run():
    start()

    ingredients = input ("Type the ingredients you want to use: ")

    #Validating input
    try:
        float(ingredients)
        quit ("Ops...  Numbers are not valid. Please try again.")
    except ValueError as e:
        pass

    searching_recipes(ingredients=ingredients)


    requesting_ingredients()
    requesting_instructions()
    steps (response_body_recipe)

    cookbook = input("Would you like to add this recipe to your Personal Cookbook file? (y/n): ")

    if cookbook == "y":
        write_products_to_file (ingredients=response_body_ingredients, instructions=response_body_recipe)

run()
