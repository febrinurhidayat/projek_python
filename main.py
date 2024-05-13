from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter
import random
import pymysql
from datetime import datetime
import subprocess
import mysql.connector

window = tkinter.Tk()
window.title("GUDANG FEBRI")
window.geometry("1243x600+100+100")
tabel_data = ttk.Treeview(window, show='headings', height=90)

style = ttk.Style()

placeholderArray = ['', '', '', '', '', '', '']
numeric = '1234567890'
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='projectpython'
    )
    return conn

conn = connection()
cursor = conn.cursor()

for i in range(0, 7):  # Perbaiki panjang array menjadi 7
    placeholderArray[i] = tkinter.StringVar()

def read():
    conn = connection()
    cursor = conn.cursor()
    cursor.connection.ping()
    sql = "SELECT `item_id`, `name`, `price`, `quantity`, `category`, `tanggal_masuk`, `tanggal_keluar` FROM stocks ORDER BY `item_id` DESC"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

# def refreshTable():
#     for data in tabel_data.get_children():
#         tabel_data.delete(data)
#     for array in read():
#         tabel_data.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")
#     tabel_data.tag_configure('orow', background="#ffffff")
#     tabel_data.pack()

def fetch_data(tabel_data):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            db='projectpython'
        )

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM stocks")
        rows = cursor.fetchall()

        for item in tabel_data.get_children():
            tabel_data.delete(item)

        for column in rows:
            data = (column[0], column[1], column[2],column[3], column[4], column[5], column[6])
            tabel_data.insert("", "end", values=data)
        connection.close()

    except mysql.connector.Error as e:
        print(f"Error: {e}")



def refresh_data():
    fetch_data(tabel_data) 
    
def cari():
    # Buat salinan data asli untuk keperluan pencarian
    original_data = read()  # Anda perlu mengganti fungsi ini sesuai dengan cara Anda membaca data

    for item in tabel_data.get_children():
        tabel_data.delete(item)

    val = str(entry_search.get())
    cursor.connection.ping()
    
    cursor.execute("SELECT * FROM stocks WHERE name LIKE %s", ("%"+val+"%",))
    result = cursor.fetchall()

    for column in result:
        data = (column[0], column[1], column[2], column[3], column[4], column[5], column[6])
        tabel_data.insert("", "end", values=data)


def setph(word, num):
    for ph in range(0, 7):  # Perbaiki panjang array menjadi 7
        if ph == num:
            placeholderArray[ph].set(word)

def get_current_date():
    current_date = datetime.now().strftime("%Y-%m-%d")
    return current_date

def set_auto_date():
    tanggal_masuk = get_current_date()
    setph(tanggal_masuk, 5)
    tglmskEntry.config(state="readonly")
    tglklrEntry.config(state="readonly")

def generateRand():
    itemId = ''
    for i in range(0, 3):
        randno = random.randrange(0, len(numeric))
        itemId = itemId + str(numeric[randno])
    randno = random.randrange(0, len(alpha))
    itemId = itemId + '-' + str(alpha[randno])
    print("generated: " + itemId)
    setph(itemId, 0)

