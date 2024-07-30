import tkinter as tk
from tkinter import ttk, messagebox
import requests
import html
import random

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz App")
        self.master.geometry("600x450")
        self.master.config(bg="#2c3e50")
        self.master.resizable(False, False)
        
        self.score = 0
        self.question_index = 0
        self.questions = []
        self.categories = [{'id': 999, 'name': 'India'}]  # Adding custom India category
        self.time_left = 15  # seconds for each question
        self.timer = None

        # Fetch categories from API and add custom category
        self.fetch_categories()
        
        # Creating widgets for category selection
        self.create_category_widgets()
        
    def fetch_categories(self):
        try:
            response = requests.get("https://opentdb.com/api_category.php")
            data = response.json()
            self.categories.extend(data["trivia_categories"])  # Append existing categories
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching categories: {e}")
    
    def create_category_widgets(self):
        self.category_label = tk.Label(self.master, text="Select a Category", font=('Arial', 16, 'bold'), fg="#ecf0f1", bg="#2c3e50")
        self.category_label.pack(pady=20)
        
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.master, textvariable=self.category_var, font=('Arial', 14))
        self.category_dropdown['values'] = [category['name'] for category in self.categories]
        self.category_dropdown.current(0)  # set the selected item
        self.category_dropdown.pack(pady=10)
        
        self.start_button = tk.Button(self.master, text="Start Quiz", command=self.start_quiz, font=('Arial', 14, 'bold'), bg="#27ae60", fg="white", cursor="hand2", activebackground="#2ecc71")
        self.start_button.pack(pady=20)
    
    def start_quiz(self):
        selected_category = self.category_var.get()
        if selected_category == 'India':
            self.load_india_questions()
        else:
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
                    random.shuffle(question["options"])
                    self.questions.append(question)
                
                self.category_label.pack_forget()
                self.category_dropdown.pack_forget()
                self.start_button.pack_forget()
                self.create_widgets()
                self.display_question()
            else:
                messagebox.showerror("Error", "Could not fetch questions. Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching questions: {e}")
    
    def load_india_questions(self):
        self.questions = [
            {
                "question": "What is the capital of India?",
                "options": ["New Delhi", "Mumbai", "Kolkata", "Chennai"],
                "answer": "New Delhi"
            },
            {
                "question": "Who is known as the Father of the Indian Nation?",
                "options": ["Jawaharlal Nehru", "Mahatma Gandhi", "Sardar Patel", "Subhas Chandra Bose"],
                "answer": "Mahatma Gandhi"
            },
            {
                "question": "Which Indian state has the longest coastline?",
                "options": ["Gujarat", "Tamil Nadu", "Maharashtra", "Andhra Pradesh"],
                "answer": "Gujarat"
            },
            {
                "question": "Who wrote the Indian national anthem?",
                "options": ["Rabindranath Tagore", "Bankim Chandra Chatterjee", "Sarojini Naidu", "Mahatma Gandhi"],
                "answer": "Rabindranath Tagore"
            },
            {
                "question": "In which year did India gain independence?",
                "options": ["1947", "1950", "1945", "1935"],
                "answer": "1947"
            }
        ]
        self.category_label.pack_forget()
        self.category_dropdown.pack_forget()
        self.start_button.pack_forget()
        self.create_widgets()
        self.display_question()
    
    def create_widgets(self):
        self.question_label = tk.Label(self.master, text="", font=('Arial', 16, 'bold'), wraplength=500, justify="center", bg="#34495e", fg="#ecf0f1", bd=10, relief="groove")
        self.question_label.pack(pady=20)
        
        self.timer_label = tk.Label(self.master, text=f"Time left: {self.time_left} seconds", font=('Arial', 12, 'bold'), bg="#34495e", fg="#ecf0f1")
        self.timer_label.pack(pady=10)
        
        self.var = tk.StringVar()
        self.option_buttons = []
        for _ in range(4):
            btn = tk.Radiobutton(self.master, text="", variable=self.var, value="", font=('Arial', 14), anchor='w', padx=10, bg="#34495e", fg="#ecf0f1", selectcolor="#1abc9c", activebackground="#34495e", activeforeground="#1abc9c", cursor="hand2")
            btn.pack(fill='x', padx=20, pady=5)
            self.option_buttons.append(btn)
        
        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit_answer, font=('Arial', 14, 'bold'), bg="#e74c3c", fg="white", cursor="hand2", activebackground="#c0392b")
        self.submit_button.pack(pady=20)
        
        self.progress_label = tk.Label(self.master, text=f"Question 1/{len(self.questions)}", font=('Arial', 12, 'bold'), bg="#34495e", fg="#ecf0f1")
        self.progress_label.pack(side='bottom', pady=10)

    def display_question(self):
        if self.timer:
            self.master.after_cancel(self.timer)
        
        self.time_left = 15
        self.update_timer()
        
        question_data = self.questions[self.question_index]
        self.question_label.config(text=question_data["question"], bg="#34495e")
        for i, option in enumerate(question_data["options"]):
            self.option_buttons[i].config(text=option, value=option, bg="#34495e", state=tk.NORMAL)
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
                    self.question_label.config(bg="#27ae60")
                    messagebox.showinfo("Correct!", "That's the correct answer!")
                else:
                    self.question_label.config(bg="#e74c3c")
                    messagebox.showerror("Incorrect", f"Wrong answer. The correct answer was {correct_answer}.")
            else:
                messagebox.showwarning("Warning", "Please select an option.")
        
        self.master.after(1000, self.next_question)

    def next_question(self):
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
