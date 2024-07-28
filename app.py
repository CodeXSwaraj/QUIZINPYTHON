import tkinter as tk
from tkinter import messagebox

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz App")
        self.master.geometry("400x300")
        self.score = 0
        self.question_index = 0
        
        self.questions = [
            {"question": "What is the capital of France?", "options": ["Berlin", "Paris", "Madrid", "Rome"], "answer": "Paris"},
            {"question": "What is 5 + 7?", "options": ["10", "11", "12", "13"], "answer": "12"},
            {"question": "What is the color of the sky?", "options": ["Blue", "Green", "Red", "Yellow"], "answer": "Blue"}
        ]
        
        self.question_label = tk.Label(master, text="")
        self.question_label.pack(pady=20)
        
        self.var = tk.StringVar()
        self.option_buttons = []
        for _ in range(4):
            btn = tk.Radiobutton(master, text="", variable=self.var, value="")
            btn.pack(anchor='w')
            self.option_buttons.append(btn)
        
        self.submit_button = tk.Button(master, text="Submit", command=self.submit_answer)
        self.submit_button.pack(pady=20)
        
        self.display_question()
    
    def display_question(self):
        question_data = self.questions[self.question_index]
        self.question_label.config(text=question_data["question"])
        for i, option in enumerate(question_data["options"]):
            self.option_buttons[i].config(text=option, value=option)
        self.var.set(None)
    
    def submit_answer(self):
        selected_option = self.var.get()
        if selected_option:
            correct_answer = self.questions[self.question_index]["answer"]
            if selected_option == correct_answer:
                self.score += 1
            
            self.question_index += 1
            if self.question_index < len(self.questions):
                self.display_question()
            else:
                messagebox.showinfo("Quiz Completed", f"Your score is {self.score}/{len(self.questions)}")
                self.master.quit()
        else:
            messagebox.showwarning("Warning", "Please select an option.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
