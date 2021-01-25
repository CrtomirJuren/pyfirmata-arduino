from tkinter import *
from PIL import ImageTk, Image


class GameScreen:
    def __init__(self, master):
        # create all of the main containers
        top_left = Frame(master, bg='black', width=200, height=200)
        top_middle = Frame(master, bg='green', width=200, height=200)
        top_right = Frame(master, bg="green", width=200, height=200)
        middle_left = Frame(master, bg='green', width=200, height=200)
        middle = Frame(master, bg='green', width=200, height=200)
        middle_right = Frame(master, bg='green', width=200, height=200)
        bottom_left = Frame(master, bg='green', width=200, height=200)
        bottom_middle = Frame(master, bg='green', width=200, height=200)
        bottom_right = Frame(master, bg='green', width=200, height=200)

        # layout all of the main containers
        top_left.grid(row=0, column=0, padx=0, pady=0)
        top_middle.grid(row=0, column=1)
        top_right.grid(row=0, column=2)
        middle_left.grid(row=1, column=0)
        middle.grid(row=1, column=1)
        middle_right.grid(row=1, column=2)
        bottom_left.grid(row=2, column=0)
        bottom_middle.grid(row=2, column=1)
        bottom_right.grid(row=2, column=2)

        # create a canvas to show image on
        canvas_for_image = Canvas(top_left, bg='black', height=390, width=577, borderwidth=2, highlightthickness=0)
        canvas_for_image.grid(row=0, column=0, sticky='nesw', padx=0, pady=0)

        # ration 1,5

        # create image from image location resize it to 200X200 and put in on canvas
        image = Image.open('arduino-v2.jpg').rotate(90)
        canvas_for_image.image = ImageTk.PhotoImage(image.resize((300, 200), Image.ANTIALIAS))
        canvas_for_image.create_image(10, 10, image=canvas_for_image.image, anchor='nw') #anchor='nw'


root = Tk()
root.title("RPG Game")
root.geometry("600x600")
display = GameScreen(root)

root.mainloop()