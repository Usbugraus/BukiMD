import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterweb import HtmlFrame
import markdown
import html
import re
import ctypes
import subprocess, sys, os

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
win.title("BukiMD - Yeni")
ttk.Style().theme_use("winnative")
win.geometry("800x600")
win.minsize(700, 500)
win.grid_rowconfigure(1, weight=1)
win.grid_columnconfigure(0, weight=1)
win.grid_columnconfigure(1, weight=1)

if hasattr(sys, "_MEIPASS"):
    icon_path = os.path.join(sys._MEIPASS, "Icon.ico")
else:
    icon_path = os.path.join(os.path.dirname(__file__), "Icon.ico")

if os.path.exists(icon_path):
    win.iconbitmap(icon_path)

CSS_STYLE = """
<style>
body {
    font-family: 'Segoe UI', sans-serif;
    background-color: #ffffff;
    color: #000;
    margin: 20px;
    line-height: 1.6;
    font-size: 15px;
}
h1 {
    color: #ff0000;
    padding-bottom: 5px;
    margin-top: 20px;
}
h2 {
    color: #0080ff;
    padding-bottom: 4px;
    margin-top: 20px;
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
    background: #fafafa;
    border-radius: 6px;
    white-space: pre-wrap;
    word-wrap: break-word;
    font-family: Consolas, monospace;
    font-size: 17px;
}

body code {
    background: #fafafa;
    padding: 2px 5px;
    border-radius: 6px;
    font-family: Consolas, monospace;
    white-space: pre;
    font-size: 17px;
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
    border-left: 4px solid #0078d7;
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
    margin: 10px 0;
}
th, td {
    border: 1px solid #000000;
    padding: 8px;
    text-align: left;
}
hr {
    border: none;
    height: 1px;
    background: #ccc;
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
    # Sadece <tag> benzeri HTML etiketlerini etkisizleştir
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
    if changed or force:
        if current_file:
            try:
                with open(current_file, "w", encoding="utf-8") as f:
                    f.write(text.get("1.0", "end-1c"))
                    win.title(f'BukiMD - {current_file}')
                    changed = False
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya kaydedilemedi:\n{str(e)}")
        else:
            save_as()

def save_as():
    global current_file, filepath
    filepath = filedialog.asksaveasfilename(defaultextension='.md',
                                            filetypes=[('Markdown Dosyası', '*.md'), ('Tüm Dosyalar', '*.*')],
                                            title='Kaydet')
    if filepath:
        current_file = filepath
        win.title(f'BukiMD - {filepath}')
        save_file(force=True)
        
def open_file():
    global filepath, current_file, changed
    try:
        filepath = filedialog.askopenfilename(title='Aç', filetypes=[('Markdown Dosyası', '*.md'), ('Tüm dosyalar', '*.*')])
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
    except Exception as e:
        messagebox.showerror('Hata', f"Dosya açılamadı:\n{str(e)}")

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

def update_title():
    title = "BukiMD - Yeni" if current_file is None else f"BukiMD - {current_file}"
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

new = tk.Button(file_toolbar, text="📄", width=4, bd=0, command=new_file, activebackground="yellow", font=("Segoe UI Emoji", 9))
new.grid(row=0, column=0, padx=(3, 0), pady=3)

open_ = tk.Button(file_toolbar, text="📂", width=4, bd=0, command=open_file, activebackground="yellow", font=("Segoe UI Emoji", 9))
open_.grid(row=0, column=1, pady=3)

save = tk.Button(file_toolbar, text="💾", width=4, bd=0, command=save_file, activebackground="yellow", font=("Segoe UI Emoji", 9))
save.grid(row=0, column=2, pady=3, padx=(0, 3))

cut = tk.Button(text_toolbar, text="✂", width=4, bd=0, command=lambda: text.event_generate("<<Cut>>"), font=("Segoe UI Emoji", 9), activebackground="yellow")
cut.grid(row=0, column=0, padx=(3, 0), pady=3)

copy = tk.Button(text_toolbar, text="📑", width=4, bd=0, command=lambda: text.event_generate("<<Copy>>"), activebackground="yellow", font=("Segoe UI Emoji", 9))
copy.grid(row=0, column=1, pady=3)

paste = tk.Button(text_toolbar, text="📋", width=4, bd=0, command=lambda: text.event_generate("<<Paste>>"), activebackground="yellow", font=("Segoe UI Emoji", 9))
paste.grid(row=0, column=2, padx=(0, 3), pady=3)

undo = tk.Button(do_toolbar, text="↶", width=4, bd=0, command=undo_, font=("Segoe UI Emoji", 9), activebackground="yellow")
undo.grid(row=0, column=0, padx=(3, 0), pady=3)

redo = tk.Button(do_toolbar, text="↷", width=4, bd=0, command=redo_, font=("Segoe UI Emoji", 9), activebackground="yellow")
redo.grid(row=0, column=1, padx=(0, 3), pady=3)

about = tk.Button(other_toolbar, text="⁝", width=4, bd=0, command=lambda: messagebox.showinfo("Hakkında", "BukiMD v1.0.0\n2025 Buğra US"), activebackground="yellow", font=("Segoe UI Emoji", 9))
about.grid(row=0, column=0, padx=3, pady=3, sticky="e")

tab = ttk.Notebook(win)

code_tab = tk.Frame(tab)
tab.add(code_tab, text="Kod")

text = tk.Text(code_tab, wrap="word", font=("Consolas", 10), undo=True)
text.pack(side="left", fill="both", expand=True)

pre_tab = tk.Frame(tab)
tab.add(pre_tab, text="Önizleme")

preview = HtmlFrame(pre_tab, messages_enabled=False)
preview.pack(fill="both", expand=True)

tab.grid(row=1, column=0, columnspan=2, padx=8, pady=8, sticky="nsew")

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

scroll = tk.Scrollbar(code_tab)
scroll.pack(side="right", padx=(0, 5), pady=(0, 5), fill="y")
scroll.config(command=text.yview)
text.config(yscrollcommand=scroll.set)

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
file_menu.add_command(label='Yeni', command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label='Yeni Pencere', command=lambda: subprocess.Popen([sys.executable, __file__]), accelerator="Ctrl+Shift+N")
file_menu.add_separator()
file_menu.add_command(label='Aç', command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label='Kaydet', command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label='Farklı Kaydet', command=save_as, accelerator="Ctrl+Shift+S")
file_menu.add_separator()
file_menu.add_command(label='Çık', command=lambda: win.destroy(), accelerator="Alt+F4")
menu.add_cascade(menu=file_menu, label="Dosya")

edit_menu = tk.Menu(menu, tearoff=0)
edit_menu.add_command(label='Geri al', command=undo_, accelerator="Ctrl+Z")
edit_menu.add_command(label='Yinele', command=redo_, accelerator="Ctrl+Y")
edit_menu.add_separator()
edit_menu.add_command(label='Kes', command=lambda: text.event_generate('<<Cut>>'), accelerator="Ctrl+X")
edit_menu.add_command(label='Kopyala', command=lambda: text.event_generate('<<Copy>>'), accelerator="Ctrl+C")
edit_menu.add_command(label='Yapıştır', command=lambda: text.event_generate('<<Paste>>'), accelerator="Ctrl+V")
edit_menu.add_command(label='Tümünü Seç', command=lambda: text.tag_add('sel', '1.0', 'end'), accelerator="Ctrl+A")
edit_menu.add_separator()
edit_menu.add_command(label="Satırı Girintile", command=indent, accelerator="Tab")
edit_menu.add_command(label="Satırın Girintisini Azalt", command=unindent, accelerator="Shift+Tab")
menu.add_cascade(menu=edit_menu, label="Düzen")

text.bind('<Button-3>', lambda event: edit_menu.tk_popup(event.x_root, event.y_root))
win.protocol("WM_DELETE_WINDOW", save_on_exit)

win.mainloop()
