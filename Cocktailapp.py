from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading

def fetch_cocktails():
    url = 'https://www.thecocktaildb.com/api/json/v1/1/filter.php?c=Cocktail'
    response = requests.get(url)
    data = response.json()
    return [drink['strDrink'] for drink in data.get('drinks', [])]

def fetch_details(cocktail_name):
    url = f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={cocktail_name}'
    response = requests.get(url)
    data = response.json()

    if 'drinks' in data and data['drinks']:
        drink = data['drinks'][0]
        instructions = drink['strInstructions']
        image_url = drink['strDrinkThumb']
        image_response = requests.get(image_url)
        image_data = Image.open(BytesIO(image_response.content))
        image = ImageTk.PhotoImage(image_data.resize((200, 200)))
        return instructions, image
    else:
        return "", None

def update_details(event):
    selected_index = cocktail_listbox.curselection()
    if selected_index:
        selected_cocktail = cocktail_list[selected_index[0]]
        if selected_cocktail not in details:
            fetch_and_update(selected_cocktail)
        else:
            update_ui(selected_cocktail)

def fetch_and_update(cocktail_name):
    def fetch():
        instructions, img = fetch_details(cocktail_name)
        details[cocktail_name] = (instructions, img)
        update_ui(cocktail_name)

    thread = threading.Thread(target=fetch)
    thread.start()

def update_ui(cocktail_name):
    instructions, img = details[cocktail_name]
    app_title.config(text="Cocktail Dictionary")
    drink_name.config(text=cocktail_name)
    instructions_text.config(state=NORMAL)
    instructions_text.delete(1.0, END)
    instructions_text.insert(END, instructions)
    instructions_text.config(state=DISABLED)
    cocktail_image.config(image=img, bg="#D6C2E9")
    cocktail_image.image = img

root = Tk()
root.title("Cocktail Dictionary")
root.geometry("1000x600")

main_frame = Frame(root, bg="#D6C2E9")
main_frame.pack(fill=BOTH, expand=True)

left_frame = Frame(main_frame, width=300, bg="#D5DBDB")
left_frame.pack(side=LEFT, fill=Y)

right_frame = Frame(main_frame, bg="#D6C2E9")
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

app_title = Label(right_frame, text="Cocktail Dictionary", font=("Arial", 28, "bold"), fg="#7D3C98", bg="#D6C2E9")
app_title.pack(pady=10)

drink_name = Label(right_frame, text="", font=("Arial", 20, "bold"), fg="black", bg="#D6C2E9")
drink_name.pack(pady=10)

image_frame = Frame(right_frame, bg="#D6C2E9", width=250, height=250)
image_frame.pack()

cocktail_image = Label(image_frame, bg="#D6C2E9")
cocktail_image.pack(padx=10, pady=10)

instructions_label = Label(right_frame, text="Instructions:", font=("Arial", 14, "bold"), fg="#17202A", bg="#D6C2E9")
instructions_label.pack()

instructions_text = Text(right_frame, wrap=WORD, height=8, width=50, fg="#17202A", font=("Arial", 12), bg="#D6C2E9")

scrollbar_text = Scrollbar(right_frame, command=instructions_text.yview)
instructions_text.configure(yscrollcommand=scrollbar_text.set)

instructions_label.pack(pady=5)
instructions_text.pack(pady=5, padx=10, side=LEFT, fill=BOTH, expand=True)
scrollbar_text.pack(side=RIGHT, fill=Y)

cocktail_listbox = Listbox(left_frame, width=35, height=15, selectbackground="#3498db", selectforeground="white", font=("Arial", 12, "bold"), activestyle="none")
cocktail_listbox.pack(side=LEFT, fill=Y)

scrollbar = Scrollbar(left_frame, orient=VERTICAL, command=cocktail_listbox.yview, troughcolor="#D5DBDB", bg="#3498db")
scrollbar.pack(side=RIGHT, fill=Y)
cocktail_listbox.config(yscrollcommand=scrollbar.set)

cocktail_list = fetch_cocktails()
details = {}

for name in cocktail_list:
    cocktail_listbox.insert(END, name)

cocktail_listbox.bind('<<ListboxSelect>>', update_details)

root.mainloop()