def save():
    itemId = str(itemIdEntry.get())
    name = str(nameEntry.get())
    price = str(priceEntry.get())
    qnt = str(qntEntry.get())
    cat = str(categoryCombo.get())
    tglmsk = str(tglmskEntry.get())
    tglklr = str(tglklrEntry.get())
    valid = True
    if not (itemId and itemId.strip()) or not (name and name.strip()) or not (price and price.strip()) or not (
            qnt and qnt.strip()) or not (cat and cat.strip()) or not (tglmsk and tglmsk.strip()):
        messagebox.showwarning("", "Tolong isi semua dengan benar")
        return
    if len(itemId) < 5:
        messagebox.showwarning("", "barang tidak ditemukan")
        return
    if not (itemId[3] == '-'):
        valid = False
    for i in range(0, 3):
        if not (itemId[i] in numeric):
            valid = False
            break
    if not (itemId[4] in alpha):
        valid = False
    if not (valid):
        messagebox.showwarning("", "barang tidak ditemukan")
        return
    try:
        cursor.connection.ping()
        sql = f"SELECT * FROM stocks WHERE `item_id` = '{itemId}' "
        cursor.execute(sql)
        checkItemNo = cursor.fetchall()
        if len(checkItemNo) > 0:
            messagebox.showwarning("", "barang sudah ada digudang")
            return
        else:
            cursor.connection.ping()
            sql = f"INSERT INTO stocks (`item_id`, `name`, `price`, `quantity`, `category`, `tanggal_masuk`, `tanggal_keluar`) VALUES ('{itemId}','{name}','{price}','{qnt}','{cat}','{tglmsk}', '{None if not tglklr else f'{tglklr}'}')"
            cursor.execute(sql)
        conn.commit()
        for num in range(0, 7):  # Perbaiki panjang array menjadi 7
            setph('', (num))
    except Exception as e:
        print(e)
        messagebox.showwarning("", "Terjadi kesalahan saat menyimpan: " + str(e))
        return
    refresh_data()

def update():
    selectedItemId = ''
    try:
        selectedItem = tabel_data.selection()[0]
        selectedItemId = str(tabel_data.item(selectedItem)['values'][0])
    except IndexError:
        messagebox.showwarning("", "Tolong pilih data barang di tabel")
        return

    item_id = str(itemIdEntry.get())
    name = str(nameEntry.get())
    price = str(priceEntry.get())
    qnt = str(qntEntry.get())
    cat = str(categoryCombo.get())
    tglmsk = str(tglmskEntry.get())
    tglklr = str(tglklrEntry.get())

    if not (item_id and item_id.strip()) or not (name and name.strip()) or not (price and price.strip()) or not (
            qnt and qnt.strip()) or not (cat and cat.strip()) or not (tglmsk and tglmsk.strip()):
        messagebox.showwarning("", "Tolong isi semua dengan benar")
        return
    if selectedItemId != item_id:
        messagebox.showwarning("", "Anda tidak bisa mengubah Id Barang")
        return

    try:
        cursor.connection.ping()
        sql = f"UPDATE stocks SET `name` = '{name}', `price` = '{price}', `quantity` = '{qnt}', `category` = '{cat}', `tanggal_masuk` = '{tglmsk}', `tanggal_keluar` = '{''}' WHERE `item_id` = '{item_id}'"
        cursor.execute(sql)
        conn.commit()

        tabel_data.item(selectedItem, values=(item_id, name, price, qnt, cat, tglmsk, tglklr)) 

        for num in range(0, 7):  # Perbaiki panjang array menjadi 7
            setph('', (num))
    except Exception as err:
        messagebox.showwarning("", f"Maaf, terjadi kesalahan: {err}")
        return

def delete():
    try:
        if tabel_data.selection()[0]:
            decision = messagebox.askquestion("", "Apakah anda mau menghapus barang?")
            if decision != 'yes':
                return
            else:
                selectedItem = tabel_data.selection()[0]
                itemId = str(tabel_data.item(selectedItem)['values'][0])
                try:
                    cursor.connection.ping()
                    sql = f"DELETE FROM stocks WHERE `item_id` = '{itemId}' "
                    cursor.execute(sql)
                    conn.commit()
                    messagebox.showinfo("", "Barang telah dihapus dalam data")
                except:
                    messagebox.showinfo("", "Maaf, terjadi kesalahan")
                refresh_data()
    except:
        messagebox.showwarning("", "Tolong pilih data barang ditabel")

def select():
    try:
        selectedItem = tabel_data.selection()[0]
        itemId = str(tabel_data.item(selectedItem)['values'][0])
        name = str(tabel_data.item(selectedItem)['values'][1])
        price = str(tabel_data.item(selectedItem)['values'][2])
        qnt = str(tabel_data.item(selectedItem)['values'][3])
        cat = str(tabel_data.item(selectedItem)['values'][4])
        tglmsk = str(tabel_data.item(selectedItem)['values'][5])
        tglklr = str(tabel_data.item(selectedItem)['values'][6])
        setph(itemId, 0)
        setph(name, 1)
        setph(price, 2)
        setph(qnt, 3)
        setph(cat, 4)
        setph(tglmsk, 5)
        setph(tglklr, 6)
    except:
        messagebox.showwarning("", "Tolong pilih data barang di tabel")

