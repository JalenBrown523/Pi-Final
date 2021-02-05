from tkinter import *
import requests

class ControlFrame(Frame):
    # The constructor
    def __init__(self, parent):
        # Call the constructor in the superclass
        Frame.__init__(self, parent)

    def __str__(self):
        pass

    # Sets up the GUI
    def setupGUI(self):
        # Makes the frame the size of the window
        self.pack(side=TOP, expand=1, fill=BOTH)

        # Enter ingredients' label
        ControlFrame.instructLabel = Label(self, text="Enter ingredients", font='verdana 18')
        ControlFrame.instructLabel.pack(anchor=N)

        # Creates the Textbox
        ControlFrame.user_input = Entry(self, bg="white", font='kristen 16')

        # Function that will process input from user
        ControlFrame.user_input.bind("<Return>", self.process)
        ControlFrame.user_input.pack(side=BOTTOM, fill=X)
        ControlFrame.user_input.focus()

    def process(self, event):
        # Resets the recepie list when one a word is entered
        IngredientFrame.myList.delete(0, END)

        # Take the input from the input line and sets them all to lower case
        action = ControlFrame.user_input.get().lower()

        # No two word ingredients (e.g. rice cakes = rice, cakes)
        ingredients = action.split()

        # Sets response to the retrieved recipes from the website
        response = requests.get(
            f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&includeIngredients={','.join(ingredients)}&number=2&fillIngredients=true&addRecipeInformation=true")
        responseJSON = response.json()

        # Create list of recipe items
        ControlFrame.Recipes = [Recipe(recipeJSON) for recipeJSON in responseJSON["results"]]

        # If responsejson is an empy string(ex. no response) then chage the text of the instruction lable
        # Handles invalid input from the user
        if (responseJSON == []):
            print("Search Error: Invalid ingredient/No results")
            ControlFrame.instructLabel.config(text="invalid input!!!!!!!, please try again.", fg="red",
                                              font="helvetica 18 bold")

        else:
            ControlFrame.instructLabel.config(text="What Ingredients do you have?", fg="black",
                                              font="helvetica 18 bold")

        # Ddd recipes to GUI
        for recipe in ControlFrame.Recipes:
            rFrame.addRecipe(recipe)

        # Resets the Textbox after input
        ControlFrame.user_input.delete(0, END)


class Recipe():
    # JavaScript Object Notation(JSON) converts Python objects to JavaScript
    # Allows for communication b/t APi's & databases b/c Python objects cannot
    def __init__(self, recipeJSON):
        self.id = recipeJSON["id"]
        self.title = recipeJSON["title"]
        self.img = recipeJSON["image"]
        self.likes = recipeJSON["likes"]
        self.ingUsed = recipeJSON["usedIngredientCount"]
        self.ingMiss = recipeJSON["missedIngredientCount"]

    def __str__(self):
        return self.title


class IngredientFrame(Frame):
    def __init__(self, parent):
        # Call the constructor in the superclass
        Frame.__init__(self, parent)

    def setupGUI(self):
        self.pack(side=TOP, expand=1, fill=BOTH)

        IngredientFrame.RecipeInfo = Text(self, state=DISABLED)
        IngredientFrame.RecipeInfo.pack(side=TOP, fill=BOTH)

        IngredientFrame.instructLabel = Label(self, text="Your list of recipes")
        IngredientFrame.instructLabel.pack(anchor=N)

        # Setup scroll bar
        IngredientFrame.scroll = Scrollbar(window)
        IngredientFrame.scroll.pack(side=RIGHT, fill=Y)

        # Create list
        IngredientFrame.myList = Listbox(window)
        IngredientFrame.myList.pack(side=TOP, expand=1, fill=BOTH)
        IngredientFrame.myList.bind('<<ListboxSelect>>', self.expandRecipe)

        # Link scroll bar to listbox
        IngredientFrame.myList.config(yscrollcommand=IngredientFrame.scroll.set)
        IngredientFrame.scroll.config(command=IngredientFrame.myList.yview)

    def addRecipe(self, Recipe):
        IngredientFrame.myList.insert(END,
                                  f"{Recipe.title}  |  Likes: {Recipe.likes}  |  Missing Ingredients: {Recipe.ingMiss}")

    def expandRecipe(self, event):
        # Runs if a recipe is selected
        if (IngredientFrame.myList.curselection()):
            recipe = ControlFrame.Recipes[IngredientFrame.myList.curselection()[0]]
            # TODO Check if this recipe is already displayed
            response = requests.get(f"https://api.spoonacular.com/recipes/{recipe.id}/information?apiKey={api_key}")
            responseJSON = response.json()
            IngredientFrame.RecipeInfo.config(state=NORMAL)
            IngredientFrame.RecipeInfo.delete("1.0", END)
            sumarry = responseJSON["summary"]
            IngredientFrame.RecipeInfo.insert(END, f"{recipe.title}\n\n{sumarry}")


##################################################################################
api_key = "b29344da13414323bac320e823e7736a"
# The default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600

# Create the window
window = Tk()
window.title("Find A Recipe")
window.geometry(f"{WIDTH}x{HEIGHT}")
window.minsize(WIDTH, HEIGHT)

# Create the controls GUI as a Tkinter Frame inside the window
cFrame = ControlFrame(window)
cFrame.setupGUI()

# Create the recipe display frame inside the window
rFrame = IngredientFrame(window)
rFrame.setupGUI()

# Wait for the window to close
window.mainloop()




