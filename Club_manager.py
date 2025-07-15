import tkinter as tk
from tkinter import messagebox
import json
import os

clubs = {}

def load_data():
    global clubs
    if os.path.exists("clubs_data.json"):
        with open("clubs_data.json", "r") as f:
            clubs = json.load(f)

def save_data():
    with open("clubs_data.json", "w") as f:
        json.dump(clubs, f, indent=2)

def custom_ask_string(title, prompt):
    dialog = tk.Toplevel(root, bg="#d1d39d")
    dialog.title(title)
    dialog.geometry("400x150+550+280")
    dialog.resizable(True, True)
    tk.Label(dialog, text=prompt, padx=10, pady=5, bg="#d1d39d").pack(anchor="w")

    entry = tk.Entry(dialog, width=50)
    entry.pack(padx=10, pady=5, fill=tk.X)
    result = [None]

    def on_ok():
        result[0] = entry.get()
        dialog.destroy()

    def on_cancel():
        result[0] = None 
        dialog.destroy()

    btn_frame = tk.Frame(dialog, bg="#d1d39d")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="OK", width=10, command=on_ok, bg="#63a5e8").pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Cancel", width=10, command=on_cancel, bg="#d76a6c").pack(side=tk.LEFT, padx=5)
    dialog.protocol("WM_DELETE_WINDOW", on_cancel)
    dialog.wait_window()
    return result[0]

def show_frame(frame):
    frame.tkraise()

root = tk.Tk()
root.title("School Club Manager")
root.geometry("530x650")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.configure(bg="#edc5db")  

main_menu = tk.Frame(root, bg="#edc5db") 
main_menu.grid(row=0, column=0, sticky="nsew")
main_center = tk.Frame(main_menu, bg="#edc5db") 
main_center.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(main_center, text="Welcome to School Club Manager", font=("Georgia", 18), bg="#c584b6").pack(pady=10)

tk.Button(main_center, text="Create New Club", height=2, width=25, font=("Georgia", 12), bg="#358ee8", fg="white",
          command=lambda: show_frame(create_club)).pack(pady=10)

tk.Button(main_center, text="Join a Club", height=2, width=25, font=("Georgia", 12), bg="#ed30a1", fg="white",
          command=lambda: [refresh_club_list(), show_frame(join_club)]).pack(pady=10)

create_club = tk.Frame(root, bg="#98bf92")
create_club.grid(row=0, column=0, sticky="nsew")
create_club.columnconfigure(0, weight=1)
create_club.rowconfigure(0, weight=1)

tk.Label(create_club, text="Create a Club", font=("Georgia", 16), bg="#f9fbf8").pack(pady=10)
tk.Label(create_club, text="* Do not add 'club' at the end.", fg="gray", bg="#a2be9d").pack()

entry_name = tk.Entry(create_club, width=55)
entry_desc = tk.Entry(create_club, width=55)
entry_leader = tk.Entry(create_club, width=55)
entry_leader_id = tk.Entry(create_club, width=55)
entry_co_leader = tk.Entry(create_club, width=55) 
entry_co_leader_id = tk.Entry(create_club, width=55)
entry_max = tk.Entry(create_club, width=40)

for label, entry in [
    ("Club Name", entry_name),
    ("Description", entry_desc),
    ("Leader Name", entry_leader),
    ("Leader ID", entry_leader_id),
    ("Co-Leader Name", entry_co_leader),
    ("Co-Leader ID", entry_co_leader_id),
    ("Max Members", entry_max)
]:
    tk.Label(create_club, text=label, height=1, width=14, bg="#079E52", fg="#F6F9F7").pack()
    entry.pack()

