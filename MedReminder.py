import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

medications = []
reminder_timers = {}  # Dictionary to store reminder timers for each medication
reminder_labels = {}  # Dictionary to store labels displaying time left for each reminder

def open_add_medication_window():
    add_medication_window = tk.Toplevel(window)
    add_medication_window.title("Add Medication")
    add_medication_window.geometry("300x200")

    name_label = tk.Label(add_medication_window, text="Medication Name:")
    name_label.pack()
    name_entry = tk.Entry(add_medication_window)
    name_entry.pack()

    dosage_label = tk.Label(add_medication_window, text="Dosage:")
    dosage_label.pack()
    dosage_entry = tk.Entry(add_medication_window)
    dosage_entry.pack()

    frequency_label = tk.Label(add_medication_window, text="Frequency:")
    frequency_label.pack()
    frequency_entry = tk.Entry(add_medication_window)
    frequency_entry.pack()

    def add_medication():
        name = name_entry.get()
        dosage = dosage_entry.get()
        frequency = frequency_entry.get()
        medications.append({"name": name, "dosage": dosage, "frequency": frequency})
        messagebox.showinfo("Success", "Medication added successfully!")
        name_entry.delete(0, tk.END)
        dosage_entry.delete(0, tk.END)
        frequency_entry.delete(0, tk.END)
        add_medication_window.destroy()

    add_button = tk.Button(add_medication_window, text="Add Medication", command=add_medication)
    add_button.pack()

def view_medication():
    if not medications:
        messagebox.showinfo("Medications", "No medications added yet.")
    else:
        meds_info = "\n".join([f"Name: {med['name']}, Dosage: {med['dosage']}, Frequency: {med['frequency']}" for med in medications])
        messagebox.showinfo("Medications", meds_info)

def set_reminder():
    if not medications:
        messagebox.showinfo("Error", "No medications added yet.")
        return

    reminder_window = tk.Toplevel(window)
    reminder_window.title("Set Reminder")
    reminder_window.geometry("400x300")

    selected_med = tk.StringVar()
    selected_med.set(medications[0]["name"])

    medication_label = tk.Label(reminder_window, text="Select Medication:")
    medication_label.pack()
    medication_optionmenu = tk.OptionMenu(reminder_window, selected_med, *([med["name"] for med in medications]))
    medication_optionmenu.pack()

    def set_reminder_action():
        selected_med_name = selected_med.get()
        for med in medications:
            if med["name"] == selected_med_name:
                frequency_input = med["frequency"].strip().lower()
                if frequency_input.endswith("m"):
                    try:
                        reminder_time = int(frequency_input[:-1]) * 60  # Convert minutes to seconds
                    except ValueError:
                        messagebox.showerror("Error", "Invalid frequency format. Please enter a valid frequency.")
                        return
                elif frequency_input.endswith("h"):
                    try:
                        reminder_time = int(frequency_input[:-1]) * 3600  # Convert hours to seconds
                    except ValueError:
                        messagebox.showerror("Error", "Invalid frequency format. Please enter a valid frequency.")
                        return
                else:
                    try:
                        reminder_time = int(frequency_input) * 3600  # Assume hours if no unit is specified
                    except ValueError:
                        messagebox.showerror("Error", "Invalid frequency format. Please enter a valid frequency.")
                        return

                def show_reminder():
                    messagebox.showinfo("Reminder", f"It's time to take {selected_med_name}!")

                reminder_timers[selected_med_name] = datetime.now() + timedelta(seconds=reminder_time)
                reminder_labels[selected_med_name] = tk.Label(reminder_window, text=f"Time left: {med['frequency']}")
                reminder_labels[selected_med_name].pack()
                update_time_left(selected_med_name)
                messagebox.showinfo("Reminder Set", f"Reminder set for {selected_med_name} every {med['frequency']}.")
                reminder_window.destroy()
                return

    set_reminder_button = tk.Button(reminder_window, text="Set Reminder", command=set_reminder_action)
    set_reminder_button.pack()

def update_time_left(selected_med_name):
    if selected_med_name in reminder_labels:
        current_time = datetime.now()
        time_left = reminder_timers[selected_med_name] - current_time
        time_left_seconds = time_left.total_seconds()
        if time_left_seconds < 0:
            time_left_str = "Time's up!"
        else:
            time_left_hours = time_left_seconds // 3600
            time_left_minutes = (time_left_seconds % 3600) // 60
            time_left_seconds = time_left_seconds % 60
            time_left_str =f"Time left: {int(time_left_hours)}h {int(time_left_minutes)}m {int(time_left_seconds)}s"
        try:
            reminder_labels[selected_med_name].configure(text=time_left_str)
            window.after(1000, lambda: update_time_left(selected_med_name))
        except tk.TclError:
            pass

