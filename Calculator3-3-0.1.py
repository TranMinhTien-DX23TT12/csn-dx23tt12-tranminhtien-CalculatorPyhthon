import tkinter as tk
from tkinter import PhotoImage
window = tk.Tk()
window.title("Scientific Calculator +")
window.resizable(False, False)
window.iconphoto(False, PhotoImage(file=r'D:/TepNguoiDung/DoAnThucTap/calculator_icon.png'))

operator = ""
text_input = tk.StringVar()
memory_val = None
is_light = True  # theme


#----------------------Tạo nút----------------------
all_buttons = []

def make_btn(text, r, c, cmd=None, colspan=1, rowspan=1):
    b = tk.Button(
        window, padx=14, pady=10, bd=4,
        font=('arial', 14, 'bold'), text=text,
        command=cmd if cmd else (lambda t=text: (gọi tên hàm)(t))
    )
    b.grid(row=r, column=c, columnspan=colspan, rowspan=rowspan, padx=3, pady=3, sticky="nsew")
    all_buttons.append(b)
    return b
make_btn("sin(", 1, 0)
make_btn("cos(", 1, 1)
make_btn("tan(", 1, 2)
make_btn("log(", 1, 3)
degBtn  = make_btn("DEG", 1, 4, cmd=( hàm biến đổi giữa độ và radian ))
make_btn("cbrt(", 1, 5)
themeBtn= make_btn("Light", 1, 6, cmd=(Hàm chuyển đổi giữa chế độ sáng và tối))

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
make_btn("⌫",    3, 5, cmd=((Hàm xóa ký tự cuối cùng))
make_btn("%", 3, 6, cmd=((hàm áp dụng phần trăm trực tiếp)))

# Row 4: 4, 5, 6, +, -, AC, 1/x
make_btn("4", 4, 0)
make_btn("5", 4, 1)
make_btn("6", 4, 2)
make_btn("+", 4, 3)
make_btn("-", 4, 4)
make_btn("AC",   4, 5, cmd=((Hàm xóa toàn bộ)))
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
