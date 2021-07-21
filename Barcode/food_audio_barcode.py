from speechRecog import say
from speechRecog import listen_continuously
from speechRecog import get_command
import food_barcode as barcode
import os
import time

## MISSING OVER INFORMATION 
def voice_over_information(info,food_item):
                
        info = info.lower()
        print(info)
        
        if ("ingredients" in info):
            print("INGREDIENTS")
            print(food_item.ingredients)
            say("INGREDIENTS")
            say(food_item.ingredients)
            print()
            
        elif ("allergies" in info):
            print("ALLERGIES")
            print(food_item.allergies)
            say("ALLERGIES")
            say(food_item.allergies)
            print()

        elif ("quantity" in info):
            print("QUANTITY")
            print(food_item.quantity)
            say("QUANTITY")
            say(food_item.quantity)
            print()

        elif ("values" in info):
            print("VALUES")
            print(food_item.nutrition_data.repr())
            say("VALUES")
            say(food_item.nutrition_data.repr())
            print()
            
        elif ("conservation" in info):
            print("CONSERVATION")
            print(food_item.conservation)
            say("CONSERVATION")
            say(food_item.conservation)
            print()

        elif ("exit" in info):
            return
        
        ## Check for number - to print
        else:
            num = ""
            for s in info.split():
                if s.isdigit():
                    num += s

            if (num == food_item.exit_num):
                return
            elif (num in food_item.numbered_values.keys()):
                print (food_item.numbered_values[num])
                say(food_item.numbered_values[num])
            else:
                print("No information about what you are looking was found.")
                print ("Please try again")
                say("No information about what you are looking was found.")
                say ("Please try again")
    
        
        info = None
        while(info == None):
            print()
            print()
            print (food_item.get_titles())
            say (food_item.get_titles())
            info = get_command("Any more information do you want to listen to?")
            if (info != None):
                    voice_over_information(info,food_item)

        
def food_item_titles(food_item):
    if (food_item == None or food_item.name == None):
        print("There is no food item with that barcode.")
        say("There is no food item with that barcode.")
    else:
        print ("We found information about ",food_item.name)
        say ("We found information about " + food_item.name)
        print (food_item.get_titles())
        say (food_item.get_titles())

        info = None
        while(info == None):
            info = get_command("Which information do you want to listen to?")
        
        voice_over_information(info,food_item)
        
def main():
    intro_phrase = "Hello. If you want us to scan a food item please say: Alexa scan food item\n\n If you want alexa to stop listening please say Alexa exit"

    while True:
        command = listen_continuously(intro_phrase)
        print(command)
        if "exit" in command: 
            break
        elif "food item" in command:
            say("Proceeding to scan food item")
            food_item = barcode.main()
            food_item_titles(food_item)
            intro_phrase = "Please say  Alexa scan food item if you want to scan another item, otherwise say Alexa exit to exit the program"
        


main()
