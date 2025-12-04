import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterweb import HtmlFrame
import markdown
import html
import re
import ctypes
import subprocess, sys, os
import json, traceback
from ToolTip import *

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

changed = False
current_file = None
filepath = None

win = tk.Tk()
ttk.Style().theme_use("winnative")
win.geometry("800x600")
win.minsize(700, 500)
win.grid_rowconfigure(1, weight=1)
win.grid_columnconfigure(0, weight=1)
win.grid_columnconfigure(1, weight=1)

def report_callback_exception(exc_type, exc_value, exc_traceback):
    tk_error_handler(exc_type, exc_value, exc_traceback)

win.report_callback_exception = report_callback_exception

configuration_file = "Configuration.json"

with open(configuration_file, "r", encoding="utf-8") as f:
    configuration = json.load(f)
        
show_tooltip = tk.BooleanVar(value=configuration["show_tooltip"])
language = tk.StringVar(value=configuration["language"])
auto_save = tk.BooleanVar(value=configuration["auto_save"])

menu_labels = {}
tab_labels = {}

def toolwindow(window):
    window.update_idletasks()
    hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
    
    GWL_STYLE = -16
    WS_MINIMIZEBOX = 0x00020000
    WS_MAXIMIZEBOX = 0x00010000
    
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
    
    style = style & ~WS_MINIMIZEBOX & ~WS_MAXIMIZEBOX
    
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
    
    ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 
                                      0x0002 | 0x0001 | 0x0004 | 0x0020 | 0x0010)
    
def tk_error_handler(exc_type, exc_value, exc_traceback):
    tb_text = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    errorwin = tk.Toplevel(win)
    errorwin.title("Hata")
    errorwin.resizable(False, False)
    errorwin.transient(win)
    errorwin.lift()
    errorwin.focus_force()
    toolwindow(errorwin)
    errorwin.grab_set()
    
    frame = tk.Frame(errorwin, bd=1, relief="raised")
    frame.pack(padx=20, pady=20, fill="both", expand=True)
    
    if language.get() == "türkçe":
        tk.Label(frame, text="Bir sorun oluştu: ").pack(anchor="nw", padx=5, pady=(5, 0))
    elif language.get() == "english":
        tk.Label(frame, text="An error occured: ").pack(anchor="nw", padx=5, pady=(5, 0))
    
    error = tk.Text(frame, bd=1, font=("Consolas", 10), width=50, height=20, wrap="none", padx=5, pady=5)
    error.insert(1.0, traceback.format_exc())
    error.config(state="disabled")
    
    scroll = tk.Scrollbar(frame, orient="vertical")
    scroll.pack(padx=(0, 5), pady=5, fill="y", side='right')
    scroll.config(command=error.yview)
    
    scroll2 = tk.Scrollbar(frame, orient="horizontal")
    scroll2.pack(padx=5, pady=(0, 5), fill="x", side='bottom')
    scroll2.config(command=error.xview)
    
    error.config(yscrollcommand=scroll.set)
    error.config(xscrollcommand=scroll2.set)
    error.pack(padx=(5, 0), pady=(5, 0), fill="both", expand=True)
    
    frame2 = tk.Frame(errorwin, bd=1, relief="raised")
    frame2.pack(padx=20, pady=(0, 20))
    
    def copy_error():
         error_content = error.get("1.0", "end-1c")
         error.clipboard_clear()
         error.clipboard_append(error_content)
         cp.config(state="disabled")
    
    ok = tk.Button(frame2, text="Tamam", bd=1, command=lambda: errorwin.destroy(), width=30)
    ok.pack(padx=5, pady=5, side="right")
    cp = tk.Button(frame2, text="Kopyala", bd=1, command=copy_error, width=30)
    cp.pack(padx=(5, 0), pady=5, side="left")
    
    if language.get() == "türkçe":
        ok.config(text="Tamam")
        cp.config(text="Kopyala")
    elif language.get() == "english":
        ok.config(text="Ok")
        cp.config(text="Copy")

if hasattr(sys, "_MEIPASS"):
    icon_path = os.path.join(sys._MEIPASS, "Icon.ico")
else:
    icon_path = os.path.join(os.path.dirname(__file__), "Icon.ico")

