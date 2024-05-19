import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

def toggle_mode():
    global dark_mode
    dark_mode = not dark_mode
    apply_theme()

def apply_theme():
    bg_color = "#333333" if dark_mode else "#f0f0f0"
    fg_color = "white" if dark_mode else "black"
    entry_bg = "#555555" if dark_mode else "white"
    entry_fg = "white" if dark_mode else "black"
    button_bg = "#555555" if dark_mode else "#f0f0f0"
    button_fg = "white" if dark_mode else "black"
    active_bg = "#666666" if dark_mode else "#e0e0e0"

    style.theme_use("clam")
    style.configure("TFrame", background=bg_color)
    style.configure("TLabel", background=bg_color, foreground=fg_color)
    style.configure("TButton", background=button_bg, foreground=button_fg)
    style.configure("TNotebook", background=bg_color)
    style.configure("TNotebook.Tab", background=button_bg, foreground=button_fg)
    style.map("TButton", background=[('active', active_bg)])

    root.config(bg=bg_color)
    
    def update_widget_colors(frame):
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=bg_color)
                update_widget_colors(widget)
            elif isinstance(widget, tk.Label):
                widget.config(bg=bg_color, fg=fg_color)
            elif isinstance(widget, tk.Entry):
                widget.config(bg=entry_bg, fg=entry_fg)
            elif isinstance(widget, tk.Button):
                widget.config(bg=button_bg, fg=button_fg, activebackground=active_bg)

    update_widget_colors(uninstall_frame)
    update_widget_colors(view_all_frame)
    update_widget_colors(install_frame)

def save_account():
    uuid = uuid_entry.get().replace("-", "")
    username = username_entry.get()

    # Check if both UUID and username fields are not empty
    if not uuid or not username:
        messagebox.showerror("Error", "Please enter both UUID and username.")
        return

    file_path = os.path.expanduser('~/.lunarclient/settings/game/accounts.json')

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = {"accounts": {}}
    else:
        data = {"accounts": {}}

    new_account = {
        "accessToken": uuid,
        "accessTokenExpiresAt": "2050-07-02T10:56:30.717167800Z",
        "eligibleForMigration": False,
        "hasMultipleProfiles": False,
        "legacy": True,
        "persistent": True,
        "userProperites": [],
        "localId": uuid,
        "minecraftProfile": {
            "id": uuid,
            "name": username
        },
        "remoteId": uuid,
        "type": "Xbox",
        "username": username
    }

    data['accounts'][uuid] = new_account

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
    messagebox.showinfo("Success", "Account installed successfully.")
    refresh_accounts()
    username_entry.delete(0, tk.END)
    uuid_entry.delete(0, tk.END)


def uninstall_account(uuid):
    file_path = os.path.expanduser('~/.lunarclient/settings/game/accounts.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)

        if 'accounts' in data:
            accounts = data['accounts']

            if uuid in accounts:
                del accounts[uuid]
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)

                messagebox.showinfo("Success", "Account uninstalled successfully.")
                refresh_accounts()
            else:
                messagebox.showinfo("Info", "Account not found.")
        else:
            messagebox.showinfo("Info", "No accounts installed.")
    else:
        messagebox.showinfo("Info", "No accounts installed.")

def refresh_accounts():
    uninstall_frame.destroy()
    view_all_frame.destroy()
    create_uninstall_tab()
    create_view_all_tab()

def create_uninstall_tab():
    global uninstall_frame
    uninstall_frame = ttk.Frame(notebook)
    notebook.add(uninstall_frame, text="Uninstall Accounts")

    file_path = os.path.expanduser('~/.lunarclient/settings/game/accounts.json')
    if (os.path.exists(file_path)):
        with open(file_path, 'r') as file:
            data = json.load(file)

        if 'accounts' in data:
            accounts = data['accounts']

            if accounts:
                tk.Label(uninstall_frame, text="Select an account to uninstall:").pack(pady=5)
                for uuid, account in accounts.items():
                    account_name = account["username"]
                    frame = tk.Frame(uninstall_frame)
                    frame.pack(fill=tk.X, padx=5, pady=2)

                    username_frame = tk.Frame(frame)
                    username_frame.pack()

                    tk.Label(username_frame, text=account_name, width=20, anchor="w").pack(side=tk.LEFT)

                    delete_icon = Image.open("./logos/delete_icon.png")
                    delete_icon = delete_icon.resize((20, 20))
                    delete_icon = ImageTk.PhotoImage(delete_icon)
                    delete_button = tk.Button(username_frame, image=delete_icon, command=lambda u=uuid: uninstall_account(u))
                    delete_button.image = delete_icon
                    delete_button.pack(side=tk.RIGHT)

            else:
                tk.Label(uninstall_frame, text="No accounts installed.").pack(pady=5)
        else:
            tk.Label(uninstall_frame, text="No accounts installed.").pack(pady=5)
    else:
        tk.Label(uninstall_frame, text="No accounts installed.").pack(pady=5)

    mode_button = tk.Button(uninstall_frame, image=dark_white_icon, command=toggle_mode)
    mode_button.place(relx=1, rely=0, anchor='ne', x=-10, y=10)

def create_view_all_tab():
    global view_all_frame
    view_all_frame = ttk.Frame(notebook)
    notebook.add(view_all_frame, text="View All Installed Accounts")

    file_path = os.path.expanduser('~/.lunarclient/settings/game/accounts.json')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)

        if 'accounts' in data:
            accounts = data['accounts']

            if accounts:
                tk.Label(view_all_frame, text="Installed Accounts:").pack(pady=5)
                for uuid, account in accounts.items():
                    account_info = f"Username: {account['username']}"
                    tk.Label(view_all_frame, text=account_info).pack(pady=2)
            else:
                tk.Label(view_all_frame, text="No accounts installed.").pack(pady=5)
        else:
            tk.Label(view_all_frame, text="No accounts installed.").pack(pady=5)

    mode_button = tk.Button(view_all_frame, image=dark_white_icon, command=toggle_mode)
    mode_button.place(relx=1, rely=0, anchor='ne', x=-10, y=10)

def main_menu():
    global notebook, style, dark_mode, root, dark_white_icon, install_frame
    root = tk.Tk()
    root.title("Cracked Lunar Menu")
    root.geometry("600x400")
    root.iconbitmap("./logos/logo.png")  # Set the application icon

    style = ttk.Style()
    dark_mode = True

    dark_white_icon = Image.open("./logos/dark-white.png")
    dark_white_icon = dark_white_icon.resize((30, 30))
    dark_white_icon = ImageTk.PhotoImage(dark_white_icon)

    notebook = ttk.Notebook(root)

    install_frame = ttk.Frame(notebook)
    notebook.add(install_frame, text="Install Account")
    tk.Label(install_frame, text="Username:").pack(pady=5)
    global username_entry
    username_entry = tk.Entry(install_frame)
    username_entry.pack(pady=5)
    tk.Label(install_frame, text="UUID:").pack(pady=5)
    global uuid_entry
    uuid_entry = tk.Entry(install_frame)
    uuid_entry.pack(pady=5)
    install_button = tk.Button(install_frame, text="Install Account", command=save_account)
    install_button.pack(pady=5)
    mode_button = tk.Button(install_frame, image=dark_white_icon, command=toggle_mode)
    mode_button.place(relx=1, rely=0, anchor='ne', x=-10, y=10)

    create_uninstall_tab()
    create_view_all_tab()

    notebook.pack(expand=True, fill="both")
    apply_theme()

    root.mainloop()

if __name__ == "__main__":
    main_menu()
