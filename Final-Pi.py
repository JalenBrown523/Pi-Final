from tkinter import *
import re
import requests
# PIL library to import images


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
        ControlFrame.instructLabel = Label(
            self, text="Enter Some Ingredients", font='verdana 15')
        ControlFrame.instructLabel.pack(anchor=N)

        # Creates the Textbox
        ControlFrame.user_input = Entry(self, bg="white", font='kristen 16')
        ControlFrame.user_input.pack(side=TOP, fill=X)
        # Cursor is set('focused') on the Textbox
        ControlFrame.user_input.focus()
        # Binds enter key to process input from user
        ControlFrame.user_input.bind("<Return>", self.process)

    def process(self, event):
        # Take the input from the input line and sets them all to lower case
        action = ControlFrame.user_input.get().lower()
        # No two word ingredients (e.g. rice cakes = rice, cakes)
        ingredients = action.split()

        # Sets response to the retrieved recipes from the website
        response = requests.get(
            f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&includeIngredients={','.join(ingredients)}&number=2&fillIngredients=true&addRecipeInformation=true")
        responseJSON = response.json()

        # Create list of recipe items
        ControlFrame.Recipes = [Recipe(recipeJSON)
                                for recipeJSON in responseJSON]

        # If responsejson is an empTy string(ex. no response) then change the text of the instruction label
        # Handles invalid input from the user
        if (responseJSON == []):
            ControlFrame.instructLabel.config(
                text="Search Error\n Check Spelling", fg="red", font="helvetica 15")

        else:
            ControlFrame.instructLabel.config(
                text="Results", fg="black", font="helvetica 15")

        # Adds recipes to the list
        for recipe in ControlFrame.Recipes:
            rFrame.addRecipe(recipe)

        # Resets the Textbox after input
        ControlFrame.user_input.delete(0, END)

        ControlFrame.responseLabel.configure(text=response.elasped)


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


class ResultFrame(Frame):
    def __init__(self, parent):
        # Call the constructor in the superclass
        Frame.__init__(self, parent)

    def setupGUI(self):
        self.pack(side=TOP, expand=1, fill=BOTH)

        ResultFrame.RecipeInfo = Text(self, state=DISABLED)
        ResultFrame.RecipeInfo.pack(side=TOP, fill=BOTH)

        ResultFrame.instructLabel = Label(self, text="Your list of recipes")
        ResultFrame.instructLabel.pack(anchor=N)

        ResultFrame.BackButton = Button(
            self, text="Back to options", command=rFrame)

        # Create list
        ResultFrame.myList = Listbox(window, font='Times 12')
        ResultFrame.myList.pack(side=TOP, expand=1, fill=BOTH)
        ResultFrame.myList.bind('<<ListboxSelect>>', self.expandRecipe)

        # Setup scroll bar
        ResultFrame.scroll = Scrollbar(window)
        ResultFrame.scroll.pack(side=RIGHT, fill=Y)

        # Link scroll option to listbox
        ResultFrame.myList.config(yscrollcommand=ResultFrame.scroll.set)
        ResultFrame.scroll.config(command=ResultFrame.myList.yview)

    def addRecipe(self, Recipe):
        ResultFrame.myList.insert(END,
                                  f"{Recipe.title}  |  Likes: {Recipe.likes}  |  Missing Ingredients: {Recipe.ingMiss}")

    def expandRecipe(self, event):
        # Runs if a recipe is selected
        if (ResultFrame.myList.curselection()):
            recipe = ControlFrame.Recipes[ResultFrame.myList.curselection()[0]]

            # TODO Check if this recipe is already displayed
            response = requests.get(
                f"https://api.spoonacular.com/recipes/{recipe.id}/information?apiKey={api_key}")
            responseJSON = response.json()
            ResultFrame.RecipeInfo.config(state=NORMAL)

            # Clear textbox
            ResultFrame.RecipeInfo.delete("1.0", END)
            summary = responseJSON["summary"]
            notyou = summary.replace("<b>", "").replace("<b>", "")
            ResultFrame.RecipeInfo.insert(END, f"{recipe.title}\n\n{notyou}")
            ResultFrame.formatSummary(self, summary, recipe)

    def formatSummary(self, summary, recipe):
        word_connect = re.finditer(r"<b>"(.+?) <\b >", summary)
        i = 0
        for found_word in word_connect:
            start = ResultFrame.RecipeInfo.index(f"1.0+{word_found.start()+len(recipe.title) + 2 - i*7} chars")")
            end=RecipeFrame.RecipeSum.index(
                f"1.0+{word_found.end()+len(recipe.title) + 2 - (i+1)*7} chars")
            ResultFrame.RecipeInfo.tag_add('bold', start, end)
            i += 1
            ResultFrame.RecipeInfo.tag_configure('bold', font = "Hlevetica 12")


##################################################################################
api_key="b29344da13414323bac320e823e7736a"
# The default size of the GUI is 800x600
WIDTH=800
HEIGHT=600

# Create the window
window=Tk()
window.title("Find A Recipe")
window.geometry(f"{WIDTH}x{HEIGHT}")
window.minsize(WIDTH, HEIGHT)

# Create the controls GUI as a Tkinter Frame inside the window
cFrame=ControlFrame(window)
cFrame.setupGUI()

# Create the recipe display frame inside the window
rFrame=ResultFrame(window)
rFrame.setupGUI()

# Wait for the window to close
window.mainloop()