def clear():
    for num in range(0, 7):  # Perbaiki panjang array menjadi 7
        setph('', (num))

def logout():
    result = messagebox.askquestion("Logout", "Apakah Anda yakin ingin logout?")
    if result == "yes":
        window.destroy()
        subprocess.run(["python", "login.py"]) #kalo tidak bisa perpindah coba menggunakan format seperti ini D:\MATKUL IF AMIKOM SEMESTER 3\Bahasa pemograman python\finaly project\projek\projekpython\login.py

frame=tkinter.Frame(window,bg="white")
frame.pack(side=LEFT, fill=BOTH)


manageFrame=tkinter.Frame(window,background="#06373d",bd=5, relief=RIDGE)
manageFrame.pack(side=TOP,fill=BOTH)

saveBtn=Button(manageFrame,text="SIMPAN",width=10,borderwidth=3,bg='#007841',fg='#ffffff',command=save,)
updateBtn=Button(manageFrame,text="UPDATE",width=10,borderwidth=3,bg='#004680',fg='#ffffff',command=update)
deleteBtn=Button(manageFrame,text="HAPUS",width=10,borderwidth=3,bg='#d5bc26',fg='#ffffff',command=delete)
selectBtn=Button(manageFrame,text="SELECT",width=10,borderwidth=3,bg='#004680',fg='#ffffff',command=select)
clearBtn=Button(manageFrame,text="CLEAR",width=10,borderwidth=3,bg='#004680',fg='#ffffff',command=clear)
logout_button = Button(manageFrame, text="LOGOUT",width=10,borderwidth=3,bg='#d30f3f',fg='#ffffff',command=logout)

saveBtn.grid(row=0,column=0,padx=30,pady=5)
updateBtn.grid(row=0,column=1,padx=30,pady=5)
deleteBtn.grid(row=0,column=5,padx=30,pady=5)
selectBtn.grid(row=0,column=3,padx=30,pady=5)
clearBtn.grid(row=0,column=2,padx=30,pady=5)
logout_button.grid(row=0, column=6,padx=30,pady=5)

entriesFrame=tkinter.Frame(frame,bg="#06373d",bd=5, relief=RIDGE)
entriesFrame.pack(side=TOP,fill=BOTH)

tes=tkinter.Frame(frame,bg="#06373d",bd=5, relief=RIDGE,height=1000)
tes.pack(side=TOP,fill=BOTH)

tas=tkinter.Frame(frame,bg="#06373d",bd=5, relief=RIDGE,height=1000)
tas.pack(side=TOP,fill=BOTH)


itemIdLabel=Label(entriesFrame,text="ITEM ID :",anchor="e",width=10,bg="#06373d",fg='#ffffff',font=('Manage',8,'bold'))
nameLabel=Label(entriesFrame,text=" BARANG :",anchor="e",width=10,bg="#06373d",fg='#ffffff',font=('Manage',8,'bold'))
priceLabel=Label(entriesFrame,text="HARGA :",anchor="e",width=10,bg="#06373d",fg='#ffffff',font=('Manage',8,'bold'))
qntLabel=Label(entriesFrame,text="JUMLAH :",anchor="e",width=10,bg="#06373d",fg='#ffffff',font=('Manage',8,'bold'))
categoryLabel=Label(entriesFrame,text="KATEGORI :",anchor="e",width=10,bg="#06373d",fg='#ffffff',font=('Manage',8,'bold'))
tglmskLabel=Label(entriesFrame,text="TGL MASUK :",anchor="e",width=10,bg="#06373d",fg='#ffffff',font=('Manage',8,'bold'))
tglklrLabel=Label(entriesFrame,text="TGL KELUAR :",anchor="e",width=10,bg="#06373d",fg='#ffffff',font=('Manage',8,'bold'))