def create():
    name = entry_name.get().strip()
    key = (name + " Club").lower()
    if not name:
        messagebox.showwarning("Missing", "Club name cannot be empty.")
        return
    if key in clubs:
        messagebox.showwarning("Exists", "Club already exists.")
        return
    if name.lower().endswith("club"):
        messagebox.showwarning("Naming Tip", "Please do not include the word 'club' in the name.")
        return
    if not entry_desc.get().strip():
        messagebox.showwarning("Missing Info", "Please enter a description.")
        return
    if not entry_leader.get().strip():
        messagebox.showwarning("Missing Info", "Please enter the leader's name.")
        return
    if not entry_leader_id.get().strip():
        messagebox.showwarning("Missing Info", "Please enter the leader's ID.")
        return
    if not entry_co_leader.get().strip():
        messagebox.showwarning("Missing Info", "Please enter the co-leader's name.")
        return
    if not entry_co_leader_id.get().strip():
        messagebox.showwarning("Missing Info", "Please enter the co-leader's ID.")
        return
    try:
        max_members = int(entry_max.get().strip())
        if max_members < 10:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid", "Please enter a number >= 10 for max members.")
        return
    
    clubs[key] = {
        "name": name + " Club",
        "description": entry_desc.get().strip(),
        "leader": entry_leader.get().strip(),
        "leader_id": entry_leader_id.get().strip(),
        "co_leader": entry_co_leader.get().strip(),
        "co_leader_id": entry_co_leader_id.get().strip(),
        "max_members": max_members,
        "members": [],
        "activities": []
    }
    save_data()
    messagebox.showinfo("Created", f"'{name}' club created successfully!")
    for e in [entry_name, entry_desc, entry_leader, entry_leader_id, entry_co_leader, entry_co_leader_id, entry_max]:
        e.delete(0, tk.END)
        
def delete_club():
    club_name = custom_ask_string("Delete Club", "Enter club name to delete:")
    if not club_name:
        return
    key = (club_name.strip() + " Club").lower()
    if key not in clubs:
        messagebox.showerror("Error", "Club not found.")
        return
    uid = custom_ask_string("Your ID", "Enter your leader/co-leader ID:")
    if not uid:
        return
    if uid not in (clubs[key]['leader_id'], clubs[key]['co_leader_id']):
        messagebox.showerror("Access Denied", "Only leaders/co-leaders can delete the club.")
        return
    if messagebox.askyesno("Confirm", f"Are you sure you want to delete '{club_name}' club?"):
        del clubs[key]
        save_data()
        refresh_club_list()
        details_text.config(state="normal")
        details_text.delete(1.0, tk.END)
        details_text.config(state="disabled") 
        messagebox.showinfo("Deleted", f"'{club_name}' has been deleted.")

def add_activity():
    club_name = custom_ask_string("Club Name", "Enter the name of your club (no 'club' at the end):")
    if not club_name:
        return
    key = (club_name.strip() + " Club").lower()
    if key not in clubs:
        messagebox.showerror("Not Found", "Club not found.")
        return
    user_id = custom_ask_string("Leader/Co-Leader ID", "Enter your student ID:")
    if not user_id:
        return
    if user_id not in (clubs[key]['leader_id'], clubs[key]['co_leader_id']):
        messagebox.showerror("Access Denied", "Only the leader or co-leader can add activities.")
        return
    title = custom_ask_string("Activity Title", "Enter activity title:").strip()
    date = custom_ask_string("Activity Date and place", "Enter date and place (e.g., 2025-08-01(Room 5)):").strip()
    desc = custom_ask_string("Activity Description", "Enter activity description:").strip()
    if not title or not date or not desc:
        messagebox.showwarning("Missing Info", "All fields (title, date/place, description) are required.")
        return

    clubs[key]["activities"].append({
        "title": title,
        "date & place": date,
        "description": desc})
    save_data()
    messagebox.showinfo("Added", f"Activity added to {clubs[key]['name']}.")
        
