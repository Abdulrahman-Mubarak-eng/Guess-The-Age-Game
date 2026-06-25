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

# --- الإعدادات الافتراضية والمتغيرات العامة ---
MAX_AGE_DEFAULT = 100
MIN_AGE_DEFAULT = 1

max_age = MAX_AGE_DEFAULT
min_age = MIN_AGE_DEFAULT
repetition = 0
age = (max_age + min_age) // 2


# --- الدوال والمنطق (Logic & Functions) ---

def change_mode():
    """تبديل المظهر بين الوضع الداكن والفاتح وحفظ الإعداد."""
    if get_appearance_mode() == "Dark":
        set_appearance_mode("Light")
        mode_button.configure(text="Dark mode")
        guessing_label.configure(text_color="Black")
        with open("mode.txt", "w") as file:
            file.write("Light")
    else:
        set_appearance_mode("Dark")
        guessing_label.configure(text_color="White")
        with open("mode.txt", "w") as file:
            file.write("Dark")
        mode_button.configure(text="Light mode")


def open_github_profile():
    """فتح رابط الملف الشخصي للمطور."""
    webbrowser.open_new("https://abdulrahman-mubarak-eng.github.io/my-portfolio/")


def disable_buttons():
    """تعطيل أزرار التحكم عند انتهاء اللعبة أو حدوث تناقض."""
    button_more.configure(state="disabled")
    button_less.configure(state="disabled")
    button_equal.configure(state="disabled")


def reset_game():
    """إعادة تعيين اللعبة إلى حالتها الأولى."""
    global max_age, min_age, repetition, age
    
    # مسح سجل المحاولات
    for widget in record_frame.winfo_children():
        widget.destroy()
        
    max_age = MAX_AGE_DEFAULT
    min_age = MIN_AGE_DEFAULT
    repetition = 0
    age = (max_age + min_age) // 2

    # تفعيل الأزرار مجدداً
    button_more.configure(state="normal")
    button_less.configure(state="normal")
    button_equal.configure(state="normal")

    default_color = "black" if get_appearance_mode() == "Light" else "white"
    guessing_label.configure(text=f"Is your age {age}?", text_color=default_color)


def more():
    """التعامل مع خيار (العمر أكبر)."""
    global min_age, age, repetition
    min_age = age + 1
    
    if min_age > max_age:
        guessing_label.configure(
            text="Impossible! Your answers are contradictory 🤨",
            text_color="Red",
        )
        disable_buttons()
        return
        
    repetition += 1
    label = CTkLabel(
        record_frame,
        width=500,
        height=30,
        corner_radius=8,
        text=f"🎯 Attempt {repetition} → {age} (Too Low)",
        text_color="White",
        font=("Arial", 15),
        fg_color="#2336E4",
    )
    label.pack(pady=10)
    
    age = (max_age + min_age) // 2
    guessing_label.configure(text=f"Is your age {age}?")


def less():
    """التعامل مع خيار (العمر أصغر)."""
    global max_age, age, repetition
    max_age = age - 1
    
    if min_age > max_age:
        guessing_label.configure(
            text="Impossible! Your answers are contradictory 🤨",
            text_color="Red",
        )
        disable_buttons()
        return
        
    repetition += 1
    label = CTkLabel(
        record_frame,
        width=500,
        height=30,
        corner_radius=8,
        text=f"🎯 Attempt {repetition} → {age} (Too High)",
        text_color="White",
        font=("Arial", 15),
        fg_color="#2336E4",
    )
    label.pack(pady=10)
    
    age = (max_age + min_age) // 2
    guessing_label.configure(text=f"Is your age {age}?")


def equal():
    """التعامل مع خيار (العمر صحيح)."""
    global repetition
    repetition += 1
    
    label = CTkLabel(
        record_frame,
        width=500,
        height=30,
        corner_radius=8,
        text=f"🎯 Attempt {repetition} → {age} (Correct ✅)",
        text_color="White",
        font=("Arial", 15),
        fg_color="#16A34A",
    )
    label.pack(pady=10)
    
    guessing_label.configure(text=f"Your age is {age}", text_color="Green")
    disable_buttons()


def toggle_fullscreen(event=None):
    """التبديل بين وضع ملء الشاشة والوضع العادي."""
    if event and root.attributes("-fullscreen"):
        root.attributes("-fullscreen", False)
    else:
        root.attributes("-fullscreen", True)


