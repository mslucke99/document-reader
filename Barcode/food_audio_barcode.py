from speechRecog import say
from speechRecog import listen_continuously
from speechRecog import get_command
import barcode
import os


## MISSING OVER INFORMATION 
def voice_over_information(info):
        print()
        print("INGREDIENTS")
        print(food_item.ingredients)
        print()
        print("ALLERGIES")
        print(food_item.allergies)
        print()
        print("QUANTITY")
        print(food_item.quantity)
        print()
        print("VALUES")
        print(food_item.nutrition_data.repr())

def food_item_titles(food_item):
    if (food_item == None or food_item.name == None):
        print("There is no food item with that barcode.")
    else:
        print ("We found information about ",food_item.name)
        say ("We found information about " + food_item.name)
        print (food_item.get_titles())
        say (food_item.get_titles())

        say ("Which information do you want to listen to? ")
        info = get_command()
        print(info)

        voice_over_information(info)
        
def main():
    say("Hello. If you want us to scan a food item please say: Alexa scan food item and if you want alexa to stop listening please say Alexa exit")
    while True:
        command = listen_continuously()
        print(command)
        if "exit" in command: 
            break
        if "food item" in command:
            say("Proceeding to scan food item")
            food_item = barcode.main()
            food_item_titles(food_item)
            break


main()

