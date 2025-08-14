import tkinter as tk
from tkinter import PhotoImage
import math
import re
#__________________________________________
is_deg = True # True = DEG, False = RAD



window = tk.Tk()
window.title("Scientific Calculator +")
window.resizable(False, False)
window.iconphoto(False, PhotoImage(file=r'D:/TepNguoiDung/DoAnThucTap/calculator_icon.png'))

operator = ""
text_input = tk.StringVar()
memory_val = None
is_light = True  # theme
#------------------------Giao Diện------------------------
def apply_theme():
    bg = "#f6f8fa" if is_light else "#0f172a"
    fg = "#111827" if is_light else "#e5e7eb"
    btn_bg = "powder blue" if is_light else "#1f2937"
    entry_bg = "#e7fbff" if is_light else "#0b2530"
    window.configure(bg=bg)
    txtDisplay.configure(bg=entry_bg, fg=fg)
    hist_label.configure(bg=bg, fg=fg) # hist label sẽ tạo sau, đây là hàm lưu lịch sử tính toán
    for b in all_buttons:
        try:
            b.configure(bg=btn_bg, fg="black" if is_light else "#f3f4f6", activebackground=btn_bg)
        except tk.TclError:
            pass
    history_list.configure(bg="#ffffff" if is_light else "#111827", fg="#111827" if is_light else "#e5e7eb", #history_list sẽ tạo sau, đây là hàm lưu lịch sử tính toán
                           highlightthickness=1, selectbackground="#93c5fd" if is_light else "#334155")

def toggle_theme():
    global is_light
    is_light = not is_light
    themeBtn.config(text="Light" if is_light else "Dark")
    apply_theme()

#-----------------------Hiển thị-----------------------
txtDisplay = tk.Entry(
    window, font=('arial', 20, 'bold'), textvariable=text_input,
    bd=12, insertwidth=4, width=26, borderwidth=4, justify='right'
)
txtDisplay.grid(row=0, column=0, columnspan=7, padx=6, pady=6, sticky="we")
#-----------------------Hàm hỗ trợ-----------------------
""" Hàm chuyển đổi giữa độ đo góc radian và độ đo góc độ """
def btnToggleDegRad():
    global is_deg
    is_deg = not is_deg
    degBtn.config(text="DEG" if is_deg else "RAD")

""" Chuyển đổi '^' thành '**' và thêm token vào biểu thức """
def btnClick(token):
    global operator
    if token == '^':
        token = '**'
    operator += str(token)
    text_input.set(operator)

""" Xóa toàn bộ biểu thức """
def btnClear():
    global operator
    operator = ""
    text_input.set("")

""" Xóa ký tự cuối cùng trong biểu thức """
def btnBackspace():
    global operator
    operator = operator[:-1]
    text_input.set(operator)
#----------------------Tạo nút----------------------
all_buttons = []

def make_btn(text, r, c, cmd=None, colspan=1, rowspan=1):
    b = tk.Button(
        window, padx=14, pady=10, bd=4,
        font=('arial', 14, 'bold'), text=text,
        command=cmd if cmd else (lambda t=text: btnClick(t))
    )
    b.grid(row=r, column=c, columnspan=colspan, rowspan=rowspan, padx=3, pady=3, sticky="nsew")
    all_buttons.append(b)
    return b
make_btn("sin(", 1, 0)
make_btn("cos(", 1, 1)
make_btn("tan(", 1, 2)
make_btn("log(", 1, 3)
degBtn  = make_btn("DEG", 1, 4, cmd=btnToggleDegRad)
make_btn("cbrt(", 1, 5)
themeBtn= make_btn("Light", 1, 6, cmd=toggle_theme)

# Row 2: sinh, cosh, tanh, log10, exp, sqrt, ^
make_btn("sinh(", 2, 0)
make_btn("cosh(", 2, 1)
make_btn("tanh(", 2, 2)
make_btn("log10(", 2, 3)
make_btn("exp(", 2, 4)
make_btn("sqrt(", 2, 5)
make_btn("^", 2, 6)

# Row 3: 7, 8, 9, *, /, ⌫,%
make_btn("7", 3, 0)
make_btn("8", 3, 1)
make_btn("9", 3, 2)
make_btn("*", 3, 3)
make_btn("/",    3, 4)
make_btn("⌫",    3, 5, cmd=btnBackspace())
make_btn("%", 3, 6, cmd=((hàm áp dụng phần trăm trực tiếp)))

# Row 4: 4, 5, 6, +, -, AC, 1/x
make_btn("4", 4, 0)
make_btn("5", 4, 1)
make_btn("6", 4, 2)
make_btn("+", 4, 3)
make_btn("-", 4, 4)
make_btn("AC",   4, 5, cmd=btnClear())
make_btn("1/x", 4, 6, cmd=((Hàm áp dụng nghịch đảo)))

# Row 5: 1, 2, 3, (, ), MC, MR
make_btn("1", 5, 0)
make_btn("2", 5, 1)
make_btn("3", 5, 2)
make_btn("(",    5, 3)
make_btn(")",    5, 4)
make_btn("MC", 5, 5, cmd=((hàm xóa giá trị bộ nhớ)))
make_btn("MR", 5, 6, cmd=((hàm gọi lại giá trị bộ nhớ)))

# Row 6: 0, ., e, =, M+, pi
make_btn("0", 6, 0)
make_btn(".", 6, 1)
make_btn("e",  6, 2)
make_btn("=",  6, 3, cmd=((hàm tạo nút =)), colspan=2)
make_btn("M+", 6, 5, cmd=((hàm thêm giá trị vào bộ nhớ)))
make_btn("pi", 6, 6)

window.mainloop()
