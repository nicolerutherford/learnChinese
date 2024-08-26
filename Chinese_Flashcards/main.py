from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
WHITE = "#ffffff"
FONT_NAME = "Courier"
SUB_HEADING = (FONT_NAME, 40, "italic")
HEADING = (FONT_NAME, 80, "bold")
data_to_learn= {}
current_card = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/Chinese_words.csv")
    data_to_learn = original_data.to_dict(orient="records")
else:
    data_to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(data_to_learn)
    canvas.itemconfig(card_word, fill= "black", font=HEADING, text =current_card["characters"])
    canvas.itemconfig(card_title, fill= "black", font=SUB_HEADING, text=current_card["pinyin"])
    canvas.itemconfig(canvas_image, image= card_front)
    flip_timer = window.after(3000, func=flip_card)

def word_is_known():
    data_to_learn.remove(current_card)
    print(len(data_to_learn))
    data = pandas.DataFrame(data_to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

def flip_card():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(card_word, fill= WHITE, text=current_card["meaning"], font= (FONT_NAME, 25))
    canvas.itemconfig(card_title, fill= WHITE, text="English Meaning")

window = Tk()
window.title("Language App")
window.config(padx= 50, pady = 50, bg= BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front= PhotoImage(file="images/card_front.png")
card_back= PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness= 0)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="Title", fill="black", font=SUB_HEADING)
card_word = canvas.create_text(360, 240, text="Word", fill="black", font=HEADING)

tick_img = PhotoImage(file="images/right.png")
tick_button = Button(highlightthickness=0, image= tick_img, command = word_is_known)
tick_button.grid(column=0, row=1)

cross_img = PhotoImage(file="images/wrong.png")
cross_button = Button(image= cross_img, highlightthickness=0, command = next_card)
cross_button.grid(column=1, row=1)

next_card()

window.mainloop()