if os.path.exists(icon_path):
    win.iconbitmap(icon_path)

CSS_STYLE = """
<style>
body {
    font-family: 'Clear Sans', sans-serif;
    background-color: #ffffff;
    color: #000;
    margin: 20px;
    line-height: 1.6;
    font-size: 17px;
}
h1 {
    color: #0080ff;
    padding-bottom: 5px;
    margin-top: 20px;
    border-bottom: 2px solid black;
}
h2 {
    color: #0080ff;
    padding-bottom: 4px;
    margin-top: 20px;
    border-bottom: 2px solid black;
    display: inline-block;
}
h3 {
    color: #000000;
    padding-bottom: 3px;
    margin-top: 20px;
}
h4 {
    color: #404040;
    padding-bottom: 2px;
    margin-top: 20px;
}
h5 {
    color: #404040;
    padding-bottom: 1px;
    margin-top: 20px;
}
h6 {
    color: #404040;
    padding-bottom: 1px;
    margin-top: 20px;
}
/* Kod bloğu genel */
pre code {
    display: block;
    padding: 8px 10px;
    white-space: pre-wrap;
    word-wrap: break-word;
    font-family: Consolas, monospace;
    font-size: 17px;
    border-bottom: 2px solid black;
    padding-bottom: 5px;
}

body code {
    padding: 2px 5px;
    font-family: Consolas, monospace;
    white-space: pre;
    font-size: 17px;
    border-bottom: 2px solid black;
    padding-bottom: 5px;
}

/* Pygments tarafından oluşturulan sınıflar */
.codehilite .hll { background-color: #ffffcc }
.codehilite .c { color: #808080; font-style: italic }       /* comment */
.codehilite .err { border: 1px solid #800000 }             /* error */
.codehilite .k { color: #bf0000; font-weight: bold }       /* keyword */
.codehilite .o { color: #404040 }                          /* operator */
.codehilite .cm { color: #808080; font-style: italic }     /* comment */
.codehilite .cp { color: #BC7A00 }                         /* pragma */
.codehilite .c1 { color: #808080; font-style: italic }     /* comment */
.codehilite .cs { color: #808080; font-style: italic }     /* comment */
.codehilite .gd { color: #A00000 }                         /* deleted */
.codehilite .ge { font-style: italic }                     /* emphasis */
.codehilite .gi { color: #00A000 }                         /* inserted */
.codehilite .gh { color: #000080; font-weight: bold }      /* heading */
.codehilite .gr { color: #800000 }                         /* error */
.codehilite .go { color: #888888 }                         /* output */
.codehilite .gp { color: #555555 }                         /* prompt */
.codehilite .gs { font-weight: bold }                      /* strong */
.codehilite .gu { color: #800080; font-weight: bold }      /* user */
.codehilite .gt { color: #0044DD }                         /* title */
.codehilite .kc { color: #bf0000; font-weight: bold }      /* keyword class */
.codehilite .kd { color: #bf0000; font-weight: bold }      /* keyword definition */
.codehilite .kn { color: #bf0000; font-weight: bold }      /* keyword namespace */
.codehilite .kp { color: #bf0000 }                         /* keyword property */
.codehilite .kr { color: #bf0000 }                         /* keyword reserved */
.codehilite .kt { color: #458; font-weight: bold }         /* type */
.codehilite .m { color: #0040bf }                          /* number */
.codehilite .s { color: #00bf00 }                             /* string */
.codehilite .na { color: #008080 }                         /* name attribute */
.codehilite .nb { color: #bf4000 }                         /* name builtin */
.codehilite .nc { color: #000000 }                         /* name class */
.codehilite .no { color: #008080 }                         /* name constant */
.codehilite .nd { color: #4000bf}                          /* name decorator */
.codehilite .ni { color: #800080 }                         /* name entity */
.codehilite .ne { color: #800000 }                         /* name exception */
.codehilite .nf { color: #000000 }                         /* name function */
.codehilite .nl { color: #A0A000 }                         /* name label */
.codehilite .nn { color: #000000 }                         /* name namespace */
.codehilite .nt { color: #954121; font-weight: bold }      /* name tag */
.codehilite .nv { color: #008080 }                         /* name variable */
.codehilite .ow { color: #bf00bf; font-weight: bold }      /* operator word */
.codehilite .w { color: #bbbbbb }                          /* whitespace */
.codehilite .mf { color: #0000bf }                         /* number float */
.codehilite .mh { color: #0040bf }                         /* number hex */
.codehilite .mi { color: #0040bf }                         /* number integer */
.codehilite .mo { color: #0040bf }                         /* number oct */
.codehilite .sb { color: #40bf00 }                             /* string backtick */
.codehilite .sc { color: #40bf00 }                             /* string char */
.codehilite .sd { color: #00bf00; font-style: italic }        /* string doc */
.codehilite .s2 { color: #40bf00 }                            /* string double */
.codehilite .se { color: #40bf00 }                            /* string escape */
.codehilite .sh { color: #00bf00 }                            /* string heredoc */
.codehilite .si { color: #40bf00; font-style: italic }        /* string interpol */
.codehilite .sx { color: #40bf00 }                            /* string regex */
.codehilite .sr { color: #009926 }                         /* string raw */
.codehilite .s1 { color: #40bf00 }                            /* string single */
.codehilite .ss { color: #990073 }                         /* string symbol */
.codehilite .bp { color: #bf4000 }                         /* builtin pseudo */
.codehilite .vc { color: #008080 }                         /* variable class */
.codehilite .vg { color: #000000 }                         /* variable global */
.codehilite .vi { color: #008080 }                         /* variable instance */
.codehilite .il { color: #666666 }                         /* number literal */

blockquote {
    border-left: 4px solid #0080ff;
    margin: 10px 0;
    padding-left: 10px;
    color: #000000;
}
ul, ol {
    margin-left: 25px;
    padding-left: 5px;
}
table {
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border-right: 2px solid #000;
  padding: 8px 12px;
  text-align: left;
}

td {
  border-bottom: 2px solid #000;
}

th {
  border-bottom: 2px solid #000;
  color: #0080ff;
  font-weight: bold;
}

td:last-child, th:last-child {
  border-right: none;
}

tr:last-child td {
  border-bottom: none;
}

hr {
    border: none;
    height: 2px;
    background: #000000;
    margin: 20px 0;
}
a {
    color: #0078d7;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
::selection { background: #cce5ff; color: #000; }
</style>
"""