def delete_reminder():
    if not medications:
        messagebox.showinfo("Error", "No medications added yet.")
        return

    delete_window = tk.Toplevel(window)
    delete_window.title("Delete Reminder")
    delete_window.geometry("400x300")

    selected_med = tk.StringVar()
    selected_med.set(medications[0]["name"])

    medication_label = tk.Label(delete_window, text="Select Medication to Delete Reminder:")
    medication_label.pack()
    medication_optionmenu = tk.OptionMenu(delete_window, selected_med, *([med["name"] for med in medications]))
    medication_optionmenu.pack()

    def delete_selected_med_reminder():
        selected_med_name = selected_med.get()
        if selected_med_name in reminder_timers:
            del reminder_timers[selected_med_name]
            reminder_labels[selected_med_name].destroy()
            del reminder_labels[selected_med_name]
            messagebox.showinfo("Success", f"Reminder for {selected_med_name} deleted successfully!")
        else:
            messagebox.showinfo("Info", f"No reminder set for {selected_med_name}.")

    delete_button = tk.Button(delete_window, text="Delete Reminder", command=delete_selected_med_reminder)
    delete_button.pack()

def mark_taken():
    if not medications:
        messagebox.showinfo("Error", "No medications added yet.")
        return

    taken_window = tk.Toplevel(window)
    taken_window.title("Mark Medication as Taken")
    taken_window.geometry("400x300")

    selected_med = tk.StringVar()
    selected_med.set(medications[0]["name"])

    medication_label = tk.Label(taken_window, text="Select Medication:")
    medication_label.pack()
    medication_optionmenu = tk.OptionMenu(taken_window, selected_med, *([med["name"] for med in medications]))
    medication_optionmenu.pack()

    def mark_as_taken():
        selected_med_name = selected_med.get()
        messagebox.showinfo("Taken", f"{selected_med_name} marked as taken.")

    mark_taken_button = tk.Button(taken_window, text="Mark as Taken", command=mark_as_taken)
    mark_taken_button.pack()

def delete_medication():
    if not medications:
        messagebox.showinfo("Error", "No medications added yet.")
        return

    delete_window = tk.Toplevel(window)
    delete_window.title("Delete Medication")
    delete_window.geometry("400x300")

    selected_med = tk.StringVar()
    selected_med.set(medications[0]["name"])

    medication_label = tk.Label(delete_window, text="Select Medication to Delete:")
    medication_label.pack()
    medication_optionmenu = tk.OptionMenu(delete_window, selected_med, *([med["name"] for med in medications]))
    medication_optionmenu.pack()

    def delete_selected_med():
        selected_med_name = selected_med.get()
        for med in medications:
            if med["name"] == selected_med_name:
                medications.remove(med)
                messagebox.showinfo("Success", f"{selected_med_name} deleted successfully!")
                delete_window.destroy()
                return
        messagebox.showerror("Error", "Failed todelete medication.")

    delete_button = tk.Button(delete_window, text="Delete Medication", command=delete_selected_med)
    delete_button.pack()

window = tk.Tk()
window.title("MedReminder")
window.geometry("400x300")

add_medication_button = tk.Button(window, text="Add Medication", command=open_add_medication_window)
add_medication_button.pack()

view_button = tk.Button(window, text="View Medications", command=view_medication)
view_button.pack()

reminder_button = tk.Button(window, text="Set Reminder", command=set_reminder)
reminder_button.pack()

reminder_list_label = tk.Label(window, text="Reminders:")
reminder_list_label.pack()
reminder_list_frame = tk.Frame(window)
reminder_list_frame.pack()

def update_reminder_list():
    for widget in reminder_list_frame.winfo_children():
        widget.destroy()
    for med_name, timer in reminder_timers.items():
        time_left = timer - datetime.now()
        time_left_seconds = time_left.total_seconds()
        if time_left_seconds < 0:
            time_left_str = "Time's up!"
        else:
            time_left_hours = time_left_seconds // 3600
            time_left_minutes = (time_left_seconds % 3600) // 60
            time_left_seconds = time_left_seconds % 60
            time_left_str = f"Time left: {int(time_left_hours)}h {int(time_left_minutes)}m {int(time_left_seconds)}s"
        reminder_label = tk.Label(reminder_list_frame, text=f"{med_name}: {time_left_str}")
        reminder_label.pack()
    window.after(1000, update_reminder_list)

update_reminder_list()

delete_reminder_button = tk.Button(window, text="Delete Reminder", command=delete_reminder)
delete_reminder_button.pack()

taken_button = tk.Button(window, text="Mark Medication as Taken", command=mark_taken)
taken_button.pack()

delete_medication_button = tk.Button(window, text="Delete Medication", command=delete_medication)
delete_medication_button.pack()

window.mainloop()