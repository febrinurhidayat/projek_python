import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import subprocess

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Login")
        self.root.geometry("910x500+100+100")
        self.root.configure(bg="#06373d")  

        self.login_frame = tk.Frame(root, bg="#1a5186", width=600, height=600, relief="ridge", borderwidth=5)
        self.login_frame.pack(pady=100, padx=150)

        self.label_sign = tk.Label(self.login_frame, text="Sign in", fg="#ffffff", bg="#1a5186", font=('Manage', 20, 'bold'))
        self.label_username = tk.Label(self.login_frame, text="Username:", fg="#ffffff", bg="#1a5186", font=('Manage', 11,))
        self.label_jabatan = tk.Label(self.login_frame, text="Jabatan:", fg="#ffffff", bg="#1a5186", font=('Manage', 11,))
        self.label_password = tk.Label(self.login_frame, text="Password:", fg="#ffffff", bg="#1a5186", font=('Manage', 11,))
        self.entry_username = tk.Entry(self.login_frame, width=25, fg="black", bg="white", font=('Manage', 11))
        
        
        self.roles = ['Admin', 'Karyawan']
        self.combo_jabatan = ttk.Combobox(self.login_frame, values=self.roles, state="readonly", width= 23,font=('Manage', 11,))
        
        self.entry_password = tk.Entry(self.login_frame, width=25, fg="black", bg="white", font=('Manage', 11), show="*")

        self.label_sign.pack(pady=10)

        self.label_username.pack(pady=0)
        self.entry_username.pack(pady=0, padx=50)
       
        self.label_jabatan.pack(pady=0)
        self.combo_jabatan.pack(pady=0, padx=50)

        self.label_password.pack(pady=0)
        self.entry_password.pack(pady=0, padx=50)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login, bg="#06373d", fg="white", width=10, relief="ridge", borderwidth=3, font=('Manage', 11,))
        self.login_button.pack(side=tk.LEFT, pady=20, padx=(50, 1))  # Menambahkan padding di sisi kanan untuk memberikan jarak

        self.register_button = tk.Button(self.login_frame, text="Register", command=self.open_registration_window, bg="#06373d", fg="white", width=10, relief="ridge", borderwidth=3, font=('Manage', 11,))
        self.register_button.pack(side=tk.RIGHT, pady=20, padx=(1, 50))  # Menambahkan padding di sisi kiri untuk memberikan jarak
        
    def login(self):
        username = self.entry_username.get()
        jabatan = self.combo_jabatan.get() 
        password = self.entry_password.get()

      
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='projectpython'
            )

            cursor = connection.cursor()

            cursor.execute("SELECT * FROM users WHERE username=%s AND jabatan=%s AND password=%s", (username, jabatan, password))
            user_data = cursor.fetchone()

            if user_data:
                if user_data[3] == 'admin':
                    messagebox.showinfo("Login", "Selamat datang, Admin!")
                    self.root.destroy()
                    self.open_admin_window()
                elif user_data[3] == 'karyawan':
                    messagebox.showinfo("Login", "Selamat datang, Karyawan!")
                    self.root.destroy()
                    self.open_karyawan_window()
                else:
                    messagebox.showwarning("Login", "Role pengguna tidak valid.")
            else:
                messagebox.showwarning("Login", "Jabatan atau password salah.")

        except mysql.connector.Error as e:
            print(f"Error: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def open_admin_window(self):
        subprocess.run(["python", "main.py"]) #kalo tidak bisa perpindah coba menggunakan format seperti ini D:\MATKUL IF AMIKOM SEMESTER 3\Bahasa pemograman python\finaly project\projek\projekpython\main.py

    def open_karyawan_window(self):
        subprocess.run(["python", "karyawan.py"]) #kalo tidak bisa perpindah coba menggunakan format seperti ini D:\MATKUL IF AMIKOM SEMESTER 3\Bahasa pemograman python\finaly project\projek\projekpython\karyawan.py

    def open_registration_window(self):
        registration_window = tk.Toplevel(self.root)
        registration_window.title("Registrasi")
        registration_window.geometry("500x200+100+100")
        registration_window.configure(bg="#06373d")
        registration_window.resizable(width=False, height=False)
        
        label_nama_pengguna = tk.Label(registration_window, text="Nama Pengguna:",fg="#ffffff", bg="#06373d", font=('Manage', 11,))
        entry_nama_pengguna = tk.Entry(registration_window, width=25, fg="black", bg="white", font=('Manage', 11))

        label_jabatan = tk.Label(registration_window, text="Jabatan:", fg="#ffffff", bg="#06373d", font=('Manage', 11,))
        self.roles = ['Admin', 'Karyawan']
        self.combo_jabatan = ttk.Combobox(registration_window, values=self.roles, state="readonly", width=23,font=('Manage', 11,))
        
        label_password = tk.Label(registration_window, text="Password:",fg="#ffffff", bg="#06373d", font=('Manage', 11,))
        entry_password = tk.Entry(registration_window, show="*", width=25, fg="black", bg="white", font=('Manage', 11))

        label_nama_pengguna.pack(pady=0)
        entry_nama_pengguna.pack(pady=0)

        label_jabatan.pack(pady=0)
        self.combo_jabatan.pack(pady=0)

        label_password.pack(pady=0)
        entry_password.pack(pady=0)

        register_button = tk.Button(registration_window, text="Register",bg="#1a5186", fg="white", width=22, relief="ridge", borderwidth=3, font=('Manage', 11,), command=lambda: self.register(entry_nama_pengguna.get(), self.combo_jabatan.get(), entry_password.get()))
        register_button.pack(side=tk.TOP,pady=15)


    def register(self, username, jabatan, password):
        if not username or not jabatan or not password:
            messagebox.showwarning("Registration", "Semua kolom harus diisi.")
            return

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='projectpython'
            )

            cursor = connection.cursor()

            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showwarning("Registration", "Username sudah terdaftar. Silahkan login.")
            else:
                cursor.execute("INSERT INTO users (username, password, jabatan ) VALUES (%s, %s, %s)", (username, password, jabatan ))
                connection.commit()
                messagebox.showinfo("Registration", "Registrasi berhasil. Silakan login.")

        except mysql.connector.Error as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Terjadi kesalahan dalam registrasi.")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
