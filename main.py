from cProfile import label
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from random import random, choice, randint, shuffle
import json

upper_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
lower_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
final_password = ""
n_upper_letters = 0
n_lower_letters = 0
n_symbols = 0
n_numbers = 0

with open("directory_data.json", "a+") as direct_data:
    direct_data.seek(0)
    dir_data = direct_data.read()

def confirm_values(upper, lower, number, _symbol):
    global n_upper_letters
    global n_lower_letters
    global n_symbols
    global n_numbers
    global final_password
    n_upper_letters = int(upper)
    n_lower_letters = int(lower)
    n_symbols = int(_symbol)
    n_numbers = int(number)
    print(n_upper_letters)
    print(n_lower_letters)
    print(n_numbers)
    print(n_symbols)
    final_password = ""
    generate_password()
    password_window.destroy()
    third_entry.delete(0, END)
    third_entry.insert(0, final_password)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    global n_upper_letters
    global n_lower_letters
    global n_symbols
    global n_numbers
    total_string_sum = n_upper_letters + n_lower_letters + n_symbols + n_numbers
    selected_upper_letters = []
    selected_lower_letters = []
    selected_numbers = []
    selected_symbols = []
    final_password_list = []
    # getting required upper case letters
    for i in range(0, n_upper_letters):
        selected_upper_letters += choice(upper_letters)
    # getting required lower case letters
    for i in range(0, n_lower_letters):
        selected_lower_letters += choice(lower_letters)
    # getting required numbers
    for i in range(0, n_numbers):
        selected_numbers += choice(numbers)
    # getting required symbols
    for i in range(0, n_symbols):
        selected_symbols += choice(symbols)
    final_password_list = selected_upper_letters + selected_lower_letters + selected_numbers + selected_symbols
    shuffle(final_password_list)
    global final_password
    # place selected strings in random position
    for i in range(0, total_string_sum):
        final_password += final_password_list[i]

# ---------------------------- SAVE PASSWORD ------------------------------- #
final_directory = ""
def choose_directory():
    global final_directory
    global direct_data
    directory = filedialog.askdirectory()
    if directory:
        final_directory = f"{directory}/my_passwords.json"
        directory_entry.delete(0, END)
        directory_entry.insert(0, final_directory)
        with open("directory_data.json", "w+") as direct_data:
            direct_data.write(final_directory)

data_file = ""
def save_password():
    global final_directory
    global data_file
    web_name = first_entry.get()
    user_name = second_entry.get()
    password = third_entry.get()

    if final_directory:
        if web_name and user_name and password:
            is_ok = messagebox.askokcancel(title=f"{web_name}", message=f"These are the details that entered:\n"
                                                                f"Username: {user_name}\nPassword: {password}\n"
                                                                f"Is it OK to save?")
            if is_ok:
                try:
                    with open(final_directory, "r") as f:
                        data = json.load(f)
                        final_dict = {
                            f"{len(data.keys())}": {
                                "Website": web_name,
                                "Username": user_name,
                                "Password": password
                            }
                        }
                except FileNotFoundError:
                    data = {}
                    final_dict = {
                        f"{len(data.keys())}": {
                            "Website": web_name,
                            "Username": user_name,
                            "Password": password
                        }
                    }
                data.update(final_dict)
                with open(final_directory, "w") as f:
                    json.dump(data, f, indent=4)

        else:
            messagebox.showinfo(title="ERROR", message="Please complete all needed information first!")
    else:
        final_directory = dir_data
        if not dir_data:
            messagebox.showinfo(title="ERROR", message="Please complete all needed information first!")