def sanitize_input(text):
    text = re.sub(r'<[^>]+>', lambda m: html.escape(m.group(0)), text)
    return text

def markdown_to_html(md_text):
    safe_md = sanitize_input(md_text)
    html_output = markdown.markdown(
        safe_md,
        extensions=[
            "extra",
            "codehilite",
            "toc",
            "sane_lists",
            "smarty",
            "nl2br",
            "attr_list",
            "def_list",
            "meta"
        ],
        extension_configs={
            "codehilite": {"guess_lang": False, "noclasses": False}
        },
        output_format="html5"
    )

    html_output = re.sub(r'(<pre><code>)(\n+)', r'\1', html_output)
    html_output = re.sub(r'(\n+)</code></pre>', r'</code></pre>', html_output)

    return html_output

def update_preview(event=None):
    md_text = text.get("1.0", tk.END)
    html_output = markdown_to_html(md_text)
    final_html = f"<!DOCTYPE html><html><head>{CSS_STYLE}</head><body>{html_output}</body></html>"
    preview.load_html(final_html)
    
def save_file(force=False):
    global current_file, changed

    if current_file is None:
        save_as()
        return

    if changed or force:
        with open(current_file, "w", encoding="utf-8") as f:
            f.write(text.get("1.0", "end-1c"))

        win.title(f'BukiMD - {current_file}')
        changed = False
        save.config(state="disabled")

def save_as():
    global current_file, filepath
    if language.get() == "türkçe":
        filepath = filedialog.asksaveasfilename(
            defaultextension='.html',
            filetypes=[('Markdown Dosyası', '*.md'), ('Tüm Dosyalar', '*.*')],
            title='Kaydet'
        )
    elif language.get() == "english":
        filepath = filedialog.asksaveasfilename(
            defaultextension='.html',
            filetypes=[('Markdown Files', '*.md'), ('All Files', '*.*')],
            title='Save'
        )
    if filepath:
        current_file = filepath
        win.title(f'BukiMD - {filepath}')
        save_file(force=True)
        
