import os
import paramiko
import tkinter as tk
from tkinter import messagebox, ttk

# Function to establish SSH connection
def connect_ssh():
    global ssh
    username = username_var.get()
    password = password_var.get()
    host = host_var.get()
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)
        messagebox.showinfo("Success", "Connected successfully!")
        # Close login window and open the file manager
        login_window.withdraw()
        open_file_manager()
    except Exception as e:
        messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")

# Function to open the file manager window
def open_file_manager():
    global file_manager_window
    file_manager_window = tk.Toplevel(root)
    file_manager_window.title("File Manager")

    # Left Pane: Local Directory
    left_pane = tk.Frame(file_manager_window)
    left_pane.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    local_dir_label = tk.Label(left_pane, text="Local Directory:")
    local_dir_label.pack(anchor="w")

    global local_dir_var
    local_dir_var = tk.StringVar(value=os.getcwd())
    local_dir_entry = tk.Entry(left_pane, textvariable=local_dir_var, width=50)
    local_dir_entry.pack(anchor="w")
    local_dir_entry.bind("<Return>", lambda event: list_local_files(local_dir_var.get()))

    global local_listbox
    local_listbox = tk.Listbox(left_pane)
    local_listbox.pack(fill=tk.BOTH, expand=True)
    list_local_files(local_dir_var.get())

    # Right Pane: Remote Directory
    right_pane = tk.Frame(file_manager_window)
    right_pane.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    remote_dir_label = tk.Label(right_pane, text="Remote Directory:")
    remote_dir_label.pack(anchor="w")

    global remote_dir_var
    remote_dir_var = tk.StringVar(value="/")
    remote_dir_entry = tk.Entry(right_pane, textvariable=remote_dir_var, width=50)
    remote_dir_entry.pack(anchor="w")
    remote_dir_entry.bind("<Return>", lambda event: list_remote_files(remote_dir_var.get()))

    global remote_listbox
    remote_listbox = tk.Listbox(right_pane)
    remote_listbox.pack(fill=tk.BOTH, expand=True)
    list_remote_files(remote_dir_var.get())

    file_manager_window.grid_columnconfigure(0, weight=1)
    file_manager_window.grid_columnconfigure(1, weight=1)
    file_manager_window.grid_rowconfigure(0, weight=1)

# Function to list local files
def list_local_files(path):
    try:
        local_listbox.delete(0, tk.END)
        for file in os.listdir(path):
            local_listbox.insert(tk.END, file)
        local_dir_var.set(path)
    except Exception as e:
        messagebox.showerror("Error", f"Unable to list local directory: {str(e)}")

# Function to list remote files
def list_remote_files(path):
    try:
        remote_listbox.delete(0, tk.END)
        stdin, stdout, stderr = ssh.exec_command(f'ls -1 {path}')
        for line in stdout.readlines():
            remote_listbox.insert(tk.END, line.strip())
        remote_dir_var.set(path)
    except Exception as e:
        messagebox.showerror("Error", f"Unable to list remote directory: {str(e)}")

# Main Application Window
root = tk.Tk()
root.withdraw()  # Hide the root window, we'll use a login window

# Login Window
login_window = tk.Toplevel(root)
login_window.title("SSH Login")

username_var = tk.StringVar()
password_var = tk.StringVar()
host_var = tk.StringVar()

tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(login_window, textvariable=username_var)
username_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(login_window, textvariable=password_var, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(login_window, text="Host:").grid(row=2, column=0, padx=10, pady=10)
host_entry = tk.Entry(login_window, textvariable=host_var)
host_entry.grid(row=2, column=1, padx=10, pady=10)

login_button = tk.Button(login_window, text="Login", command=connect_ssh)
login_button.grid(row=3, columnspan=2, pady=10)

root.mainloop()