import webbrowser
from customtkinter import (
    get_appearance_mode,
    set_appearance_mode,
    CTk,
    CTkLabel,
    CTkButton,
    CTkFrame,
    CTkScrollableFrame,
)
from flask import app

max_age = 100
min_age = 1
Repetition = 0
age = (max_age + min_age) // 2


def change_mode():
    if get_appearance_mode() == "Dark":
        set_appearance_mode("Light")
        mode_button.configure(text="Dark mode")
        Guessing.configure(text_color="Black")
        with open("mode.txt", "w") as file:
            file.write("Light")
    else:
        set_appearance_mode("Dark")
        Guessing.configure(text_color="White")
        with open("mode.txt", "w") as file:
            file.write("Dark")
        mode_button.configure(text="Light mode")


def open_itch_profile():
    webbrowser.open_new("https://abdulrahman-mubarak.itch.io")


def open_github_profile():
    webbrowser.open_new("https://github.com/Abdulrahman-Mubarak-eng")


def Reset():
    for widget in frame2.winfo_children():
        widget.destroy()
    global max_age, min_age, Repetition, age
    max_age = 100
    min_age = 1
    Repetition = 0
    age = (max_age + min_age) // 2

    BUTTUN_more.configure(state="normal")
    BUTTUN_less.configure(state="normal")
    BUTTUN_equal.configure(state="normal")

    # تحديد لون النص تلقائياً بناءً على الثيم الافتراضي لـ CustomTkinter دون تعارض
    default_color = "black" if get_appearance_mode() == "Light" else "white"
    Guessing.configure(text=f"Is your age {age}?", text_color=default_color)


def Disabling_the_buttons():
    BUTTUN_more.configure(state="disabled")
    BUTTUN_less.configure(state="disabled")
    BUTTUN_equal.configure(state="disabled")


def more():
    global min_age, age, Repetition
    min_age = age + 1
    if min_age > max_age:
        Guessing.configure(
            text="Impossible! Your answers are contradictory 🤨",
            text_color="Red",
        )
        Disabling_the_buttons()
        return
    Repetition += 1
    Lable = CTkLabel(
        frame2,
        500,
        30,
        corner_radius=8,
        text=f"🎯 Attempt {Repetition} → {age} (Too Low)",
        text_color="White",
        font=("Arial", 15),
        fg_color="#2336E4",
    )
    Lable.pack(pady=10)
    age = (max_age + min_age) // 2
    Guessing.configure(text=f"Is your age {age}?")


def less():
    global max_age, age, Repetition
    max_age = age - 1
    if min_age > max_age:
        Guessing.configure(
            text="Impossible! Your answers are contradictory 🤨",
            text_color="Red",
        )
        Disabling_the_buttons()
        return
    Repetition += 1
    Lable = CTkLabel(
        frame2,
        500,
        30,
        corner_radius=8,
        text=f"🎯 Attempt {Repetition} → {age} (Too High)",
        text_color="White",
        font=("Arial", 15),
        fg_color="#2336E4",
    )
    Lable.pack(pady=10)
    age = (max_age + min_age) // 2
    Guessing.configure(text=f"Is your age {age}?")


def equal():
    global Repetition
    Repetition += 1
    Lable = CTkLabel(
        frame2,
        500,
        30,
        corner_radius=8,
        text=f"🎯 Attempt {Repetition} → {age} (Correct ✅)",
        text_color="White",
        font=("Arial", 15),
        fg_color="#16A34A",
    )
    Lable.pack(pady=10)
    Guessing.configure(text=f"Your age is {age}", text_color="Green")
    Disabling_the_buttons()


# 🛠️ تصحيح الخطأ هنا: تم تغيير Home إلى Home2 لأن attributes تتبع النافذة الرئيسية وليس الفريم
def escape(event):
    Home2.attributes("-fullscreen", False)


Home2 = CTk()
Home2.title("Guess the age")
Home2.attributes("-fullscreen", True)
Home2.bind("<Escape>", escape)
Home2.iconbitmap("Guess the age icon.ico")



# ملاحظة: تأكد من وجود ملف الأيقونة في نفس مجلد السكربت حتى لا يظهر خطأ آخر
try:
    Home2.iconbitmap("Guess the age icon.ico")
except Exception:
    pass

Home = CTkScrollableFrame(Home2, corner_radius=20,fg_color=Home2.cget("fg_color"))
Home.pack(fill="both", expand=True, padx=20, pady=20)

try:
    with open("mode.txt", "r") as file:
        mode = file.read().strip()
        if mode == "Light":
            set_appearance_mode("Light")
        else:
            set_appearance_mode("Dark")
except FileNotFoundError:
    set_appearance_mode("Dark")

mode_button = CTkButton(Home2, text="Light mode", command=change_mode)
mode_button.place(x=10, y=10)

CTkLabel(Home, 100, 50, text="🎯 Guess The Age", font=("Arial", 30, "bold")).pack(
    pady=10
)

CTkLabel(
    Home, 100, 50, text="Think of an age between 1 and 100", font=("Arial", 20)
).pack(pady=10)

Guessing = CTkLabel(
    Home, 100, 50, text=f"Is your age {age}?", font=("Arial", 25, "bold")
)
Guessing.pack(pady=10)

frame = CTkFrame(Home, 1001, 100, corner_radius=20)
frame.pack(pady=10)

BUTTUN_more = CTkButton(
    frame,
    100,
    50,
    text="⬆ Higher",
    corner_radius=20,
    hover_color="#1D4ED8",
    fg_color="#2563EB",
    text_color="white",
    font=("Arial", 20),
    command=more,
)
BUTTUN_more.grid(row=0, column=0, padx=10)

BUTTUN_equal = CTkButton(
    frame,
    100,
    50,
    text="✅ Correct",
    corner_radius=20,
    hover_color="#D8D825",
    fg_color="#D8C413",
    text_color="white",
    font=("Arial", 20),
    command=equal,
)
BUTTUN_equal.grid(row=0, column=1, padx=10)

BUTTUN_less = CTkButton(
    frame,
    100,
    50,
    text="⬇ Lower",
    corner_radius=20,
    hover_color="#B91C1C",
    fg_color="#DC2626",
    text_color="white",
    font=("Arial", 20),
    command=less,
)
BUTTUN_less.grid(row=0, column=2, padx=10)

CTkLabel(Home, 100, 50, text="Guessing record:", font=("Arial", 20)).pack(
    pady=10
)
frame2 = CTkScrollableFrame(Home, 550, height=25, corner_radius=20)
frame2.pack(pady=10)

CTkButton(
    Home,
    100,
    40,
    text="🔄 Restart",
    corner_radius=20,
    hover_color="#D97706",
    fg_color="#F59E0B",
    text_color="white",
    font=("Arial", 20),
    command=Reset,
).pack(pady=10)

links_frame = CTkFrame(Home2, fg_color="transparent")
links_frame.pack(side="bottom", pady=20)

btn_more_games = CTkButton(
    links_frame,
    width=180,
    height=25,
    text="More Games & Apps 🚀",
    command=open_itch_profile,
    fg_color="#ff4b5c",
    hover_color="#e03e4d",
    font=("Arial", 14, "bold"),
)
btn_more_games.grid(row=0, column=0, padx=10, pady=5)

link_label = CTkLabel(
    links_frame,
    text="© 2026 Abdulrahman Mubarak. All rights reserved.",
    text_color="#1f74ff",
    font=("Arial", 13, "underline"),
    cursor="hand2",
)
link_label.grid(row=0, column=1, padx=10, pady=5)
link_label.bind("<Button-1>", lambda e: open_github_profile())

Home2.mainloop()