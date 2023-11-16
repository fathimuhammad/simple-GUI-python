from tkinter import *
from tkinter import messagebox
from tkinter.filedialog   import asksaveasfilename
from tkinter import filedialog
import os
from tkinter.messagebox import askokcancel

class SimpleEditor(Frame):
    def __init__(self, parent=None, file=None):
        Frame.__init__(self, parent)
        self.frm = Frame(parent)
        self.frm.pack(fill=X)
        self.buatJudul()
        parent.title('Text Editor')
        #parent.title('Text editor dengan copy paste - dari mn-belajarpython.blogspot.co.id')
        self.buatTombol()
        self.kolomTeksUtama()
        self.settext(text='',file=file)
        self.kolomTeks.config(font=('DejaVu Sans Mono', 10))
        self.indeks = 1.0
        self.buatCari()
        self.path = ''

    def buatTombol(self):
        Button(self.frm, text='Open', relief='flat',  command=self.bukaFile).pack(side=LEFT)
        Button(self.frm, text='Save', relief='flat',  command=self.perintahSimpan).pack(side=LEFT)
        Button(self.frm, text='Copy', relief='flat', command=self.perintahCopy).pack(side=LEFT)
        Button(self.frm, text='Cut', relief='flat',   command=self.perintahCut).pack(side=LEFT)
        Button(self.frm, text='Paste', relief='flat', command=self.perintahPaste).pack(side=LEFT)
        Button(self.frm, text='Undo', relief='flat',   command=self.perintahUndo).pack(side=LEFT)
        Button(self.frm, text='Redo', relief='flat', command=self.perintahRedo).pack(side=LEFT)
        Button(self.frm, text='Keluar', relief='flat', command=self.perintahKeluar).pack(side=LEFT)

    def kolomTeksUtama(self):
        scroll = Scrollbar(self)
        kolomTeks = Text(self, relief=SUNKEN, undo=True)
        scroll.config(command=kolomTeks.yview)
        kolomTeks.config(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)
        kolomTeks.pack(side=LEFT, expand=YES, fill=BOTH)
        self.kolomTeks = kolomTeks
        self.pack(expand=YES, fill=BOTH)

    def perintahSimpan(self):
        print(self.path)
        if self.path:
            alltext = self.gettext()
            open(self.path, 'w').write(alltext)
            messagebox.showinfo('Berhasil', 'Selamat File telah tersimpan ! ')
        else:
            tipeFile = [('Text file', '*.txt'), ('Python file', '*asdf.py'), ('All files', '.*')]
            filename = asksaveasfilename(filetypes=(tipeFile), initialfile=self.kolomJudul.get())
            if filename:
                alltext = self.gettext()
                open(filename, 'w').write(alltext)
                self.path = filename

    def perintahCopy(self):
        try:
            text = self.kolomTeks.get(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)
            self.kolomTeks.selection_clear()
        except:
            pass

    def perintahCut(self):
        try :
            text = self.kolomTeks.get(SEL_FIRST, SEL_LAST)
            self.kolomTeks.delete(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)
        except:
            pass

    def perintahPaste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.kolomTeks.insert(INSERT, text)
        except TclError:
            pass

    def perintahFind(self):
        target = self.kolomCari.get()
        if target:
            self.indeks = self.kolomTeks.search(target, str(float(self.indeks)+0.1), stopindex=END)
            if self.indeks:
                pastit = self.indeks + ('+%dc' % len(target))
                self.kolomTeks.tag_remove(SEL, '1.0', END)
                self.kolomTeks.tag_add(SEL, self.indeks, pastit)
                self.kolomTeks.mark_set(INSERT, pastit)
                self.kolomTeks.see(INSERT)
                self.kolomTeks.focus()
            else:
                self.indeks = '0.9'

    def perintahKeluar(self):
        ans = askokcancel('Keluar', "anda yakin ingin keluar?")
        if ans: Frame.quit(self)

    def settext(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
        self.kolomTeks.delete('1.0', END)
        self.kolomTeks.insert('1.0', text)
        self.kolomTeks.mark_set(INSERT, '1.0')
        self.kolomTeks.focus()

    def gettext(self):
        return self.kolomTeks.get('1.0', END+'-1c')

    def buatJudul(self):
        top = Frame(root)
        top.pack(fill=BOTH, padx=17, pady=5)
        judul = Label(top, text="Judul : ")
        judul.pack(side="left")
        self.kolomJudul = Entry(top)
        self.kolomJudul.pack(side="left")

    def buatCari(self):
        Button(self.frm, text='Cari', command=self.perintahFind).pack(side="right")
        self.kolomCari = Entry(self.frm)
        self.kolomCari.pack(side="right")

    def bukaFile(self):
        extensiFile = [ ('All files', '*'), ('Text files', '*.txt'),('Python files', '*.py')]
        buka = filedialog.askopenfilename(filetypes = extensiFile)
        if buka != '':
            text = self.readFile(buka)
            if text:
                self.path = buka
                nama = os.path.basename(buka)
                self.kolomJudul.delete(0, END)
                self.kolomJudul.insert(END, nama)
                self.kolomTeks.delete('0.1',END)
                self.kolomTeks.insert(END, text)

    def readFile(self, filename):
        try:
            f = open(filename, "r")
            text = f.read()
            return text
        except:
            messagebox.showerror("Error!!","Maaf file tidak dapat dibuka ! :) \nsabar ya..")
            return None

    def perintahUndo(self):
        try:
            self.kolomTeks.edit_undo()
        except:
            pass
    def perintahRedo(self):
        try:
            self.kolomTeks.edit_redo()
        except:
            pass

root = Tk()
SimpleEditor(root)
mainloop()