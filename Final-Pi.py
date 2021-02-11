from tkinter import *
import re
import requests
import ImageTk
from io import BytesIO
from PIL import Image
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
        # Enter ingredients' label
        ControlFrame.instructLabel = Label(
            window, text="Enter Some Ingredients", font='verdana 15')
        ControlFrame.instructLabel.pack(anchor=N)

        # Creates the Textbox
        ControlFrame.user_input = Entry(
            window, bg="white", font='kristen 16')
        # Binds enter key to process input from user
        ControlFrame.user_input.bind('<Return>', self.process)
        ControlFrame.user_input.pack(side=TOP, fill=X, pady=5)
        # Cursor is set('focused') on the Textbox
        ControlFrame.user_input.focus()

        # Makes the frame the size of the window
        self.pack(side=TOP, expand=1, fill=BOTH)

        # Creates 'How Many Re..' label
        ControlFrame.resultAmntL = Label(
            self, font="helvetica 14", text="How Many Recipes?")
        ControlFrame.resultAmntL.grid(column=0, row=0)
        # Creates input box
        ControlFrame.resultAmnt = Entry(
            self, bg="white", font="helvetica 14", width=3)
        ControlFrame.resultAmnt.insert(0, "5")
        ControlFrame.resultAmnt.grid(column=1, row=0)

    def process(self, event):
        # Take the input from the input line and sets them all to lower case
        action = ControlFrame.user_input.get().lower()
        # No two word ingredients (e.g. rice cakes = rice, cakes)
        ingredients = action.split()

        # Sets response to the retrieved recipes from the website
        response = requests.get(
            f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={','.join(ingredients)}&number={ControlFrame.resultAmnt.get()}")
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
                text="Enter Ingredients", fg="black", font="helvetica 15")

        # list of recipes
        ControlFrame.Recipes = [Recipe(recipeJSON)
                                for recipeJSON in responseJSON]

        # Adds recipes to the list
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
        self.missedIng = []

        i = 0
        for ing in recipeJSON["missedIngredients"]:
            if (ing["name"] not in self.missedIng):
                self.missedIng.append(ing["name"])
            else:
                i += 1
        self.ingMissCnt = recipeJSON["missedIngredientCount"] - i

    def __str__(self):
        return self.title


class ResultFrame(Frame):
    def __init__(self, parent):
        # Call the constructor in the superclass
        Frame.__init__(self, parent)

    # View recipe options
    def listReicpes(Frame):
        rFrame.pack_forget()
        cFrame.pack(side=TOP, expand=1, fill=BOTH)
        ResultFrame.bottomFrame.pack_forget()
        ResultFrame.bottomFrame.pack(side=TOP, fill=X)

    def setupGUI(self):
        # Builds bottom frame
        ResultFrame.bottomFrame = Frame(window)
        ResultFrame.bottomFrame.pack(side=TOP, fill=X)

        ResultFrame.instructLabel = Label(
            ResultFrame.bottomFrame, text="Your list of recipes")
        ResultFrame.instructLabel.pack(side=LEFT, pady=6)

        # Adds back button
        ResultFrame.instructLabel = Button(ResultFrame.bottomFrame, text="Back", font="helvetica 10", command=rFrame.listReicpes())
        ResultFrame.instructLabel.pack(anchor=E, side=RIGHT, pady=6)

        ResultFrame.recipeInfo = Text(
            self, state=DISABLED, wrap=WORD, font='helvetica', height=10, width=40)

        ResultFrame.img = Label(self, height=0, width=0)

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

        self.pack(side=TOP, expand=1, fill=BOTH)

    def addRecipe(self, Recipe):
        ResultFrame.myList.insert(END,
                                  f"{Recipe.title}  |  Likes: {Recipe.likes}  |  Missing Ingredients: {Recipe.ingUsed}")

    def expandRecipe(self, event):
        # Runs if a recipe is selected
        if (ResultFrame.myList.curselection()):
            recipe = ControlFrame.Recipes[ResultFrame.myList.curselection()[0]]

            # Disable controls
            cFrame.pack_forget()
            # pack the recipe frame
            rFrame.pack(side=TOP, expand=1, fill=BOTH)

            ResultFrame.recipeInfo.pack(
                anchor=N, side=RIGHT, fill=BOTH, expand=1)
            ResultFrame.img.pack(anchor=NW, fill=BOTH, side=TOP)
            ResultFrame.bottomFrame.pack_forget()
            ResultFrame.bottomFrame.pack(side=TOP, fill=BOTH, expand=1)
            ResultFrame.myList.pack_forget()
            ResultFrame.myList.pack(side=BOTTOM, expand=1, fill=BOTH)

            # Textbox editable
            ResultFrame.recipeInfo.config(state=NORMAL)
            ResultFrame.recipeInfo.delete("1.0", END)

            instruct = requests.get(
                f"https://api.spoonacular.com/recipes/{recipe.id}/analyzedInstructions?apiKey={api_key}")
            instructions = instruct.json()
            steplist = []
            for ins in instructions:
                instructionList = ins['steps']
                for steps in instructionList:
                    steplist.append(steps['step'])

            if (hasattr(ControlFrame.Recipes[ResultFrame.myList.curselection()[0]], "photo")):
                Rphoto = ControlFrame.Recipes[ResultFrame.myList.curselection()[
                    0]].photo
                ResultFrame.imgLabel.config(image=Rphoto)
                # RecipeFrame.RecipeSum.config(width=int((800 - Rphoto.width())/12.08))
            else:
                response = requests.get(recipe.img)
                image = Image.open(BytesIO(response.content)
                                   ).resize((312, 231))
                photo = ImageTk.PhotoImage(image)
                # save photo to og recipe object-
                ControlFrame.Recipes[ResultFrame.myList.curselection()[
                    0]].photo = photo
                ResultFrame.img.config(image=photo)

            if (len(recipe.missedIng) > 0):
                ingredients = ", ".join(recipe.missedIng)
                ResultFrame.recipeInfo.insert(
                    "1.0", f"Missing Ingredients: {ingredients}\n")

            if (len(steplist) > 0):
                recstep = ", ".join(steplist)
                # print (recstep)
                ResultFrame.recipeInfo.insert(END, f"Steps: {recstep}")
                ResultFrame.recipeInfo.config(state=DISABLED)

    def formatSummary(self, summary, recipe):
        word_connect = re.finditer(r"<b>(.+?) <\b >", summary)
        i = 0
        for found_word in word_connect:
            start = ResultFrame.RecipeInfo.index(
                f"1.0+{found_word.start()+len(recipe.title) + 2 - i*7} chars")
            end = ResultFrame.RecipeInfo.index(
                f"1.0+{found_word.end()+len(recipe.title) + 2 - (i+1)*7} chars")
            ResultFrame.RecipeInfo.tag_add('bold', start, end)
            i += 1
            ResultFrame.RecipeInfo.tag_configure('bold', font="Times 12")


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
rFrame = ResultFrame(window)
rFrame.setupGUI()

# Wait for the window to close
window.mainloop()
