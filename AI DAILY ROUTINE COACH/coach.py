import tkinter as tk
from tkinter import messagebox
import cohere
import time

# ----------------- COHERE API KEY ----------------- #
cohere_client = cohere.Client("API KEY")  

# ----------------- AI Engine ----------------- #
class AIModel:
    def __init__(self):
        pass

    def generate_suggestion(self, lifestyle_summary):
        try:
            response = cohere_client.generate(
                model="command",  
                prompt=f"User's lifestyle summary: {lifestyle_summary}. Suggest practical sustainability actions.",
                max_tokens=150,
                temperature=0.7,
                stop_sequences=["--"]
            )
            return response.generations[0].text.strip()
        except Exception as e:
            return f"Error from AI: {str(e)}"

# ----------------- Feedback Engine ----------------- #
class FeedbackEngine:
    @staticmethod
    def get_feedback(index, value):
        q_text = questions[index][0]
        feedback = ""

        try:
            if index == 0:
                if value < 4:
                    feedback = "✅ Your energy consumption is excellent!"
                elif value < 8:
                    feedback = "⚠️ Moderate energy use. Try reducing it slightly."
                else:
                    feedback = "❌ High energy use! Consider unplugging devices."

            elif index == 1:
                feedback = "✅ Great! Renewable energy is sustainable!" if value else "⚠️ Try switching to renewables."

            elif index == 2:
                if value >= 3:
                    feedback = "✅ You're recycling regularly. Well done!"
                elif value >= 1:
                    feedback = "♻️ Try to recycle a bit more often."
                else:
                    feedback = "❌ Try starting a recycling habit."

            elif index == 3:
                if value < 80:
                    feedback = "✅ Great water conservation!"
                elif value <= 150:
                    feedback = "⚠️ Average water use. Be mindful."
                else:
                    feedback = "❌ High water use. Consider reducing it."

            elif index == 4:
                feedback = "✅ Efficient appliances save energy!" if value else "⚠️ Upgrade to energy-saving devices."

            elif index == 5:
                if value <= 2:
                    feedback = "✅ Excellent car usage level!"
                elif value <= 4:
                    feedback = "⚠️ Consider reducing car use."
                else:
                    feedback = "❌ High car usage. Try biking or public transport."

            elif index == 6:
                if value <= 4:
                    feedback = "✅ Low waste output. Great!"
                elif value <= 8:
                    feedback = "⚠️ Try reducing waste slightly."
                else:
                    feedback = "❌ Too much waste. Consider reusing items."

            elif index == 7:
                feedback = "✅ Public transportation is eco-friendly!" if value else "🚇 Try using buses or trains."

            elif index == 8:
                feedback = "✅ Plant-based eating helps the planet!" if value else "🥗 Try adding more plant-based meals."

            elif index == 9:
                feedback = "✅ Active in sustainability programs!" if value else "🌱 Join a local sustainability project."
        except:
            feedback = "Invalid input."

        return f"{q_text}\n➡️ {feedback}\n"

# ----------------- GUI Class ----------------- #
class CarbonCoachApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌿 AI Daily Routine Carbon Coach")
        self.root.geometry("750x600")
        self.root.configure(bg="#e8f5e9")
        self.root.resizable(False, False)

        self.ai_model = AIModel()
        self.answers = []
        self.feedback_log = []
        self.q_index = 0

        self.answer_var = tk.StringVar()
        self.entry_var = tk.StringVar()

        self.setup_ui()

    def setup_ui(self):
        self.welcome_label = tk.Label(self.root, text="🌍 Welcome to Your AI Carbon Footprint Coach!",
                                      font=("Helvetica", 18, "bold"), bg="#e8f5e9")
        self.welcome_label.pack(pady=20)

        self.info_label = tk.Label(self.root, text="Answer a few questions about your daily habits,\nand get suggestions to reduce your carbon footprint.",
                                   font=("Helvetica", 14), bg="#e8f5e9")
        self.info_label.pack()

        self.start_button = tk.Button(self.root, text="Start Now", font=("Helvetica", 14), command=self.show_question,
                                      bg="#4CAF50", fg="white", padx=20, pady=10)
        self.start_button.pack(pady=30)

        self.question_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg="#e8f5e9")
        self.entry_widget = tk.Entry(self.root, textvariable=self.entry_var, font=("Helvetica", 12))
        self.yes_radio = tk.Radiobutton(self.root, text="Yes", variable=self.answer_var, value="1",
                                        font=("Helvetica", 12), bg="#e8f5e9")
        self.no_radio = tk.Radiobutton(self.root, text="No", variable=self.answer_var, value="0",
                                       font=("Helvetica", 12), bg="#e8f5e9")
        self.next_button = tk.Button(self.root, text="Next", font=("Helvetica", 14), command=self.next_question,
                                     bg="#2e7d32", fg="white", padx=15, pady=5)

    def show_question(self):
        self.welcome_label.pack_forget()
        self.info_label.pack_forget()
        self.start_button.pack_forget()

        if self.q_index >= len(questions):
            return

        q_text, q_type = questions[self.q_index]
        self.question_label.config(text=q_text)
        self.question_label.pack(pady=20)

        self.yes_radio.pack_forget()
        self.no_radio.pack_forget()
        self.entry_widget.pack_forget()

        if q_type == "radio":
            self.answer_var.set("")
            self.yes_radio.pack()
            self.no_radio.pack()
        else:
            self.entry_var.set("")
            self.entry_widget.pack()

        self.next_button.pack(pady=20)

    def next_question(self):
        q_type = questions[self.q_index][1]

        if q_type == "radio":
            val = self.answer_var.get()
            if val not in ["0", "1"]:
                messagebox.showwarning("Input Required", "Please select Yes or No.")
                return
            value = int(val)
        else:
            entry = self.entry_var.get()
            if not entry.strip():
                messagebox.showwarning("Input Required", "Please enter a number.")
                return
            try:
                value = int(entry)
            except ValueError:
                messagebox.showwarning("Invalid Input", "Only numeric input allowed.")
                return

        self.answers.append(value)
        feedback = FeedbackEngine.get_feedback(self.q_index, value)
        self.feedback_log.append(feedback)

        self.q_index += 1
        if self.q_index < len(questions):
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        result_summary = "\n".join([f"{questions[i][0]} => {self.answers[i]}" for i in range(len(self.answers))])
        time.sleep(1)  
        ai_suggestion = self.ai_model.generate_suggestion(result_summary)

        final_feedback = "\n".join(self.feedback_log)

        messagebox.showinfo(
            "🌿 Your AI Coach Suggests:",
            f"📋 Your responses:\n\n{result_summary}\n\n🧠 Feedback:\n\n{final_feedback}\n\n🤖 AI Suggestions:\n{ai_suggestion}"
        )

# ----------------- Questions ----------------- #
questions = [
    ("How much energy do you consume daily? (kWh)", "entry"),
    ("Do you use renewable energy sources?", "radio"),
    ("How often do you recycle? (times/week)", "entry"),
    ("How much water do you use daily? (liters)", "entry"),
    ("Do you use energy-efficient appliances?", "radio"),
    ("How often do you use your car for daily commute?", "entry"),
    ("How much waste do you produce daily? (kg)", "entry"),
    ("Do you use public transportation?", "radio"),
    ("Do you eat plant-based meals?", "radio"),
    ("Are you active in any sustainability programs?", "radio")
]

# ----------------- Run App ----------------- #
def run_app():
    root = tk.Tk()
    app = CarbonCoachApp(root)
    root.mainloop()

run_app()
