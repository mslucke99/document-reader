# Food Objects
from foodObjects import *

## Web Scrapping 
from bs4 import BeautifulSoup
import requests
from requests.api import head

def error_web_scraping_handling(value,val_replace):
    if (value != None):
        txt= value.text
        return txt.replace(val_replace, "")
    return None

def fix_nutrition_data(data,serving_size):

    if data == None:
        return None

    #CREATE OBJECT 
    food_nutrition = Nutrition (serving_size)

    ## GET VALUE FROM TABLE 
    body =  data.find('tbody')
    if (body == None):
        return None
    #body = error_web_scraping_handling (body,"")   

    body_content = body.find_all('tr')
    ## Body Content Missing 
    if (body_content == []):
        return None

    for rows in body_content:
        
        value = rows.find_all('td',class_="nutriment_value")[1].text
        value = ' '.join(value.split())        
        label = rows.find('td',class_="nutriment_label").text.lower()
        label = ' '.join(label.split())  

        if ('kcal' in label):
            food_nutrition.calories = value
            
        elif ('energy (kj)' in label):
            food_nutrition.energy = value
            
        elif ('- saturated fat' in label):
            food_nutrition.saturated_fat = value

        elif ("- trans fat" in label):
            food_nutrition.trans_fat = value

        elif ("- cholesterol" in label):
            food_nutrition.trans_fat = value

        elif ('- sugars' in label):
            food_nutrition.sugars = value
            
        elif ('fat' == label):
            food_nutrition.fat = value
            
        elif ('proteins' in label):
            food_nutrition.proteins = value
            
        elif ('salt'in label):
           
            food_nutrition.salt = value
        elif ('sodium' in label):
            food_nutrition.sodium = value
            
        elif ('carbohydrates' in label):
            food_nutrition.carbohydrates = value 
            

    return food_nutrition

def web_scrapping(code_num):

    #Just in case - errror handling (it should never occur)
    if (type(code_num) != str):
        return None

    url = "https://world.openfoodfacts.org/product/" + code_num
    html_txt = requests.get(url,timeout=5)

    ## WEBSITE DOES NOT EXIST
    if (html_txt == None):
        return None

    content = BeautifulSoup(html_txt.content, 'lxml') #lxml parser being used


    #Ingredients of product
    ingredients = content.find('div',id = "ingredients_list")
    ingredients = error_web_scraping_handling (ingredients,"")
    
    ## Serving Size
    serving_size = content.find (lambda tag:tag.name=="p" and "Serving size:" in tag.text)
    serving_size = error_web_scraping_handling (serving_size,"Serving size: ")
    #serving_size = serving_size.replace("Serving size: ","") 

    #Nutrition Facts
    nutrition_data = content.find('table',id = "nutrition_data_table")
    nutrition_data = fix_nutrition_data (nutrition_data,serving_size)
    
    # Name of product
    name = content.find (lambda tag:tag.name=="p" and "Common name:" in tag.text)
    name = error_web_scraping_handling (name,"Common name: ")    
    #name = name.replace("Common name: ", "")

    # Possible Alergies of Product
    possible_allergies = content.find(lambda tag:tag.name=="p" and "Substances or products causing allergies or intolerances" in tag.text)
    possible_allergies = error_web_scraping_handling (possible_allergies,"Substances or products causing allergies or intolerances: ")
    #possible_allergies = possible_allergies.replace("Substances or products causing allergies or intolerances: ","")
    
    # Conservation Conditions
    conservation_conditions = content.find (lambda tag:tag.name=="p" and "Conservation conditions" in tag.text)
    conservation_conditions = error_web_scraping_handling (conservation_conditions,"Conservation conditions: ")    
    #conservation_conditions = conservation_conditions.replace("Conservation conditions: ","")
    
    #Quantity of Product 
    quantity = content.find(lambda tag:tag.name=="p" and "Quantity" in tag.text)
    quantity = error_web_scraping_handling (quantity,"Quantity: ")
    #quantity = quantity.replace("Quantity: ","")

    return  Food_Item (name,ingredients,nutrition_data,possible_allergies,conservation_conditions,quantity)
