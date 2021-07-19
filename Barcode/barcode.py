#!pip install opencv-python
#!pip install numpy
#!apt install libzbar0
#!pip install pyzbar


#!pip install beautifulsoup4
#!pip install lxml 
#!pip install requests


### FOOD OBJECT CLASSES
class Nutrition:
    def __init__(self,serving_size=None,energy=None,calories=None,fat=None,saturated_fat=None,carbohydrates=None,sugars=None,proteins=None,salt=None,sodium = None):
        self.serving_size = serving_size
        self.energy = energy
        self.calories = calories
        self.fat = fat
        self.saturated_fat = saturated_fat
        self.carbohydrates = carbohydrates
        self.sugars = sugars 
        self.proteins = proteins
        self.salt = salt
        self.sodium  = sodium
        self.cholesterol = None
        self.trans_fat = None
    def repr(self):
        str_val = ""

        if (self.serving_size != None):
            str_val += "Serving Size: " + self.serving_size + "\n"

        if (self.energy != None):
            str_val += "Energy (kJ): " + self.energy + "\n"
        
        if(self.calories != None):
            str_val += "Calories: " + self.calories + "\n"

        if (self.fat != None):
            str_val += "Fat: " + self.fat
            if (self.saturated_fat != None):
                str_val += "of which " + self.saturated_fat + " is saturated fat" 
            if (self.trans_fat != None):
                str_val += ", " + self.trans_fat + " is trans fat"
            if (self.cholesterol != None):
                str_val += " and " + self.cholesterol + " is cholesterol"  
            str_val += "\n"
        
        if (self.proteins != None):
            str_val += "Protein: " + self.proteins + "\n"

        if (self.carbohydrates != None):
            str_val += "Carbs: " + self.carbohydrates
            if (self.sugars != None):
                str_val += "of which " + self.sugars + " is sugar" 
            str_val  += "\n"

        if (self.salt != None):
            str_val += "Salt: " + self.salt
            if (self.sodium != None):
                str_val += "of which " + self.sodium + " is sodium" 

        return str_val
class Food_Item:
    def __init__(self,name=None,ingredients=None,nutrition_data=None,allergies=None,conservation=None,quantity=None):
        self.name = name
        self.ingredients = ingredients
        self.nutrition_data= nutrition_data
        self.allergies= allergies
        self.conservation= conservation
        self.quantity=quantity

    def get_titles(self):
        i = 1
        str_val = ""
        if (self.ingredients != None):
            str_val += str(i) + ". Ingredients" + "\n"
            i+=1
        if (self.nutrition_data != None):
            i+=1
            str_val += str(i) + ". Nutrition Data"  + "\n"
        if (self.allergies != None):
            str_val += str(i) + ". Possible Allergies"  + "\n"
            i+=1
        if (self.conservation != None):
            str_val += str(i)+ ". Method of Conservation"  + "\n"
            i+=1
        if (self.quantity != None):
            str_val += str(i) + ". Quantity"  + "\n"
            i+=1
        str_val += str(i) + ". None" + "\n"
        return str_val

    def __str__(self):
        pass
    

## Temporary import to see results
from os import name
import time
from speechRecog import say

## Computer Vision 
import cv2
import numpy as np
import pyzbar.pyzbar as zbar

## Web Scrapping 
from bs4 import BeautifulSoup
import requests
from requests.api import head
    
## THINGS TO IMPROVE
#   How to integrate it with the main parts of the prototype
#   Add timeout to the video capture - display message
#   Can the video see partially the barcode, but not read it do to finger? 
#   Different display partially visual imprared to fully visually impared

## BARCODE DETECTION WITH OPEN CV
def check_barcode(img):
    return zbar.decode(img)

def video_capture():

    #get the camera
    capture = cv2.VideoCapture(0)

    #size of the screen shown 
    capture.set(3,640)#width
    capture.set(4,480)#height

    startTime =  time.time()
    while True:
        success,img = capture.read()

        ## TIME LIMIT OF 1 MINUTE TO FIND BARCODE
        timeElapsed = int (time.time() - startTime)
        if (timeElapsed > 60):
            return -1
        if success:
            cv2.imshow("Frame",img)
            barcodes = check_barcode(img)
            #print("the barcode of this frame is ", barcodes)

            if barcodes != []:
                return barcodes
        else:
            break

        ## adds a delay and escapes a video  - used only for debuggin
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def decode_barcode(barcodes):
    for barcode in barcodes:
        bc = (barcode.data)
        #bc = re.findall("\d+", str(bc))
        bc = ("".join(filter(str.isdigit, str(bc))))
        return bc


### WEB SCRAPPING GIVEN BARCODE 
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
    url = "https://world.openfoodfacts.org/product/" + code_num
    print(url)
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

def main():
    barcodes = video_capture()
    if barcodes == -1:
        say ("1 minute has elapsed and we have not found a barcode. Please try again later")

    barcodes = decode_barcode(barcodes)
    food_item = web_scrapping(barcodes)
    #food_item = web_scrapping("0009800895250")
    return food_item


if __name__ == "__main__":
    path = "C:/Users/larfe/Documents/Mycroft-Dev/Research_Summer_2021/Barcode/Pictures/3.jfif" 
    main()
    time.sleep(2000)

#My Symcode scanner
# CMOS or CCD technology

#https://barcodesdatabase.org/

#https://bytescout.com/blog/barcode-information.html
#https://upcdatabase.org/
 #b'5602512802278'