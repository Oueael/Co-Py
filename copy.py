import pyperclip
import tkinter as tk
import keyboard

# Dictionary to store link sets
link_sets = {}

# Counter to create unique names for each set
set_counter = 1

def copy_links_to_clipboard(links, set_name):
    if links:
        links_text = '\n'.join(links)
        pyperclip.copy(links_text)
        link_sets[set_name][1].config(text=f"Copied: {links_text}")  # Update current copy text
        status_label.config(text=f"Links copied from {set_name}")
    else:
        status_label.config(text=f"{set_name} is empty!")

def update_current_links_display():
    for set_name, (_, links_label, links) in link_sets.items():
        links_label.config(text=f"Current: {links[0] if links else 'No link available'}")

def adjust_window_size():
    # Adjust height dynamically based on the number of sets
    base_height = 300  # Base height for fixed elements
    additional_height = len(link_sets) * 80  # Height per set
    new_height = base_height + additional_height
    root.geometry(f"400x{new_height}")

def add_new_set():
    global set_counter
    if set_counter > 10:
        status_label.config(text="Maximum of 10 sets reached!")
        return

    set_name = f"Set {set_counter}"
    set_counter += 1

    # Add a new set with an empty list
    current_links = []
    links_label = tk.Label(root, text=f"Current: No link available")
    copied_label = tk.Label(root, text="Copied: None", fg="gray")

    copy_button = tk.Button(root, text=f"Copy {set_name}", command=lambda: copy_links_to_clipboard(current_links, set_name))
    update_button = tk.Button(root, text=f"Update {set_name}", command=lambda: update_set_links(set_name))
    delete_button = tk.Button(root, text=f"Delete {set_name}", command=lambda: delete_set(set_name, links_label, copied_label, copy_button, update_button, delete_button))

    # Pack the widgets
    copy_button.pack(pady=5)
    links_label.pack()
    copied_label.pack()
    update_button.pack(pady=5)
    delete_button.pack(pady=5)

    link_sets[set_name] = (copy_button, links_label, current_links)
    adjust_window_size()

def update_set_links(set_name):
    new_link = link_input.get()
    if new_link:
        link_sets[set_name][2].append(new_link)  # Append the new link to the set
        update_current_links_display()

def delete_set(set_name, *widgets):
    for widget in widgets:
        widget.destroy()
    del link_sets[set_name]  # Remove the set from the dictionary
    adjust_window_size()

# Create the main window
root = tk.Tk()
root.title("Co Py")

# Set the initial window size
root.geometry("400x300")

# Label for the keyboard shortcuts
shortcut_label = tk.Label(
    root,
    text=(
        "Keyboard Shortcuts:\n"
        "Ctrl+1 = Copy Set 1\n"
        "Ctrl+2 = Copy Set 2\n"
        "Ctrl+3 = Copy Set 3\n"
        "etc.\n"
        "Ctrl+0 = Copy Set 10"
    ),
    anchor="w"
)
shortcut_label.pack(pady=10)

# Create a button to add new sets
add_set_button = tk.Button(root, text="Add New Set", command=add_new_set)
add_set_button.pack(pady=10)

# Create a Text Entry box for editing the links
link_input = tk.Entry(root, width=40)
link_input.pack(pady=10)

# Create a status label to display the result of the action
status_label = tk.Label(root, text="Click a button to copy links or use shortcuts", anchor="w")
status_label.pack(pady=20)

# Create an exit button
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=10)

# Function to assign hotkeys dynamically
def assign_hotkeys():
    for i in range(1, 11):
        set_name = f"Set {i}"
        keyboard.add_hotkey(f'ctrl+{i % 10}', lambda s=set_name: copy_links_to_clipboard(link_sets[s][2], s) if s in link_sets else None)

# Assign hotkeys
assign_hotkeys()

# Start the Tkinter event loop
root.mainloop()
