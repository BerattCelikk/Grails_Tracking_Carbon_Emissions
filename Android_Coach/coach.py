import tkinter as tk
from tkinter import messagebox
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# ----------------- AI Model ----------------- #
X = np.array([
    [5, 1, 3, 100, 1, 2, 3, 1, 1, 0],
    [2, 0, 1, 50, 0, 5, 2, 0, 2, 1],
    [8, 1, 5, 120, 1, 1, 4, 1, 0, 0],
    [3, 0, 4, 70, 1, 3, 3, 0, 1, 1]
])
y = [
    "Reduce energy use and switch to renewable sources.",
    "You're doing well! Try reducing waste production.",
    "Excellent! Keep up your eco-friendly habits.",
    "Consider commuting less by car and recycling more."
]

model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
model.fit(X, y)

# ----------------- App UI ----------------- #
root = tk.Tk()
root.title("🌿 AI Daily Routine Carbon Coach")
root.geometry("750x600")
root.configure(bg="#e8f5e9")
root.resizable(False, False)

# ----------------- Welcome Screen ----------------- #
def start_app():
    welcome_label.pack_forget()
    start_button.pack_forget()
    info_label.pack_forget()
    show_question()

welcome_label = tk.Label(root, text="🌍 Welcome to Your AI Carbon Footprint Coach!", font=("Helvetica", 18, "bold"), bg="#e8f5e9")
welcome_label.pack(pady=20)

info_label = tk.Label(root, text="Answer a few questions about your daily habits,\nand get suggestions to reduce your carbon footprint.", font=("Helvetica", 14), bg="#e8f5e9")
info_label.pack()

start_button = tk.Button(root, text="Start Now", font=("Helvetica", 14), command=start_app, bg="#4CAF50", fg="white", padx=20, pady=10)
start_button.pack(pady=30)

# ----------------- Questions ----------------- #
questions = [
    ("How much energy do you consume daily? (kWh)", "entry"),
    ("Do you use renewable energy sources?", "radio"),
    ("How often do you recycle? (times/week)", "entry"),
    ("How much water do you use daily? (liters)", "entry"),
    ("Do you use energy-efficient appliances?", "radio"),
    ("How often do you commute by car? (days/week)", "entry"),
    ("How much waste do you produce weekly? (kg)", "entry"),
    ("Do you use public transportation?", "radio"),
    ("Do you consume plant-based food?", "radio"),
    ("Do you participate in sustainability programs?", "radio")
]

answers = []
answers_feedback = []
question_index = 0
answer_var = tk.StringVar()
entry_var = tk.StringVar()

question_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#e8f5e9")
entry_widget = tk.Entry(root, textvariable=entry_var, font=("Helvetica", 12))

yes_radio = tk.Radiobutton(root, text="Yes", variable=answer_var, value="1", font=("Helvetica", 12), bg="#e8f5e9")
no_radio = tk.Radiobutton(root, text="No", variable=answer_var, value="0", font=("Helvetica", 12), bg="#e8f5e9")

next_button = tk.Button(root, text="Next", font=("Helvetica", 14), command=lambda: next_question(), bg="#2e7d32", fg="white", padx=15, pady=5)

# ----------------- Feedback Generator ----------------- #
def generate_feedback(q_index, value):
    q_text = questions[q_index][0]
    feedback = ""

    if q_index == 0:  # Energy
        if value < 4:
            feedback = "✅ Your energy consumption is excellent!"
        elif value < 8:
            feedback = "⚠️ Your energy use is moderate. Try reducing it slightly."
        else:
            feedback = "❌ Your energy consumption is high. Unplug unused devices."

    elif q_index == 1:
        feedback = "✅ Great! Renewable energy is sustainable!" if value else "⚠️ Consider switching to renewables."

    elif q_index == 2:
        if value >= 3:
            feedback = "✅ You're recycling regularly. Well done!"
        elif value >= 1:
            feedback = "♻️ Try to recycle a bit more often."
        else:
            feedback = "❌ Recycling makes a difference! Give it a try."

    elif q_index == 3:
        if value < 80:
            feedback = "✅ Your water consumption is low. Good!"
        elif value <= 150:
            feedback = "⚠️ Your water use is average. Watch for excess use."
        else:
            feedback = "❌ High water use detected. Shorter showers help!"

    elif q_index == 4:
        feedback = "✅ Using efficient appliances helps a lot!" if value else "⚠️ Consider switching to energy-saving devices."

    elif q_index == 5:
        if value <= 2:
            feedback = "✅ Great job reducing car usage!"
        elif value <= 4:
            feedback = "⚠️ Consider reducing car trips further."
        else:
            feedback = "❌ Too much car use! Try biking or carpooling."

    elif q_index == 6:
        if value <= 4:
            feedback = "✅ Low waste generation. Keep it up!"
        elif value <= 8:
            feedback = "⚠️ Average waste levels. Look for reduction tips."
        else:
            feedback = "❌ High waste output. Reduce, reuse, recycle!"

    elif q_index == 7:
        feedback = "✅ Using public transport reduces emissions!" if value else "🚇 Try using bus, metro or bike more often."

    elif q_index == 8:
        feedback = "✅ Plant-based eating is eco-friendly!" if value else "🥗 Add more plant-based meals to your diet."

    elif q_index == 9:
        feedback = "✅ Being part of sustainability programs shows commitment!" if value else "🌱 Try joining a local sustainability initiative."

    return f"{q_text}\n➡️ {feedback}\n"

# ----------------- Show Question ----------------- #
def show_question():
    global question_index
    if question_index >= len(questions):
        return

    question, qtype = questions[question_index]
    question_label.config(text=question)
    question_label.pack(pady=20)

    yes_radio.pack_forget()
    no_radio.pack_forget()
    entry_widget.pack_forget()

    if qtype == "radio":
        answer_var.set("")
        yes_radio.pack()
        no_radio.pack()
    else:
        entry_var.set("")
        entry_widget.pack()

    next_button.pack(pady=20)

# ----------------- Next Question ----------------- #
def next_question():
    global question_index

    qtype = questions[question_index][1]
    if qtype == "radio":
        answer = answer_var.get()
        if answer not in ["0", "1"]:
            messagebox.showwarning("Input Required", "Please select Yes or No.")
            return
        value = int(answer)
    else:
        entry = entry_var.get()
        if not entry.strip():
            messagebox.showwarning("Input Required", "Please enter a number.")
            return
        if not entry.isdigit():
            messagebox.showwarning("Invalid Input", "Only numbers are allowed.")
            return
        value = int(entry)

    answers.append(value)
    feedback = generate_feedback(question_index, value)
    answers_feedback.append(feedback)

    question_index += 1
    if question_index < len(questions):
        show_question()
    else:
        give_advice()

# ----------------- AI Advice Summary ----------------- #
def give_advice():
    input_data = np.array([answers])
    prediction = model.predict(input_data)[0]
    feedback_text = "\n".join(answers_feedback)

    messagebox.showinfo("🌿 Your AI Coach Suggests:", f"{prediction}\n\n📋 Personalized Feedback:\n\n{feedback_text}")

# ----------------- Start App ----------------- #
root.mainloop()