def open_file():
    global filepath, current_file, changed
    
    if language.get() == "türkçe":
        filepath = filedialog.askopenfilename(title='Aç', filetypes=[('Markdown Dosyası', '*.md'), ('Tüm dosyalar', '*.*')])
    elif language.get() == "english":
        filepath = filedialog.askopenfilename(title='Open', filetypes=[('Markdown Files', '*.md'), ('All Files', '*.*')])
        
    if filepath:
        with open(filepath, 'r', encoding='utf-8') as file:
            opened_file = file.read()
        text.delete(1.0, tk.END)
        text.insert(1.0, opened_file)
        current_file = filepath
        win.title(f'BukiMD - {current_file}')
        changed = False
        text.edit_modified(False)
        update_preview()
        update()
        save.config(state="disabled")

def new_file():
    global current_file, filepath, changed
    if changed:
        confirm = messagebox.askyesnocancel("Kaydet", "Bu belgeyi kaydetmek istiyor musunuz?")
        if confirm:
            save_file()
        if confirm == False: 
            pass
        if confirm is None:
            return
    changed = False
    current_file = None
    filepath = None
    text.delete(1.0, tk.END)
    update_title()
    update_preview()
    text.edit_modified(False)
    text.xview_moveto(0)
    text.yview_moveto(0)
    text.config(xscrollcommand=scroll_h.set, yscrollcommand=scroll.set)
    win.update_idletasks()

def update_title():
    if language.get() == "türkçe":
        title = "BukiMD - Yeni" if current_file is None else f"BukiMD - {current_file}"
    elif language.get() == "english":
        title = "BukiMD - New" if current_file is None else f"BukiMD - {current_file}"
        
    if changed:
        title += " *"
    win.title(title)
        
def save_on_exit():
    global changed
    if changed:
        confirm = messagebox.askyesnocancel("Kaydet", "Bu belgeyi kaydetmek istiyor musunuz?")
        if confirm:
            save_file()
            win.destroy()
        if confirm == False: 
            win.destroy()
    else:
        win.destroy()
        
    config = {
        "show_tooltip": show_tooltip.get(),
        "language": language.get(),
        "auto_save": auto_save.get()
        }
        
    with open(configuration_file, "w", encoding="utf-8") as f:
        cfile = json.dump(config, f, ensure_ascii=False, indent=4)
        
def undo_():
    try:
        text.edit_undo()
        update()
    except: pass
    
def redo_():
    try:
        text.edit_redo()
        update()
    except: pass
    
def update(event=None):
    global changed
    if text.edit_modified():
        changed = True
        update_title()
        text.edit_modified(False)
        save.config(state="normal")
        
def show_about():
    if language.get() == "türkçe":
        messagebox.showinfo("Hakkında", "BukiMD v1.0.5\n© Telif Hakkı 2025 Buğra US")
    elif language.get() == "english":
        messagebox.showinfo("About", "BukiMD v1.0.5\n© Copyright 2025 Buğra US")
    
def autosv(event):
    global current_file
    if current_file and auto_save.get():
        save_file()
    
toolbar_frame = tk.Frame(win)
toolbar_frame.grid(row=0, column=0, sticky="ew")

file_toolbar = tk.Frame(toolbar_frame, bd=1, relief="raised")
file_toolbar.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="w")

text_toolbar = tk.Frame(toolbar_frame, bd=1, relief="raised")
text_toolbar.grid(row=0, column=1, padx=10, pady=10, sticky="w")

do_toolbar = tk.Frame(toolbar_frame, bd=1, relief="raised")
do_toolbar.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="w")

other_toolbar_frame = tk.Frame(win)
other_toolbar_frame.grid(row=0, column=1, sticky="e")

other_toolbar = tk.Frame(other_toolbar_frame, bd=1, relief="raised")
other_toolbar.grid(row=0, column=0, padx=10, pady=10, sticky="e")

