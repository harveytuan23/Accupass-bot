import tkinter as tk
import subprocess


class MyApp:
    def __init__(self, master):
        self.master = master
        master.title("My Program")

        self.label = tk.Label(master, text="Enter key word:")
        self.label.pack()

        self.textbox = tk.Entry(master)
        self.textbox.pack()

        self.button = tk.Button(master, text="Submit", command=self.submit)
        self.button.pack()

    def submit(self):
        text = self.textbox.get()  # Get text from input box
        # Call app.py with input text
        result = subprocess.run(
            ['python', 'app.py', text], capture_output=True)
        print(result.stdout.decode())  # Print output to console


root = tk.Tk()
myapp = MyApp(root)
root.geometry('200x200')
root.mainloop()
