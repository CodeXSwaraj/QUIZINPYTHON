import tkinter as tk
from tkinter import messagebox
import requests
import html

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz App")
        self.master.geometry("600x400")
        self.master.resizable(False, False)
        
        self.score = 0
        self.question_index = 0
        self.questions = []
        
        # Fetch questions from API
        self.fetch_questions()
        
        # Creating widgets
        self.create_widgets()
        
        if self.questions:
            self.display_question()

    def fetch_questions(self):
        try:
            response = requests.get("https://opentdb.com/api.php?amount=10&type=multiple")
            data = response.json()
            if data["response_code"] == 0:
                for item in data["results"]:
                    question = {
                        "question": html.unescape(item["question"]),
                        "options": [html.unescape(opt) for opt in item["incorrect_answers"]] + [html.unescape(item["correct_answer"])],
                        "answer": html.unescape(item["correct_answer"])
                    }
                    # Shuffle the options to randomize their order
                    import random
                    random.shuffle(question["options"])
                    self.questions.append(question)
            else:
                messagebox.showerror("Error", "Could not fetch questions. Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def create_widgets(self):
        # Question label
        self.question_label = tk.Label(self.master, text="", font=('Arial', 16, 'bold'), wraplength=500, justify="center", bg="#f0f0f0")
        self.question_label.pack(pady=20)
        
        # Options (Radio buttons)
        self.var = tk.StringVar()
        self.option_buttons = []
        for _ in range(4):
            btn = tk.Radiobutton(self.master, text="", variable=self.var, value="", font=('Arial', 14), anchor='w', padx=10, bg="#e1e1e1")
            btn.pack(fill='x', padx=20, pady=5)
            self.option_buttons.append(btn)
        
        # Submit button
        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit_answer, font=('Arial', 14), bg="#4caf50", fg="white")
        self.submit_button.pack(pady=20)
        
        # Progress bar
        self.progress_label = tk.Label(self.master, text=f"Question 1/{len(self.questions)}", font=('Arial', 12), bg="#f0f0f0")
        self.progress_label.pack(side='bottom', pady=10)

    def display_question(self):
        question_data = self.questions[self.question_index]
        self.question_label.config(text=question_data["question"])
        for i, option in enumerate(question_data["options"]):
            self.option_buttons[i].config(text=option, value=option, bg="#e1e1e1")
        self.var.set(None)
        self.update_progress()

    def update_progress(self):
        current_question = self.question_index + 1
        total_questions = len(self.questions)
        self.progress_label.config(text=f"Question {current_question}/{total_questions}")

    def submit_answer(self):
        selected_option = self.var.get()
        if selected_option:
            correct_answer = self.questions[self.question_index]["answer"]
            if selected_option == correct_answer:
                self.score += 1
                messagebox.showinfo("Correct!", "That's the correct answer!", icon='info')
                self.question_label.config(bg="#dff0d8")
            else:
                messagebox.showerror("Incorrect", f"Wrong answer. The correct answer was {correct_answer}.")
                self.question_label.config(bg="#f8d7da")
            
            self.question_index += 1
            if self.question_index < len(self.questions):
                self.display_question()
            else:
                self.show_results()
        else:
            messagebox.showwarning("Warning", "Please select an option.")

    def show_results(self):
        messagebox.showinfo("Quiz Completed", f"Your score is {self.score}/{len(self.questions)}")
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