new = tk.Button(file_toolbar, text="\uE130", width=5, pady=4, bd=0, command=new_file, activebackground="yellow", font=("Segoe Fluent Icons", 10))
new.grid(row=0, column=0, padx=(3, 0), pady=3)

open_ = tk.Button(file_toolbar, text="\uE197", width=5, pady=4, bd=0, command=open_file, activebackground="yellow", font=("Segoe Fluent Icons", 10))
open_.grid(row=0, column=1, pady=3)

save = tk.Button(file_toolbar, text="\uE105", width=5, pady=4, bd=0, command=save_file, activebackground="yellow", font=("Segoe Fluent Icons", 10))
save.grid(row=0, column=2, pady=3, padx=(0, 3))

cut = tk.Button(text_toolbar, text="\uE16B", width=5, pady=4, bd=0, command=lambda: text.event_generate("<<Cut>>"), font=("Segoe Fluent Icons", 10), activebackground="yellow")
cut.grid(row=0, column=0, padx=(3, 0), pady=3)

copy = tk.Button(text_toolbar, text="\uE16F", width=5, pady=4, bd=0, command=lambda: text.event_generate("<<Copy>>"), activebackground="yellow", font=("Segoe Fluent Icons", 10))
copy.grid(row=0, column=1, pady=3)

paste = tk.Button(text_toolbar, text="\uE16D", width=5, pady=4, bd=0, command=lambda: text.event_generate("<<Paste>>"), activebackground="yellow", font=("Segoe Fluent Icons", 10))
paste.grid(row=0, column=2, padx=(0, 3), pady=3)

undo = tk.Button(do_toolbar, text="\uE10E", width=5, pady=4, bd=0, command=undo_, font=("Segoe Fluent Icons", 10), activebackground="yellow")
undo.grid(row=0, column=0, padx=(3, 0), pady=3)

redo = tk.Button(do_toolbar, text="\uE10D", width=5, pady=4, bd=0, command=redo_, font=("Segoe Fluent Icons", 10), activebackground="yellow")
redo.grid(row=0, column=1, padx=(0, 3), pady=3)

about = tk.Button(other_toolbar, text="\uE10C", width=5, pady=4, bd=0, command=show_about, activebackground="yellow", font=("Segoe Fluent Icons", 10))
about.grid(row=0, column=0, padx=3, pady=3, sticky="e")

tab = ttk.Notebook(win)

code_tab = tk.Frame(tab)
tab.add(code_tab, text="Kod")

text = tk.Text(code_tab, wrap="none", font=("Consolas", 10), undo=True)

pre_tab = tk.Frame(tab)
tab.add(pre_tab, text="Önizleme")

preview = HtmlFrame(pre_tab, messages_enabled=False)
preview.pack(fill="both", expand=True, padx=5, pady=5)

tab.grid(row=1, column=0, columnspan=2, padx=8, pady=(0, 8), sticky="nsew")

def indent(event=None):
    try:
        selection = text.tag_ranges("sel")
        if selection:
            start, end = selection
            lines = text.get(start, end).splitlines()
            indented = "\n".join("    "+line for line in lines)
            text.delete(start, end)
            text.insert(start, indented)
        else:
            text.insert("insert", "    ")
    except:
        text.insert("insert", "    ")
    return "break"

def unindent(event=None):
    try:
        selection = text.tag_ranges("sel")
        if selection:
            start, end = selection
            lines = text.get(start, end).splitlines()
            unindented = "\n".join(line[4:] if line.startswith("    ") else line for line in lines)
            text.delete(start, end)
            text.insert(start, unindented)
        else:
            cur_line = text.get("insert linestart", "insert lineend")
            if cur_line.startswith("    "):
                text.delete("insert linestart", "insert linestart+4c")
    except:
        pass
    return "break"

