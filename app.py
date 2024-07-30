import tkinter as tk
from tkinter import ttk, messagebox
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
        self.categories = []
        self.time_left = 15  # seconds for each question
        self.timer = None

        # Fetch categories from API
        self.fetch_categories()
        
        # Creating widgets for category selection
        self.create_category_widgets()
        
    def fetch_categories(self):
        try:
            response = requests.get("https://opentdb.com/api_category.php")
            data = response.json()
            self.categories = data["trivia_categories"]
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching categories: {e}")
    
    def create_category_widgets(self):
        self.category_label = tk.Label(self.master, text="Select a Category", font=('Arial', 16))
        self.category_label.pack(pady=20)
        
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.master, textvariable=self.category_var, font=('Arial', 14))
        self.category_dropdown['values'] = [category['name'] for category in self.categories]
        self.category_dropdown.current(0)  # set the selected item
        self.category_dropdown.pack(pady=10)
        
        self.start_button = tk.Button(self.master, text="Start Quiz", command=self.start_quiz, font=('Arial', 14), bg="#4caf50", fg="white")
        self.start_button.pack(pady=20)
    
    def start_quiz(self):
        selected_category = self.category_var.get()
        category_id = next((cat['id'] for cat in self.categories if cat['name'] == selected_category), None)
        if category_id:
            self.fetch_questions(category_id)
        else:
            messagebox.showerror("Error", "Invalid category selected.")
    
    def fetch_questions(self, category_id):
        try:
            response = requests.get(f"https://opentdb.com/api.php?amount=10&category={category_id}&type=multiple")
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
                
                # Remove category selection widgets and start quiz
                self.category_label.pack_forget()
                self.category_dropdown.pack_forget()
                self.start_button.pack_forget()
                self.create_widgets()
                self.display_question()
            else:
                messagebox.showerror("Error", "Could not fetch questions. Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching questions: {e}")
    
    def create_widgets(self):
        # Question label
        self.question_label = tk.Label(self.master, text="", font=('Arial', 16, 'bold'), wraplength=500, justify="center", bg="#f0f0f0")
        self.question_label.pack(pady=20)
        
        # Timer label
        self.timer_label = tk.Label(self.master, text=f"Time left: {self.time_left} seconds", font=('Arial', 12), bg="#f0f0f0")
        self.timer_label.pack(pady=10)
        
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
        
        # Progress label
        self.progress_label = tk.Label(self.master, text=f"Question 1/{len(self.questions)}", font=('Arial', 12), bg="#f0f0f0")
        self.progress_label.pack(side='bottom', pady=10)

    def display_question(self):
        if self.timer:
            self.master.after_cancel(self.timer)
        
        self.time_left = 15
        self.update_timer()
        
        question_data = self.questions[self.question_index]
        self.question_label.config(text=question_data["question"])
        for i, option in enumerate(question_data["options"]):
            self.option_buttons[i].config(text=option, value=option, bg="#e1e1e1")
        self.var.set(None)
        self.update_progress()
    
    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left} seconds")
            self.time_left -= 1
            self.timer = self.master.after(1000, self.update_timer)
        else:
            self.submit_answer(timer_expired=True)

    def update_progress(self):
        current_question = self.question_index + 1
        total_questions = len(self.questions)
        self.progress_label.config(text=f"Question {current_question}/{total_questions}")

    def submit_answer(self, timer_expired=False):
        selected_option = self.var.get()
        if timer_expired:
            messagebox.showinfo("Time's up!", "Time ran out for this question.")
        else:
            if selected_option:
                correct_answer = self.questions[self.question_index]["answer"]
                if selected_option == correct_answer:
                    self.score += 1
                    messagebox.showinfo("Correct!", "That's the correct answer!", icon='info')
                    self.question_label.config(bg="#dff0d8")
                else:
                    messagebox.showerror("Incorrect", f"Wrong answer. The correct answer was {correct_answer}.")
                    self.question_label.config(bg="#f8d7da")
            else:
                messagebox.showwarning("Warning", "Please select an option.")
        
        self.question_index += 1
        if self.question_index < len(self.questions):
            self.display_question()
        else:
            self.show_results()

    def show_results(self):
        if self.timer:
            self.master.after_cancel(self.timer)
        messagebox.showinfo("Quiz Completed", f"Your score is {self.score}/{len(self.questions)}")
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
