import tkinter as tk
from tkinter import ttk, messagebox
import crud_logic

def run_crud():
    root = tk.Tk()
    root.title("Quiz CRUD")
    root.geometry("800x500")
    root.configure(bg="#2c3e50")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background="#2c3e50", foreground="white", font=("Arial", 10))
    style.configure("TLabelframe", background="#2c3e50", foreground="white", bordercolor="#3498db")
    style.configure("TLabelframe.Label", background="#2c3e50", foreground="white", font=("Arial", 10, "bold"))
    style.configure("TEntry", fieldbackground="#ecf0f1", foreground="#2c3e50")
    style.configure("TCombobox", fieldbackground="#ecf0f1", foreground="#2c3e50")
    style.configure("TButton", background="#3498db", foreground="white", font=("Arial", 10, "bold"), borderwidth=0, padding=6)
    style.map("TButton", background=[("active", "#2980b9")])
    style.configure("TFrame", background="#2c3e50")
    style.configure("Treeview", background="#ecf0f1", foreground="#2c3e50", fieldbackground="#ecf0f1", font=("Arial", 9))
    style.configure("Treeview.Heading", background="#3498db", foreground="white", font=("Arial", 10, "bold"))
    style.map("Treeview.Heading", background=[("active", "#2980b9")])

    questions = crud_logic.load_quiz()

    var_question = tk.StringVar()
    var_opt1 = tk.StringVar()
    var_opt2 = tk.StringVar()
    var_opt3 = tk.StringVar()
    var_correct = tk.StringVar(value="1")

    def clear():
        var_question.set("")
        var_opt1.set("")
        var_opt2.set("")
        var_opt3.set("")
        var_correct.set("1")
        tree.selection_remove(tree.selection())

    def refresh_table():
        for item in tree.get_children():
            tree.delete(item)
        for idx, q in enumerate(questions):
            display_correct = q["correct"] + 1
            tree.insert("", "end", values=(idx, q["question"], display_correct))

    def add():
        try:
            correct_internal = int(var_correct.get()) - 1
            payload = {
                "question": var_question.get().strip(),
                "options": [var_opt1.get().strip(), var_opt2.get().strip(), var_opt3.get().strip()],
                "correct": correct_internal
            }
            crud_logic.add_question(questions, payload)
            refresh_table()
            clear()
            messagebox.showinfo("Success", "Question added!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a question")
            return
        idx = int(tree.item(sel[0], "values")[0])
        try:
            correct_internal = int(var_correct.get()) - 1
            payload = {
                "question": var_question.get().strip(),
                "options": [var_opt1.get().strip(), var_opt2.get().strip(), var_opt3.get().strip()],
                "correct": correct_internal
            }
            crud_logic.edit_question(questions, idx, payload)
            refresh_table()
            clear()
            messagebox.showinfo("Success", "Question updated!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a question")
            return
        idx = int(tree.item(sel[0], "values")[0])
        if messagebox.askyesno("Confirm", "Delete this question?"):
            try:
                crud_logic.remove_question(questions, idx)
                refresh_table()
                clear()
                messagebox.showinfo("Success", "Question deleted!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def on_select(event):
        sel = tree.selection()
        if sel:
            idx = int(tree.item(sel[0], "values")[0])
            q = questions[idx]
            var_question.set(q["question"])
            var_opt1.set(q["options"][0])
            var_opt2.set(q["options"][1])
            var_opt3.set(q["options"][2])
            var_correct.set(str(q["correct"] + 1))

    # ================================
    #   INPUT FRAME (editor)
    # ================================
    input_frame = ttk.LabelFrame(root, text="Question Editor", padding=10)
    input_frame.pack(fill="x", padx=10, pady=10)

    ttk.Label(input_frame, text="Question:").grid(row=0, column=0, sticky="w", pady=5)
    ttk.Entry(input_frame, textvariable=var_question, width=60).grid(row=0, column=1, columnspan=2, pady=5)

    ttk.Label(input_frame, text="Option 1:").grid(row=1, column=0, sticky="w", pady=5)
    ttk.Entry(input_frame, textvariable=var_opt1, width=30).grid(row=1, column=1, pady=5)

    ttk.Label(input_frame, text="Option 2:").grid(row=2, column=0, sticky="w", pady=5)
    ttk.Entry(input_frame, textvariable=var_opt2, width=30).grid(row=2, column=1, pady=5)

    ttk.Label(input_frame, text="Option 3:").grid(row=3, column=0, sticky="w", pady=5)
    ttk.Entry(input_frame, textvariable=var_opt3, width=30).grid(row=3, column=1, pady=5)

    ttk.Label(input_frame, text="Correct:").grid(row=1, column=2, sticky="w", padx=(10,0))
    ttk.Combobox(input_frame, textvariable=var_correct, values=["1", "2", "3"], width=5, state="readonly").grid(row=1, column=3, sticky="w")

    # ----------------------------------------------------------
    #   ✅ NEW BUTTON ADDED DIRECTLY IN THE INPUT FRAME
    # ----------------------------------------------------------
    ttk.Button(input_frame, text="Add Question", command=add).grid(
        row=4, column=3, sticky="e", pady=(10, 5), padx=(0, 10)
    )

    # ================================
    #   TABLE FRAME
    # ================================
    table_frame = ttk.LabelFrame(root, text="Questions", padding=10)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ttk.Treeview(table_frame, columns=("idx", "question", "correct"), show="headings", height=10)
    tree.heading("idx", text="#")
    tree.heading("question", text="Question")
    tree.heading("correct", text="Correct")
    tree.column("idx", width=50, anchor="center")
    tree.column("question", width=500)
    tree.column("correct", width=80, anchor="center")
    tree.pack(fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", on_select)

    refresh_table()

    # Bottom buttons (kept as they were — still useful)
    button_frame = ttk.Frame(root)
    button_frame.pack(fill="x", padx=10, pady=10)

    ttk.Button(button_frame, text="Update", command=update).pack(side="left", padx=5, pady=5)
    ttk.Button(button_frame, text="Delete", command=delete).pack(side="left", padx=5, pady=5)
    ttk.Button(button_frame, text="Clear", command=clear).pack(side="left", padx=5, pady=5)

    root.mainloop()