def delete_activity():
    club_name = custom_ask_string("Club Name", "Enter your club name:")
    if not club_name:
        return
    key = (club_name.strip() + " Club").lower()
    if key not in clubs:
        messagebox.showerror("Not Found", "Club not found.")
        return
    uid = custom_ask_string("Your ID", "Enter your leader/co-leader ID:")
    if not uid:
        return
    if uid not in (clubs[key]['leader_id'], clubs[key]['co_leader_id']):
        messagebox.showerror("Access Denied", "Only leaders/co-leaders can delete activities.")
        return
    title = custom_ask_string("Activity Title", "Enter the title of activity to delete:")
    c = clubs[key]
    for a in c['activities']:
        if a['title'].lower() == title.lower():
            c['activities'].remove(a)
            save_data()
            messagebox.showinfo("Deleted", f"Activity '{title}' removed.")
            return
    messagebox.showinfo("Not Found", "Activity not found.")

button_font = ("Georgia", 9)
tk.Button(create_club, text="Create Club", command=create, bg="#dde411", height=1, width=14, font=button_font).pack(pady=10)
tk.Button(create_club, text="Delete Club", command=delete_club, bg="#77e37c", height=1, width=14, font=button_font).pack(pady=5)
tk.Button(create_club, text="Add Activity to Club", command=add_activity, bg="#80eedf", height=1, width=17, font=button_font).pack(pady=5)
tk.Button(create_club, text="Delete Activity", command=delete_activity, bg="#edac5d", height=1, width=14, font=button_font).pack(pady=5)
tk.Button(create_club, text="Back to Menu", command=lambda: show_frame(main_menu), bg="#d94f4f", height=1, width=14, font=button_font).pack(pady=10)


join_club = tk.Frame(root, bg="#7cc8cf")
join_club.grid(row=0, column=0, sticky="nsew")
join_club.columnconfigure(0, weight=1)
join_club.rowconfigure(0, weight=1)
tk.Label(join_club, text="Join Club", font=("Georgia", 16)).pack(pady=10)

def refresh_club_list():
    listbox.delete(0, tk.END)
    for club in clubs.values():
        listbox.insert(tk.END, club['name'])
    save_data()

def show_details():
    sel = listbox.curselection()
    if not sel:
        details_text.config(state="normal")
        details_text.delete(1.0, tk.END)
        details_text.config(state="disabled")
        return

    name = listbox.get(sel[0]).strip()
    key = name.lower()  
    if key not in clubs:
        messagebox.showerror("Error", f"Club '{name}' not found.\nKey tried: '{key}'")
        return

    c = clubs[key]
    details_text.config(state="normal")  
    details_text.delete(1.0, tk.END) 

    details_text.insert(tk.END, f"Description: {c['description']}\n")
    details_text.insert(tk.END, f"Leader: {c['leader']}\n")
    details_text.insert(tk.END, f"Co-Leader: {c['co_leader']}\n")
    details_text.insert(tk.END, f"Members: {len(c['members'])}/{c['max_members']}\n")
    details_text.insert(tk.END, "Activities:\n")

    if c['activities']:
        for activity in c['activities']:
            details_text.insert(tk.END, f"Title: {activity['title']} | Date & Place: {activity['date & place']} | Description: {activity['description']}\n")
    else:
        details_text.insert(tk.END, "No activities yet.\n")
    
    details_text.config(state="disabled")
    save_data()

def join_selected_club():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("Select", "Select a club first.")
        return

    key = listbox.get(sel[0]).lower()
    c = clubs[key]
    if len(c['members']) >= c['max_members']:
        messagebox.showinfo("Full", "This club is full.")
        return

    while True:
        name = custom_ask_string("Name", "Enter your full name:")
        if name is None:
            messagebox.showinfo("Canceled", "Joining canceled.")
            return
        if name.strip() == "":
            messagebox.showwarning("Input Required", "Please enter your name to continue.")
        else:
            break  
        
    while True:
        sid = custom_ask_string("ID", "Enter your student ID:")
        if sid is None:
            messagebox.showinfo("Canceled", "Joining canceled.")
            return
        if sid.strip() == "":
            messagebox.showwarning("Input Required", "Please enter your student ID.")
        elif any(m['id'] == sid for m in c['members']):
            messagebox.showinfo("Exists", "This student ID already joined.")
        else:
            break 

    while True:
        reason = custom_ask_string("Purpose", "Why join this club?")
        if reason is None:
            messagebox.showinfo("Canceled", "Joining canceled.")
            return
        if reason.strip() == "":
            messagebox.showwarning("Input Required", "Please enter a reason.")
        else:
            break 
    c['members'].append({"name": name, "id": sid, "purpose": reason})
    messagebox.showinfo("Joined", f"{name} joined {c['name']}!")
    save_data()
    
