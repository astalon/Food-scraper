from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import re
import os
import json
import shutil

# Food scraper designed for downloading ingredients, instructions and picture from a Ica recipe website
def scrape(url):
	ingredients_json = {}
	instructions_json = {}

	opts = webdriver.FirefoxOptions()
	opts.headless = True

	firefox_binary = FirefoxBinary('/usr/bin/firefox')
	driver = webdriver.Firefox(firefox_binary=firefox_binary, options=opts)

	driver.get(url)

	title = driver.title
	title_end_index = re.search("Recept", title).start()
	title=title[:title_end_index-3]

	org_title = title
	title = "Recept/"+title
	if os.path.exists(title):
		print(org_title + " already exists")
	else:	

		try:
			#instructions = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"cooking-step__content__instruction")))
			#instructions = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"ingredients__list__item")))

			instructions = driver.find_elements_by_class_name("cooking-step__content__instruction")
			ingredients = driver.find_elements_by_class_name("ingredients__list__item")
			img = driver.find_elements_by_class_name("recipe-image-square__image")
			os.makedirs(title)
			nr_ingredients = len(ingredients)

			for i in range(nr_ingredients):
				ingredients_json[str(i)] = ingredients[i].text


			for i in range(0, len(instructions)):
				instructions_json[str(i)] = instructions[i].text

			string = img[0].get_property('attributes')['1']['value']

			# Extract actual source that we can use,
			res1= re.search("assets", string)
			start = res1.start()
			res2 = re.search("jpg", string)
			end = res2.end()

			#Save instructions and ingredients to a json
			with open(title+'/ingredients.json', 'w') as f:
				json.dump(ingredients_json, f, ensure_ascii=False)

			with open(title+'/instructions.json', 'w') as f:
				json.dump(instructions_json, f, ensure_ascii=False)

			# Save the image
			src = string[start:end]
			driver.get("https://"+src)
			driver.save_screenshot(title + '/' + org_title+".png")
			print("Done: ", org_title)

		except:
			print("Something went wrong while getting instructions, ingredients or picture")



	driver.close()