# getting the passwords
def load_passwords():
    try:
        with open(dir_data, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("You don't have any saved passwords!")
    else:
        return data

# search a password
def search_passwords(website_name):
    try:
        with open(dir_data, "r") as f:
            data = json.load(f)
            for key in range(len(data.keys())):
                if data[f"{key}"]["Website"].lower() == website_name.lower():
                    found_pass_window = Tk()
                    found_pass_window.title("Password Found")
                    found_pass_window.config(padx=30, pady=30)

                    web_label = Label(found_pass_window, text="Website:")
                    web_label.grid(row=1, column=0)
                    web_entry = Entry(found_pass_window, width=30)
                    web_entry.insert(END, data[f"{key}"]["Website"])
                    web_entry.grid(row=1, column=1)
                    username_label = Label(found_pass_window, text="Username:")
                    username_label.grid(row=2, column=0)
                    username_entry = Entry(found_pass_window, width=30)
                    username_entry.insert(END, data[f"{key}"]["Username"])
                    username_entry.grid(row=2, column=1)
                    password_label = Label(found_pass_window, text="Password:")
                    password_label.grid(row=3, column=0)
                    password_entry = Entry(found_pass_window, width=30)
                    password_entry.insert(END, data[f"{key}"]["Password"])
                    password_entry.grid(row=3, column=1)
    except FileNotFoundError:
        messagebox.showinfo(title="ERROR", message="No saved password file found!")



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

w = 500 # width for the Tk root
h = 500 # height for the Tk root

# get screen width and height
ws = window.winfo_screenwidth() # width of the screen
hs = window.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen
# and where it is placed
window.geometry('%dx%d+%d+%d' % (w, h, x, y))


title_logo_canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_image = PhotoImage(file="just_logo.png")
title_logo_canvas.create_image(100, 100, image=logo_image)
title_logo_canvas.grid(row=0, column=1)


first_label = Label(text="Website:")
first_label.grid(row=1, column=0, pady=5)
second_label = Label(text="Email/Username:")
second_label.grid(row=2, column=0, pady=5)
third_label = Label(text="Password:")
third_label.grid(row=3, column=0, pady=5)


first_entry = Entry(width=50)
first_entry.grid(row=1, column=1, columnspan=2, pady=5)
first_entry.focus()
second_entry = Entry(width=50)
second_entry.insert(END, "example@example.com")
second_entry.grid(row=2, column=1, columnspan=2, pady=5)
third_entry = Entry(width=50)
third_entry.grid(row=3, column=1, columnspan=2, pady=5)

password_window = None
def generate_password_pressed():

    global password_window
    password_window = Tk()
    password_window.title("Generate Password")
    password_window.config(padx=50, pady=50)

    p_w = 300  # width for the Tk root
    p_h = 300  # height for the Tk root

    # get screen width and height
    p_ws = password_window.winfo_screenwidth()  # width of the screen
    p_hs = password_window.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the Tk root window
    p_x = (p_ws / 2) - (w / 2)
    p_y = (p_hs / 2) - (h / 2)

    # set the dimensions of the screen
    # and where it is placed
    password_window.geometry('%dx%d+%d+%d' % (p_w, p_h, p_x, p_y))

    upper_label = Label(password_window, text="How many upper-case letters?")
    upper_letter_box = Spinbox(password_window, width=5, from_=0, to=10)
    upper_label.grid(row=0, column=0, pady=5)
    upper_letter_box.grid(row=0, column=1, pady=5)

    lower_label = Label(password_window, text="How many lower-case letters?")
    lower_letter_box = Spinbox(password_window, width=5, from_=0, to=10)
    lower_label.grid(row=1, column=0, pady=5)
    lower_letter_box.grid(row=1, column=1, pady=5)

    number_label = Label(password_window, text="How many numbers?")
    number_box = Spinbox(password_window, width=5, from_=0, to=10)
    number_label.grid(row=2, column=0, pady=5)
    number_box.grid(row=2, column=1, pady=5)

    symbol_label = Label(password_window, text="How many symbols?")
    symbol_box = Spinbox(password_window, width=5, from_=0, to=10)
    symbol_label.grid(row=3, column=0, pady=5)
    symbol_box.grid(row=3, column=1, pady=5)

    confirm_button = Button(password_window,text="Confirm", bg="white",
                            command=lambda:confirm_values(upper_letter_box.get(),
                                                          lower_letter_box.get(),
                                                          number_box.get(),
                                                          symbol_box.get()))
    confirm_button.grid(row=4, column=1, pady=5)


directory_label = Label(text="Directory:")
directory_entry = Entry(width=37)
directory_entry.insert(0, dir_data)
directory_label.grid(row=4, column=0)
directory_entry.grid(row=4, column=1)
directory_button = Button(text="File", width=9, pady=0, bg="white", command=choose_directory)
directory_button.grid(row=4, column=2)


password_button = Button(text="Generate Password", width=32, bg="white", pady=0, command=generate_password_pressed)
password_button.grid(row=6, column=1, pady=5)

add_button = Button(text="Add", width=9, pady=0, bg="white", command=save_password)
add_button.grid(row=6, column=2, columnspan=2, pady=5)

def load_password_pressed():
    data = load_passwords()

    load_window = Tk()
    load_window.title("My Passwords")
    load_window.config(padx=20, pady=20)
    load_window.geometry('1040x600')
    page_title = Label(load_window, text="My Passwords", font=("Arial", 25, "bold"))
    page_title.pack(expand=True, fill=BOTH)

    main_frame = Frame(load_window)
    main_frame.pack(fill=BOTH, expand=1)
    # Configure the grid to allow the canvas to expand
    load_window.columnconfigure(0, weight=1)
    load_window.rowconfigure(0, weight=1)

    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    my_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    def on_mousewheel(event):
        my_canvas.yview_scroll(-1 * int(event.delta / 120), "units")
    my_canvas.bind_all('<MouseWheel>', on_mousewheel)

    second_frame = Frame(my_canvas)

    my_canvas.create_window((0,0), window=second_frame, anchor="nw")

    try:
        for i in range(len(data.keys()) + 1):
            for j in range(4):
                e = Entry(second_frame, width=20, fg="blue", font=('Arial', 16, 'bold'))
                e.grid(row=i+1, column=j)
                if j == 0:
                    e.insert(END, f"{i}")
                if i == 0 and j == 1:
                    e.insert(END, "Website")
                if i == 0 and j == 2:
                    e.insert(END, "Username")
                if i == 0 and j == 3:
                    e.insert(END, "Password")
                if j == 1 and i > 0:
                    e.insert(END, data[f"{i - 1}"]["Website"])
                if j == 2 and i > 0:
                    e.insert(END, data[f"{i - 1}"]["Username"])
                if j == 3 and i > 0:
                    e.insert(END, data[f"{i - 1}"]["Password"])
    except AttributeError:
        messagebox.showinfo(title="ERROR", message="You don't have any saved password file!")


load_button = Button(text="Load Passwords", width=43, bg="white", pady=0, command=load_password_pressed)
load_button.grid(row=7, column=1, columnspan=3, pady=1)

search_entry = Entry(width=37)
search_entry.insert(END, "Enter a website name")
search_entry.grid(row=5,column=1, pady=1)
search_button = Button(text="Search", width=9, pady=0, bg="white", command=lambda: search_passwords(search_entry.get()))
search_button.grid(row=5, column=2, pady=3)


mainloop()