itemIdLabel.grid(row=0,column=0,padx=10)
nameLabel.grid(row=1,column=0,padx=10)
priceLabel.grid(row=2,column=0,padx=10)
qntLabel.grid(row=3,column=0,padx=10)
categoryLabel.grid(row=4,column=0,padx=10)
tglmskLabel.grid(row=5,column=0,padx=10)
tglklrLabel.grid(row=6,column=0,padx=10)

categoryArray=['Produk Makanan','Produk Minuman','Produk Elektronik','Produk Kesehatan','Produk Beku','Produk RumahTangga','Pakaian','Mainan']

itemIdEntry=Entry(entriesFrame,width=10,textvariable=placeholderArray[0])
nameEntry=Entry(entriesFrame,width=25,textvariable=placeholderArray[1])
priceEntry=Entry(entriesFrame,width=25,textvariable=placeholderArray[2])
qntEntry=Entry(entriesFrame,width=25,textvariable=placeholderArray[3])
categoryCombo=ttk.Combobox(entriesFrame,width=25,textvariable=placeholderArray[4],values=categoryArray)
tglmskEntry=Entry(entriesFrame,width=25,textvariable=placeholderArray[5])
tglklrEntry=Entry(entriesFrame,width=25,textvariable=placeholderArray[6])

itemIdEntry.grid(row=0,column=2,sticky="w",padx=5,pady=5)
nameEntry.grid(row=1,column=2,sticky="w",padx=5,pady=5)
priceEntry.grid(row=2,column=2,sticky="w",padx=5,pady=5)
qntEntry.grid(row=3,column=2,sticky="w",padx=5,pady=5)
categoryCombo.grid(row=4,column=2,sticky="w",padx=5,pady=5)
tglmskEntry.grid(row=5,column=2,sticky="w",padx=5,pady=5)
tglklrEntry.grid(row=6,column=2,sticky="w",padx=5,pady=5)

generateIdBtn=Button(entriesFrame,text="GENERATE ID",borderwidth=3,bg='#004680',fg='#ffffff',font=('Manage',9),command=generateRand)
generateIdBtn.grid(row=0,column=2,sticky="w", padx=85 ,pady=5)

button_search = Button(tes, text='Search',borderwidth=2,bg='#004680',fg='#ffffff',font=('Manage',9))
entry_search = Entry(tes, width=25,font=('Manage',10))
entry_search.grid(row=0,column=0,sticky="n",padx=5,pady=5)
button_search.grid(row=0,column=1,sticky="n",padx=5,pady=5)
button_search['command']=cari
cari()

style.configure(window)
tabel_data['columns']=("Id barang","Nama Barang","Harga","Jumlah","Kategori","Tanggal Masuk","Tanggal Keluar")
tabel_data.column("#0",width=0,stretch=NO)
tabel_data.column("Id barang",anchor=W,width=70)
tabel_data.column("Nama Barang",anchor=W,width=125)
tabel_data.column("Harga",anchor=W,width=125)
tabel_data.column("Jumlah",anchor=W,width=100)
tabel_data.column("Kategori",anchor=W,width=150)
tabel_data.column("Tanggal Masuk",anchor=W,width=150)
tabel_data.column("Tanggal Keluar",anchor=W,width=150)

tabel_data.heading("Id barang",text="Id barang",anchor=W)
tabel_data.heading("Nama Barang",text="Nama Barang",anchor=W)
tabel_data.heading("Harga",text="Harga",anchor=W)
tabel_data.heading("Jumlah",text="Jumlah",anchor=W)
tabel_data.heading("Kategori",text="Kategori",anchor=W)
tabel_data.heading("Tanggal Masuk",text="Tanggal Masuk",anchor=W)
tabel_data.heading("Tanggal Keluar",text="Tanggal Keluar",anchor=W)
tabel_data.pack()

refresh_data()
set_auto_date()

window.resizable(False,False)
window.mainloop()