def update_settings(*args):
    global menu_labels, tab_labels
    if language.get() == "türkçe":
        menu_labels = {
            "file":{"label": "Dosya",
                    "menus":[
                        "Yeni",
                        "Yeni Pencere",
                        "Aç",
                        "Kaydet",
                        "Farklı Kaydet",
                        "Çık"
                        ]
                    },
            "edit":{"label": "Düzen",
                    "menus":[
                        "Geri Al",
                        "Yinele",
                        "Kes",
                        "Kopyala",
                        "Yapıştır",
                        "Tümünü Seç",
                        "Satırı Girintile",
                        "Satırın Girintisini Azalt"
                        ]
                    },
            "settings":{"label": "Ayarlar",
                        "menus":[
                            "Otomatik Kaydet",
                            "Araç İpuçlarını Göster",
                            "Dil"
                            ]
                        }
            }
        
        tab_labels = ["Kod", "Önizleme"]
    elif language.get() == "english":
        menu_labels = {
            "file":{"label": "File",
                    "menus":[
                        "New",
                        "New Window",
                        "Open",
                        "Save",
                        "Save As",
                        "Exit"
                        ]
                    },
            "edit":{"label": "Edit",
                    "menus":[
                        "Undo",
                        "Redo",
                        "Cut",
                        "Copy",
                        "Paste",
                        "Select All",
                        "Indent the line",
                        "Decrease the indent of the line"
                        ]
                    },
            "settings":{"label": "Settings",
                        "menus":[
                            "Auto Save",
                            "Show Tooltips",
                            "Language"
                            ]
                        }
            }
        
        tab_labels = ["Code", "Preview"]
    
    if language.get() == "türkçe":
        ToolTip(about, "Hakkında", shown=show_tooltip.get())
        ToolTip(redo, "Yinele - Ctrl+Y", shown=show_tooltip.get())
        ToolTip(undo, "Geri Al - Ctrl+Z", shown=show_tooltip.get())
        ToolTip(paste, "Yapıştır - Ctrl+V", shown=show_tooltip.get())
        ToolTip(copy, "Kopyala - Ctrl+C", shown=show_tooltip.get())
        ToolTip(cut, "Kes - Ctrl+X", shown=show_tooltip.get())
        ToolTip(save, "Kaydet - Ctrl+S", shown=show_tooltip.get())
        ToolTip(open_, "Aç - Ctrl+O", shown=show_tooltip.get())
        ToolTip(new, "Yeni - Ctrl+N", shown=show_tooltip.get())
        
    elif language.get() == "english":
        ToolTip(about, "About", shown=show_tooltip.get())
        ToolTip(redo, "Redo - Ctrl+Y", shown=show_tooltip.get())
        ToolTip(undo, "Undo - Ctrl+Z", shown=show_tooltip.get())
        ToolTip(paste, "Paste - Ctrl+V", shown=show_tooltip.get())
        ToolTip(copy, "Copy - Ctrl+C", shown=show_tooltip.get())
        ToolTip(cut, "Cut - Ctrl+X", shown=show_tooltip.get())
        ToolTip(save, "Save - Ctrl+S", shown=show_tooltip.get())
        ToolTip(open_, "Open - Ctrl+O", shown=show_tooltip.get())
        ToolTip(new, "New - Ctrl+N", shown=show_tooltip.get())
    
    menu.entryconfig(1, label=menu_labels["file"]["label"])
    file_menu.entryconfig(0, label=menu_labels["file"]["menus"][0])
    file_menu.entryconfig(1, label=menu_labels["file"]["menus"][1])
    file_menu.entryconfig(3, label=menu_labels["file"]["menus"][2])
    file_menu.entryconfig(4, label=menu_labels["file"]["menus"][3])
    file_menu.entryconfig(5, label=menu_labels["file"]["menus"][4])
    file_menu.entryconfig(7, label=menu_labels["file"]["menus"][5])
    
    menu.entryconfig(2, label=menu_labels["edit"]["label"])
    edit_menu.entryconfig(0, label=menu_labels["edit"]["menus"][0])
    edit_menu.entryconfig(1, label=menu_labels["edit"]["menus"][1])
    edit_menu.entryconfig(3, label=menu_labels["edit"]["menus"][2])
    edit_menu.entryconfig(4, label=menu_labels["edit"]["menus"][3])
    edit_menu.entryconfig(5, label=menu_labels["edit"]["menus"][4])
    edit_menu.entryconfig(6, label=menu_labels["edit"]["menus"][5])
    edit_menu.entryconfig(8, label=menu_labels["edit"]["menus"][6])
    edit_menu.entryconfig(9, label=menu_labels["edit"]["menus"][7])
    
    menu.entryconfig(3, label=menu_labels["settings"]["label"])
    pre_menu.entryconfig(0, label=menu_labels["settings"]["menus"][0])
    pre_menu.entryconfig(1, label=menu_labels["settings"]["menus"][1])
    pre_menu.entryconfig(2, label=menu_labels["settings"]["menus"][2])
    
    tab.tab(0, text=tab_labels[0])
    tab.tab(1, text=tab_labels[1])
    
    update_title()