def view_members():
    club_name = custom_ask_string("Club Name", "Enter your club name (no 'club' at the end):")
    if not club_name:
        return
    key = (club_name.strip() + " Club").lower()
    if key not in clubs:
        messagebox.showerror("Error", "Club not found.")
        return

    uid = custom_ask_string("ID", "Enter your leader/co-leader ID:")
    if not uid:
        return
    if uid not in (clubs[key]['leader_id'], clubs[key]['co_leader_id']):
        messagebox.showerror("Access Denied", "Only the leader or co-leader can view members.")
        return

    mems = clubs[key]['members']
    if not mems:
        messagebox.showinfo("Members", "No members yet.")
        return
    
    win = tk.Toplevel(root)
    win.title(f"Members of {clubs[key]['name']}")
    win.geometry("450x350+550+250")
    win.configure(bg="#d3bbbb")
    tk.Label(win, text="Member list", bg="#f2f2f2", font=("Arial", 12)).pack(pady=5)

    list_frame = tk.Frame(win)
    list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    v_scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    h_scrollbar = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    member_list = tk.Listbox(list_frame, width=60, height=12, yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    member_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    v_scrollbar.config(command=member_list.yview)
    h_scrollbar.config(command=member_list.xview)

    for m in mems:
        member_list.insert(tk.END, f"{m['name']} | ID:{m['id']} | Reason: {m['purpose']}")

    def delete_selected():
        sel = member_list.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a member to remove.")
            return
        index = sel[0]
        member = mems[index]
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete {member['name']}?")
        if confirm:
            del mems[index]
            save_data()
            member_list.delete(index)
            messagebox.showinfo("Deleted", f"{member['name']} removed.")

    tk.Button(win, text="Delete member", bg="#e57373", command=delete_selected).pack(pady=5)
    tk.Button(win, text="Close", bg="#cccccc", command=win.destroy).pack(pady=5)
    
top = tk.Frame(join_club)
top.pack(fill=tk.X, padx=10, pady=5)
tk.Label(top, text="Available Clubs", font=("Georgia", 14), bg="#30edca").pack(side=tk.LEFT)
tk.Button(top, text="View Members' details (Leaders Only)", command=view_members, bg="#01080d", fg="white").pack(side=tk.RIGHT)

list_frame = tk.Frame(join_club)
list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
listbox = tk.Listbox(list_frame, xscrollcommand=True)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll_y = tk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x = tk.Scrollbar(join_club, orient="horizontal", command=listbox.xview)
scroll_x.pack(fill=tk.X, padx=10)
listbox.config(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

details_text = tk.Text(join_club, wrap="word", height=8, width=50, font=("Times New Roman", 10), bg="#f9f9f9")
details_text.pack(pady=10, padx=10)
scrollbar = tk.Scrollbar(join_club, command=details_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
details_text.config(yscrollcommand=scrollbar.set)

tk.Button(join_club, text="Refresh List", command=refresh_club_list, height=1, width=14, font=("Georgia", 9), bg="#b7d189").pack(pady=5)
tk.Button(join_club, text="View club details", command=show_details, height=1, width=17, font=("Georgia", 9), bg="#00cca7").pack(pady=5)
tk.Button(join_club, text="Join Club", command=join_selected_club, height=1, width=14, font=("Georgia", 9), bg="#cf8bb3").pack(pady=5)
tk.Button(join_club, text="Back to Menu", command=lambda: show_frame(main_menu), height=1, width=14, font=("Georgia", 9), bg="#d94f4f").pack(pady=10)

load_data()
show_frame(main_menu)
root.mainloop()