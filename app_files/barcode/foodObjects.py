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
        return self.name
    