show_tooltip.trace_add("write", update_settings)
language.trace_add("write", update_settings)
auto_save.trace_add("write", update_settings)

scroll = tk.Scrollbar(code_tab)
scroll.pack(side="right", padx=(0, 5), pady=5, fill="y")
scroll.config(command=text.yview)

scroll_h = tk.Scrollbar(code_tab, orient="horizontal")
scroll_h.pack(side="bottom", padx=(5, 0), pady=(0, 5), fill="x")
scroll_h.config(command=text.xview)
text.config(xscrollcommand=scroll_h.set, yscrollcommand=scroll.set)

text.pack(fill="both", padx=(5, 0), pady=(5, 0), expand=True)

text.bind("<KeyRelease>", update_preview)
text.bind("<Shift-Tab>", unindent)
text.bind("<Tab>", indent)
text.bind("<<Modified>>", update)
win.bind("<Control-s>", lambda e: save_file())
win.bind("<Control-Shift-S>", lambda e: save_as())
win.bind("<Control-o>", lambda e: open_file())
win.bind("<Control-n>", lambda e: new_file())
win.bind("<Control-z>", lambda e: undo_())
win.bind("<Control-y>", lambda e: redo_())
win.bind("<Control-Shift-N>", lambda e: subprocess.Popen([sys.executable, __file__]))

menu = tk.Menu(win)
win.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label='', command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label='', command=lambda: subprocess.Popen([sys.executable, __file__]), accelerator="Ctrl+Shift+N")
file_menu.add_separator()
file_menu.add_command(label='', command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label='', command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label='', command=save_as, accelerator="Ctrl+Shift+S")
file_menu.add_separator()
file_menu.add_command(label='', command=lambda: win.destroy(), accelerator="Alt+F4")
menu.add_cascade(menu=file_menu, label="")

edit_menu = tk.Menu(menu, tearoff=0)
edit_menu.add_command(label='', command=undo_, accelerator="Ctrl+Z")
edit_menu.add_command(label='', command=redo_, accelerator="Ctrl+Y")
edit_menu.add_separator()
edit_menu.add_command(label='', command=lambda: text.event_generate('<<Cut>>'), accelerator="Ctrl+X")
edit_menu.add_command(label='', command=lambda: text.event_generate('<<Copy>>'), accelerator="Ctrl+C")
edit_menu.add_command(label='', command=lambda: text.event_generate('<<Paste>>'), accelerator="Ctrl+V")
edit_menu.add_command(label='', command=lambda: text.tag_add('sel', '1.0', 'end'), accelerator="Ctrl+A")
edit_menu.add_separator()
edit_menu.add_command(label="", command=indent, accelerator="Tab")
edit_menu.add_command(label="", command=unindent, accelerator="Shift+Tab")
menu.add_cascade(menu=edit_menu, label="")

pre_menu = tk.Menu(menu, tearoff=0)
pre_menu.add_checkbutton(label="", onvalue=True, offvalue=False, variable=auto_save)
pre_menu.add_checkbutton(label="", onvalue=True, offvalue=False, variable=show_tooltip)
lang_menu = tk.Menu(menu, tearoff=0)
lang_menu.add_radiobutton(label='Türkçe', variable=language, value="türkçe")
lang_menu.add_radiobutton(label='English', variable=language, value="english")
pre_menu.add_cascade(menu=lang_menu, label="")
menu.add_cascade(menu=pre_menu, label="")

update_settings()

text.bind("<KeyRelease>", update_preview)
text.bind("<KeyRelease>", autosv, add="+")
text.bind('<Button-3>', lambda event: edit_menu.tk_popup(event.x_root, event.y_root))
win.protocol("WM_DELETE_WINDOW", save_on_exit)

win.mainloop()
