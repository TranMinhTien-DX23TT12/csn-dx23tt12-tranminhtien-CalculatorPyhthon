import tkinter as tk
import math
import re
from tkinter import PhotoImage

# ===================== Eval Helpers & Environment =====================
# Angle mode: True = DEG, False = RAD
is_deg = True

def _to_angle(x):
    return math.radians(x) if is_deg else x

def sin(x):  return math.sin(_to_angle(x))
def cos(x):  return math.cos(_to_angle(x))
def tan(x):  return math.tan(_to_angle(x))

def sinh(x): return math.sinh(_to_angle(x))
def cosh(x): return math.cosh(_to_angle(x))
def tanh(x): return math.tanh(_to_angle(x))

def log(x):    return math.log(x)     # ln
def log10(x):  return math.log10(x)
def exp(x):    return math.exp(x)
def sqrt(x):   return math.sqrt(x)
def pow_(a,b): return math.pow(a,b)
def cbrt(x): return x ** (1/3)
EVAL_ENV = {
    "__builtins__": None,
    "pi": math.pi,
    "e": math.e,
    "sin": sin, "cos": cos, "tan": tan,
    "sinh": sinh, "cosh": cosh, "tanh": tanh,
    "log": log, "log10": log10, "exp": exp, "sqrt": sqrt, "cbrt": cbrt,
}

# ===================== App =====================
window = tk.Tk()
window.title("Scientific Calculator +")
window.resizable(False, False)
window.iconphoto(False, PhotoImage(file=r'D:/TepNguoiDung/DoAnThucTap/calculator_icon.png'))

operator = ""
text_input = tk.StringVar()
memory_val = None
is_light = True  # theme

# --------------------- Theme ---------------------
def apply_theme():
    bg = "#f6f8fa" if is_light else "#0f172a"
    fg = "#111827" if is_light else "#e5e7eb"
    btn_bg = "powder blue" if is_light else "#1f2937"
    entry_bg = "#e7fbff" if is_light else "#0b2530"
    window.configure(bg=bg)
    txtDisplay.configure(bg=entry_bg, fg=fg)
    hist_label.configure(bg=bg, fg=fg)
    for b in all_buttons:
        try:
            b.configure(bg=btn_bg, fg="black" if is_light else "#f3f4f6", activebackground=btn_bg)
        except tk.TclError:
            pass
    history_list.configure(bg="#ffffff" if is_light else "#111827", fg="#111827" if is_light else "#e5e7eb",
                           highlightthickness=1, selectbackground="#93c5fd" if is_light else "#334155")

def toggle_theme():
    global is_light
    is_light = not is_light
    themeBtn.config(text="Light" if is_light else "Dark")
    apply_theme()

# --------------------- Display ---------------------
txtDisplay = tk.Entry(
    window, font=('arial', 20, 'bold'), textvariable=text_input,
    bd=12, insertwidth=4, width=26, borderwidth=4, justify='right'
)
txtDisplay.grid(row=0, column=0, columnspan=7, padx=6, pady=6, sticky="we")

# --------------------- Helpers ---------------------
def btnClick(token):
    """Append token to expression; convert '^' to '**'."""
    global operator
    if token == '^':
        token = '**'
    operator += str(token)
    text_input.set(operator)

def btnClear():
    global operator
    operator = ""
    text_input.set("")

def btnBackspace():
    global operator
    operator = operator[:-1]
    text_input.set(operator)

def btnToggleDegRad():
    global is_deg
    is_deg = not is_deg
    degBtn.config(text="DEG" if is_deg else "RAD")

def _preprocess(expr: str) -> str:
    # Replace percent like 50% -> (50/100)
    expr = re.sub(r'(?<!\w)(\d+(\.\d+)?)%', r'(\1/100)', expr)
    return expr

def btnEquals(event=None):
    global operator
    expr = operator.strip()
    if not expr:
        return
    try:
        expr2 = _preprocess(expr)
        result = eval(expr2, EVAL_ENV, {})
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        text_input.set(str(result))
        add_history(f"{expr} = {result}")
        operator = str(result)
    except Exception:
        text_input.set("Error")
        operator = ""

def get_current_number_span(s):
    """Return (start, end) indices of trailing number in s, or None."""
    m = re.search(r'(\d+(\.\d+)?)\s*$', s)
    if not m: return None
    return (m.start(1), m.end(1))

