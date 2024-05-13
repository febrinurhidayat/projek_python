import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import csv
from datetime import datetime
import mysql.connector
import subprocess
from login import LoginApp


def connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='projectpython'
    )
    return conn

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

def exportExcel():
    conn = connection()
    cursor = conn.cursor()
    cursor.connection.ping()
    sql = "SELECT `item_id`, `name`, `price`, `quantity`, `category`, `tanggal_masuk`, `tanggal_keluar` FROM stocks ORDER BY `item_id` DESC"
    cursor.execute(sql)
    dataraw = cursor.fetchall()
    date = str(datetime.now())
    date = date.replace(' ', '_')
    date = date.replace(':', '-')
    dateFinal = date[0:16]
    with open("stocks_"+dateFinal+".csv", 'a', newline='') as f:
        w = csv.writer(f, dialect='excel')
        for record in dataraw:
            w.writerow(record)
    print("saved: stocks_"+dateFinal+".csv")
    conn.commit()
    conn.close()
    messagebox.showinfo("", "File Excel telah didownload")


window = tk.Tk()
window.title("GUDANG KARYAWAN")
window.geometry("767x640+100+100")
my_tree = ttk.Treeview(window, show='headings', height=90)
style = ttk.Style()

frame = tk.Frame(window, bg="#109057")
frame.pack()


def update_tanggal_keluar(item_id, tanggal_keluar, popup):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            db='projectpython'
        )

        cursor = connection.cursor()

        # Misalkan Anda memiliki kolom 'tanggal_keluar' yang ingin diupdate
        update_sql = "UPDATE stocks SET tanggal_keluar = %s WHERE item_id = %s"

        # Eksekusi query update
        cursor.execute(update_sql, (tanggal_keluar, item_id))

        # Commit perubahan
        connection.commit()

        # Tutup koneksi
        connection.close()

        messagebox.showinfo("Update", "Tanggal keluar berhasil diupdate")
        popup.destroy()

        # Refresh tabel setelah update
        refresh_data()

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", "Gagal mengupdate tanggal keluar")

def update_data():
    selected_item = my_tree.selection()
    try:
            # Ambil data dari baris yang dipilih
            item_id = my_tree.item(selected_item, "values")[0]

            # Tampilkan popup untuk memasukkan tanggal keluar
            popup = tk.Toplevel(window)
            popup.title("Update Tanggal Keluar")
            popup.geometry("400x100+100+100")
            popup.configure(bg="#06373d")
            popup.resizable(width=False, height=False)
            label = tk.Label(popup, text="Masukkan Tanggal Keluar:",fg="#ffffff", bg="#06373d", font=('Manage', 11,))
            label.pack(pady=1)

            entry_date = tk.Entry(popup,width=25, fg="black", bg="white", font=('Manage', 11))
            entry_date.pack(pady=1)

            # Fungsi untuk melakukan update
            def update_clicked():
                tanggal_keluar = entry_date.get()
                update_tanggal_keluar(item_id, tanggal_keluar, popup)

            # Tombol untuk melakukan update
            button_update = tk.Button(popup, text="Update",bg="#ff9800", fg="white", width=21, relief="ridge", borderwidth=3, font=('Manage', 11,), command=update_clicked)
            button_update.pack(pady=10)

    except IndexError as e:
            print(f"Error: {e}")
            messagebox.showerror(
                "Error", "Gagal mendapatkan data barang. Pilih baris yang valid.")


def fetch_data(my_tree):
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

        for item in my_tree.get_children():
            my_tree.delete(item)

        for column in rows:
            data = (column[0], column[1], column[2],column[3], column[4], column[5], column[6])
            my_tree.insert("", "end", values=data)
        connection.close()

    except mysql.connector.Error as e:
        print(f"Error: {e}")

  
def refresh_data():
    fetch_data(my_tree)


def logout():
    result = messagebox.askquestion(
        "Logout", "Apakah Anda yakin ingin logout?")

    if result == "yes":
        window.destroy()
        subprocess.run(["python", "login.py"])


# Tombol
tes = tk.Frame(window, bg="#06373d", bd=5, relief=tk.RIDGE, height=1000)
tes.pack(side=tk.TOP, fill=tk.BOTH)

refresh_button = tk.Button(tes, text="REFRESH", command=refresh_data,
                           width=10, borderwidth=3, bg='#004680', fg='#ffffff')
refresh_button.grid(row=0, column=0, padx=10, pady=5)

excel_button = tk.Button(tes, text="DOWNLOAD", command=exportExcel,
                         width=10, borderwidth=3, bg='#007841', fg='#ffffff')
excel_button.grid(row=0, column=1, padx=10, pady=5)

update_button = tk.Button(tes, text="UPDATE", command=update_data,
                          width=10, borderwidth=3, bg='#ff9800', fg='#ffffff')
update_button.grid(row=0, column=2, padx=10, pady=5)

logout_button = tk.Button(tes, text="LOGOUT", command=logout,
                          width=10, borderwidth=3, bg='#d30f3f', fg='#ffffff')
logout_button.grid(row=0, column=3, padx=(355,0), pady=5, sticky=tk.E)

my_tree['columns'] = ("Id barang", "Nama Barang", "Harga",
                      "Jumlah", "Kategori", "Tanggal Masuk", "Tanggal Keluar")
my_tree.column("#0", width=0, stretch=tk.NO)
my_tree.column("Id barang", anchor=tk.W, width=70)
my_tree.column("Nama Barang", anchor=tk.W, width=125)
my_tree.column("Harga", anchor=tk.W, width=70)
my_tree.column("Jumlah", anchor=tk.W, width=50)
my_tree.column("Kategori", anchor=tk.W, width=150)
my_tree.column("Tanggal Masuk", anchor=tk.W, width=150)
my_tree.column("Tanggal Keluar", anchor=tk.W, width=150)

my_tree.heading("Id barang", text="Id barang", anchor=tk.W)
my_tree.heading("Nama Barang", text="Nama Barang", anchor=tk.W)
my_tree.heading("Harga", text="Harga", anchor=tk.W)
my_tree.heading("Jumlah", text="Jumlah", anchor=tk.W)
my_tree.heading("Kategori", text="Kategori", anchor=tk.W)
my_tree.heading("Tanggal Masuk", text="Tanggal Masuk", anchor=tk.W)
my_tree.heading("Tanggal Keluar", text="Tanggal Keluar", anchor=tk.W)

my_tree.tag_configure('orow', background="#109057")
my_tree.pack()

refresh_data()

window.resizable(False, False)
window.mainloop()
