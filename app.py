import tkinter as tk
from tkinter import ttk, messagebox
import requests
import html
import random

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz App")
        self.master.geometry("1920x1080")
        self.master.config(bg="#2c3e50")
        self.master.state('zoomed')  # Fullscreen mode
        
        self.score = 0
        self.question_index = 0
        self.questions = []
        self.categories = [{'id': 999, 'name': 'India'}]
        self.time_left = 15
        self.timer = None
        self.difficulty = 'easy'
        self.high_scores = []

        self.fetch_categories()
        self.create_category_widgets()
        
    def fetch_categories(self):
        try:
            response = requests.get("https://opentdb.com/api_category.php")
            data = response.json()
            self.categories.extend(data["trivia_categories"])
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching categories: {e}")
    
    def create_category_widgets(self):
        self.category_label = tk.Label(self.master, text="Select a Category", font=('Arial', 28, 'bold'), fg="#ecf0f1", bg="#2c3e50")
        self.category_label.pack(pady=20)
        
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.master, textvariable=self.category_var, font=('Arial', 24))
        self.category_dropdown['values'] = [category['name'] for category in self.categories]
        self.category_dropdown.current(0)
        self.category_dropdown.pack(pady=20)
        
        self.difficulty_label = tk.Label(self.master, text="Select Difficulty", font=('Arial', 28, 'bold'), fg="#ecf0f1", bg="#2c3e50")
        self.difficulty_label.pack(pady=20)
        
        self.difficulty_var = tk.StringVar()
        self.difficulty_dropdown = ttk.Combobox(self.master, textvariable=self.difficulty_var, font=('Arial', 24))
        self.difficulty_dropdown['values'] = ['easy', 'medium', 'hard']
        self.difficulty_dropdown.current(0)
        self.difficulty_dropdown.pack(pady=20)
        
        self.start_button = tk.Button(self.master, text="Start Quiz", command=self.start_quiz, font=('Arial', 24, 'bold'), bg="#27ae60", fg="white", cursor="hand2", activebackground="#2ecc71")
        self.start_button.pack(pady=40)
    
    def start_quiz(self):
        self.difficulty = self.difficulty_var.get()
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
            response = requests.get(f"https://opentdb.com/api.php?amount=10&category={category_id}&difficulty={self.difficulty}&type=multiple")
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
                self.difficulty_label.pack_forget()
                self.difficulty_dropdown.pack_forget()
                self.start_button.pack_forget()
                self.create_widgets()
                self.display_question()
            else:
                messagebox.showerror("Error", "Could not fetch questions. Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching questions: {e}")
    
    def load_india_questions(self):
        india_questions = [
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
            },
            {
                "question": "What is the national animal of India?",
                "options": ["Lion", "Tiger", "Elephant", "Peacock"],
                "answer": "Tiger"
            },
            {
                "question": "Which is the largest state of India by area?",
                "options": ["Uttar Pradesh", "Madhya Pradesh", "Rajasthan", "Maharashtra"],
                "answer": "Rajasthan"
            },
            {
                "question": "Who was the first Prime Minister of India?",
                "options": ["Mahatma Gandhi", "Jawaharlal Nehru", "Indira Gandhi", "Rajendra Prasad"],
                "answer": "Jawaharlal Nehru"
            },
            {
                "question": "Which river is known as the Ganga of the South?",
                "options": ["Godavari", "Krishna", "Cauvery", "Yamuna"],
                "answer": "Cauvery"
            },
            {
                "question": "Which Indian state is known as the 'Spice Garden of India'?",
                "options": ["Kerala", "Assam", "Tamil Nadu", "Karnataka"],
                "answer": "Kerala"
            }
        ]
        
        self.questions = random.sample(india_questions, 5)
        self.category_label.pack_forget()
        self.category_dropdown.pack_forget()
        self.difficulty_label.pack_forget()
        self.difficulty_dropdown.pack_forget()
        self.start_button.pack_forget()
        self.create_widgets()
        self.display_question()
    
    def create_widgets(self):
        self.question_label = tk.Label(self.master, text="", font=('Arial', 24, 'bold'), wraplength=1500, justify="center", bg="#34495e", fg="#ecf0f1", bd=10, relief="groove")
        self.question_label.pack(pady=30)
        
        self.timer_label = tk.Label(self.master, text=f"Time left: {self.time_left} seconds", font=('Arial', 18, 'bold'), bg="#34495e", fg="#ecf0f1")
        self.timer_label.pack(pady=10)
        
        self.var = tk.StringVar()
        self.option_buttons = []
        for _ in range(4):
            btn = tk.Radiobutton(self.master, text="", variable=self.var, value="", font=('Arial', 20), anchor='w', padx=10, bg="#34495e", fg="#ecf0f1", selectcolor="#1abc9c", activebackground="#34495e", activeforeground="#1abc9c", cursor="hand2")
            btn.pack(fill='x', padx=40, pady=5)
            self.option_buttons.append(btn)
        
        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit_answer, font=('Arial', 20, 'bold'), bg="#e74c3c", fg="white", cursor="hand2", activebackground="#c0392b")
        self.submit_button.pack(pady=30)
        
        self.progress_label = tk.Label(self.master, text="", font=('Arial', 18, 'bold'), bg="#34495e", fg="#ecf0f1")
        self.progress_label.pack(pady=10)
    
    def display_question(self):
        self.time_left = 15
        self.update_timer()
        self.update_progress()
        
        question_data = self.questions[self.question_index]
        self.question_label.config(text=question_data["question"])
        for i, option in enumerate(question_data["options"]):
            self.option_buttons[i].config(text=option, value=option)
        self.var.set(None)
    
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left} seconds")
            self.timer = self.master.after(1000, self.update_timer)
        else:
            self.submit_answer(auto_submit=True)
    
    def update_progress(self):
        self.progress_label.config(text=f"Question {self.question_index + 1}/{len(self.questions)}")
    
    def submit_answer(self, auto_submit=False):
        selected_option = self.var.get()
        if selected_option or auto_submit:
            correct_answer = self.questions[self.question_index]["answer"]
            if selected_option == correct_answer:
                self.score += 1
            
            self.question_index += 1
            if self.question_index < len(self.questions):
                self.display_question()
            else:
                if self.timer:
                    self.master.after_cancel(self.timer)
                self.show_review()
        else:
            messagebox.showwarning("Warning", "Please select an option.")
    
    def show_review(self):
        review_window = tk.Toplevel(self.master)
        review_window.title("Review Answers")
        review_window.geometry("800x600")
        review_window.config(bg="#2c3e50")
        
        tk.Label(review_window, text="Review Your Answers", font=('Arial', 24, 'bold'), bg="#2c3e50", fg="#ecf0f1").pack(pady=20)
        
        for i, question in enumerate(self.questions):
            frame = tk.Frame(review_window, bg="#34495e", pady=10)
            frame.pack(fill="x", padx=10)
            
            question_label = tk.Label(frame, text=f"Q{i+1}: {question['question']}", font=('Arial', 18, 'bold'), wraplength=750, justify="left", bg="#34495e", fg="#ecf0f1")
            question_label.pack(anchor='w')
            
            correct_answer_label = tk.Label(frame, text=f"Correct Answer: {question['answer']}", font=('Arial', 18), bg="#34495e", fg="#2ecc71")
            correct_answer_label.pack(anchor='w', padx=20)
            
            selected_answer = self.var.get()
            if selected_answer == question["answer"]:
                selected_answer_label = tk.Label(frame, text=f"Your Answer: {selected_answer} (Correct)", font=('Arial', 18), bg="#34495e", fg="#2ecc71")
            else:
                selected_answer_label = tk.Label(frame, text=f"Your Answer: {selected_answer} (Wrong)", font=('Arial', 18), bg="#34495e", fg="#e74c3c")
            selected_answer_label.pack(anchor='w', padx=20)
        
        tk.Button(review_window, text="Close", command=review_window.destroy, font=('Arial', 18, 'bold'), bg="#e74c3c", fg="white", cursor="hand2", activebackground="#c0392b").pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

