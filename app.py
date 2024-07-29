import tkinter as tk
from tkinter import messagebox

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz App")
        self.master.geometry("600x400")
        self.master.resizable(False, False)
        
        self.score = 0
        self.question_index = 0
        
        # Questions data
        self.questions = [
            {
                "question": "What is the capital of France?", 
                "options": ["Berlin", "Paris", "Madrid", "Rome"], 
                "answer": "Paris"
            },
            {
                "question": "What is 5 + 7?", 
                "options": ["10", "11", "12", "13"], 
                "answer": "12"
            },
            {
                "question": "What is the color of the sky?", 
                "options": ["Blue", "Green", "Red", "Yellow"], 
                "answer": "Blue"
            },
            {
                "question": "Which planet is known as the Red Planet?", 
                "options": ["Earth", "Mars", "Jupiter", "Saturn"], 
                "answer": "Mars"
            },
            {
                "question": "Who wrote 'Hamlet'?", 
                "options": ["Charles Dickens", "Jane Austen", "William Shakespeare", "Mark Twain"], 
                "answer": "William Shakespeare"
            },
            {
                "question": "What is the largest mammal?", 
                "options": ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"], 
                "answer": "Blue Whale"
            },
            {
                "question": "Which element has the chemical symbol 'O'?", 
                "options": ["Gold", "Oxygen", "Osmium", "Zinc"], 
                "answer": "Oxygen"
            },
            {
                "question": "In which year did the Titanic sink?", 
                "options": ["1912", "1905", "1915", "1920"], 
                "answer": "1912"
            },
            {
                "question": "What is the smallest prime number?", 
                "options": ["0", "1", "2", "3"], 
                "answer": "2"
            },
            {
                "question": "Which country is known as the Land of the Rising Sun?", 
                "options": ["China", "South Korea", "Japan", "Vietnam"], 
                "answer": "Japan"
            }
        ]
        
        # Creating widgets
        self.create_widgets()
        self.display_question()

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