def apply_percent_inline():
    """Transform trailing number N to (N/100)."""
    global operator
    span = get_current_number_span(operator)
    if span:
        i, j = span
        num = operator[i:j]
        operator = operator[:i] + f"({num}/100)" + operator[j:]
    else:
        operator += "(/100)"
    text_input.set(operator)

def apply_reciprocal():
    """Wrap last number or parenthesized term as 1/(term)."""
    global operator
    s = operator.rstrip()
    if not s:
        return
    # If ends with ')', try to find matching '('
    if s.endswith(')'):
        depth = 0
        for idx in range(len(s)-1, -1, -1):
            if s[idx] == ')': depth += 1
            elif s[idx] == '(':
                depth -= 1
                if depth == 0:
                    operator = s[:idx] + "1/(" + s[idx+1:-1] + ")"
                    text_input.set(operator)
                    return
        # fallback – just prepend 1/(
        operator = "1/(" + operator + ")"
    else:
        span = get_current_number_span(s)
        if span:
            i, j = span
            operator = s[:i] + "1/(" + s[i:j] + ")" + s[j:]
        else:
            operator = "1/(" + s + ")"
    text_input.set(operator)

# --------------------- Memory ---------------------
def mem_add():
    """M+: add current display value to memory (or set if None)."""
    global memory_val
    try:
        val = float(text_input.get())
        if memory_val is None:
            memory_val = val
        else:
            memory_val += val
        mem_label.config(text=f"M={memory_val:g}")
    except Exception:
        pass

def mem_recall():
    """MR: insert memory value into expression."""
    global operator
    if memory_val is None:
        return
    # do not add extra decimals if integer
    if float(memory_val).is_integer():
        token = str(int(memory_val))
    else:
        token = str(memory_val)
    operator += token
    text_input.set(operator)

def mem_clear():
    """MC: clear memory."""
    global memory_val
    memory_val = None
    mem_label.config(text="M=—")

# --------------------- History ---------------------
history = []

def add_history(item: str):
    history.append(item)
    history_list.insert(tk.END, item)
    history_list.yview_moveto(1.0)

def history_double_click(event):
    # On double click, paste the result part into expression
    sel = history_list.curselection()
    if not sel: return
    item = history_list.get(sel[0])
    if " = " in item:
        expr, res = item.rsplit(" = ", 1)
        paste_result = res.strip()
        global operator
        operator += paste_result
        text_input.set(operator)

# --------------------- Button Factory ---------------------
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

# --------------------- Layout ---------------------
# Row 1: sin, cos, tan, log, DEG/RAD, pow, light/dark theme
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
make_btn("⌫",    3, 5, cmd=btnBackspace)
make_btn("%", 3, 6, cmd=apply_percent_inline)

# Row 4: 4, 5, 6, +, -, AC, 1/x
make_btn("4", 4, 0)
make_btn("5", 4, 1)
make_btn("6", 4, 2)
make_btn("+", 4, 3)
make_btn("-", 4, 4)
make_btn("AC",   4, 5, cmd=btnClear)
make_btn("1/x", 4, 6, cmd=apply_reciprocal)

# Row 5: 1, 2, 3, (, ), MC, MR
make_btn("1", 5, 0)
make_btn("2", 5, 1)
make_btn("3", 5, 2)
make_btn("(",    5, 3)
make_btn(")",    5, 4)
make_btn("MC", 5, 5, cmd=mem_clear)
make_btn("MR", 5, 6, cmd=mem_recall)

# Row 6: 0, ., e, =, M+, pi
make_btn("0", 6, 0)
make_btn(".", 6, 1)
make_btn("e",  6, 2)
make_btn("=",  6, 3, cmd=btnEquals, colspan=2)
make_btn("M+", 6, 5, cmd=mem_add)
make_btn("pi", 6, 6)






# History label and list
hist_label = tk.Label(window, text="History (double-click to paste result):", font=('arial', 11))
hist_label.grid(row=7, column=0, columnspan=7, sticky='w', padx=8, pady=(8,0))
history_list = tk.Listbox(window, height=6)
history_list.grid(row=8, column=0, columnspan=7, padx=6, pady=(0,8), sticky="we")
history_list.bind("<Double-Button-1>", history_double_click)

# Memory indicator
mem_label = tk.Label(window, text="M=—", font=('arial', 11))
mem_label.grid(row=9, column=0, columnspan=7, sticky='w', padx=8, pady=(0,8))

# Keyboard: Enter to evaluate
window.bind("<Return>", btnEquals)

# Apply initial theme
apply_theme()

window.mainloop()