# --- بناء الواجهة الرسومية (GUI Setup) ---

root = CTk()
root.title("Guess the age")
root.attributes("-fullscreen", True)
root.bind("<Escape>", toggle_fullscreen)
root.minsize(800,600)

# محاولة تحميل الأيقونة
try:
    root.iconbitmap("Guess the age icon.ico")
except Exception:
    pass

# قراءة وحفظ وضع المظهر المفضل
try:
    with open("mode.txt", "r") as file:
        saved_mode = file.read().strip()
        set_appearance_mode(saved_mode)
except FileNotFoundError:
    set_appearance_mode("Dark")

# 1. إنشاء شريط علوي (Top Bar) خاص بالأزرار لحمايتها من الاختفاء
top_bar = CTkFrame(root, fg_color="transparent", height=50)
top_bar.pack(fill="x", padx=20, pady=(10, 0))

# زر المظهر وزر الشاشة الكاملة داخل الشريط العلوي المخصص
mode_button_text = "Light mode" if get_appearance_mode() == "Dark" else "Dark mode"
mode_button = CTkButton(top_bar, text=mode_button_text, command=change_mode)
mode_button.pack(side="left")

fullscreen_button = CTkButton(top_bar, text="Fill Screen", command=lambda: toggle_fullscreen(True))
fullscreen_button.pack(side="right")

# 2. الإطار الرئيسي القابل للتمرير لمحتويات اللعبة (يبدأ الآن أسفل الأزرار)
home_scroll_frame = CTkScrollableFrame(root, corner_radius=20, fg_color=root.cget("fg_color"))
home_scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)

# العناوين ونصوص العرض
CTkLabel(home_scroll_frame, text="🎯 Guess The Age", font=("Arial", 30, "bold")).pack(pady=10)
CTkLabel(home_scroll_frame, text="Think of an age between 1 and 100", font=("Arial", 20)).pack(pady=10)

guessing_label = CTkLabel(home_scroll_frame, text=f"Is your age {age}?", font=("Arial", 25, "bold"))
guessing_label.pack(pady=10)

# إطار أزرار التخمين (أكبر، أصغر، يساوي)
buttons_frame = CTkFrame(home_scroll_frame, width=1001, height=100, corner_radius=20)
buttons_frame.pack(pady=10)

button_more = CTkButton(
    buttons_frame, width=100, height=50, text="⬆ Higher", corner_radius=20,
    hover_color="#1D4ED8", fg_color="#2563EB", text_color="white", font=("Arial", 20),
    command=more
)
button_more.grid(row=0, column=0, padx=10)

button_equal = CTkButton(
    buttons_frame, width=100, height=50, text="✅ Correct", corner_radius=20,
    hover_color="#D8D825", fg_color="#D8C413", text_color="white", font=("Arial", 20),
    command=equal
)
button_equal.grid(row=0, column=1, padx=10)

button_less = CTkButton(
    buttons_frame, width=100, height=50, text="⬇ Lower", corner_radius=20,
    hover_color="#B91C1C", fg_color="#DC2626", text_color="white", font=("Arial", 20),
    command=less
)
button_less.grid(row=0, column=2, padx=10)

# سجل المحاولات وإعادة التشغيل
CTkLabel(home_scroll_frame, text="Guessing record:", font=("Arial", 20)).pack(pady=10)

record_frame = CTkScrollableFrame(home_scroll_frame, width=550, height=25, corner_radius=20)
record_frame.pack(pady=10)

CTkButton(
    home_scroll_frame, width=100, height=40, text="🔄 Restart", corner_radius=20,
    hover_color="#D97706", fg_color="#F59E0B", text_color="white", font=("Arial", 20),
    command=reset_game
).pack(pady=10)

# إطار الحقوق في الأسفل
links_frame = CTkFrame(root, fg_color="transparent")
links_frame.pack(side="bottom", pady=20)

link_label = CTkLabel(
    links_frame,
    text="© 2026 Abdulrahman Mubarak. All rights reserved.",
    text_color="#1f74ff",
    font=("Arial", 13, "underline"),
    cursor="hand2",
)
link_label.grid(row=0, column=1, padx=10, pady=5)
link_label.bind("<Button-1>", lambda e: open_github_profile())

# تشغيل التطبيق
root.mainloop()
