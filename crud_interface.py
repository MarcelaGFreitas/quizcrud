import tkinter as tk  # import base tkinter module
from tkinter import ttk, messagebox  # import themed widgets and dialogs
import crud_logic  # import backend logic module

def run_crud():
    root = tk.Tk()  # create main window
    root.title("Quiz CRUD")  # set window title
    root.geometry("800x500")  # set window size

    questions = crud_logic.load_quiz()  # load questions from JSON

    var_question = tk.StringVar()  # variable for question text
    var_opt1 = tk.StringVar()  # variable for option 1
    var_opt2 = tk.StringVar()  # variable for option 2
    var_opt3 = tk.StringVar()  # variable for option 3
    var_correct = tk.StringVar(value="0")  # variable for correct answer index

    def clear():
        var_question.set("")  # clear question field
        var_opt1.set("")  # clear option 1
        var_opt2.set("")  # clear option 2
        var_opt3.set("")  # clear option 3
        var_correct.set("0")  # reset correct to 0
        tree.selection_remove(tree.selection())  # clear table selection

    def refresh_table():
        for item in tree.get_children():  # loop through table rows
            tree.delete(item)  # delete each row
        for idx, q in enumerate(questions):  # loop through questions list
            tree.insert("", "end", values=(idx, q["question"], q["correct"]))  # insert row with data

    def add():
        try:
            payload = {  # build data object
                "question": var_question.get().strip(),  # get question text
                "options": [var_opt1.get().strip(), var_opt2.get().strip(), var_opt3.get().strip()],  # get options list
                "correct": int(var_correct.get())  # get correct index as integer
            }
            crud_logic.add_question(questions, payload)  # call backend add function
            refresh_table()  # update table display
            clear()  # clear input fields
            messagebox.showinfo("Success", "Question added!")  # show success message
        except Exception as e:  # catch any errors
            messagebox.showerror("Error", str(e))  # show error message

    def update():
        sel = tree.selection()  # get selected table row
        if not sel:  # check if nothing selected
            messagebox.showwarning("Warning", "Select a question")  # show warning
            return  # exit function
        idx = int(tree.item(sel[0], "values")[0])  # get index from selected row
        try:
            payload = {  # build data object
                "question": var_question.get().strip(),  # get question text
                "options": [var_opt1.get().strip(), var_opt2.get().strip(), var_opt3.get().strip()],  # get options list
                "correct": int(var_correct.get())  # get correct index as integer
            }
            crud_logic.edit_question(questions, idx, payload)  # call backend edit function
            refresh_table()  # update table display
            clear()  # clear input fields
            messagebox.showinfo("Success", "Question updated!")  # show success message
        except Exception as e:  # catch any errors
            messagebox.showerror("Error", str(e))  # show error message

    def delete():
        sel = tree.selection()  # get selected table row
        if not sel:  # check if nothing selected
            messagebox.showwarning("Warning", "Select a question")  # show warning
            return  # exit function
        idx = int(tree.item(sel[0], "values")[0])  # get index from selected row
        if messagebox.askyesno("Confirm", "Delete this question?"):  # ask for confirmation
            try:
                crud_logic.remove_question(questions, idx)  # call backend delete function
                refresh_table()  # update table display
                clear()  # clear input fields
                messagebox.showinfo("Success", "Question deleted!")  # show success message
            except Exception as e:  # catch any errors
                messagebox.showerror("Error", str(e))  # show error message

    def on_select(event):
        sel = tree.selection()  # get selected table row
        if sel:  # check if something is selected
            idx = int(tree.item(sel[0], "values")[0])  # get index from row
            q = questions[idx]  # get question data from list
            var_question.set(q["question"])  # load question into field
            var_opt1.set(q["options"][0])  # load option 1
            var_opt2.set(q["options"][1])  # load option 2
            var_opt3.set(q["options"][2])  # load option 3
            var_correct.set(str(q["correct"]))  # load correct index

    input_frame = ttk.LabelFrame(root, text="Question Editor", padding=10)  # create input section frame
    input_frame.pack(fill="x", padx=10, pady=10)  # add frame to window

    ttk.Label(input_frame, text="Question:").grid(row=0, column=0, sticky="w", pady=5)  # create label
    ttk.Entry(input_frame, textvariable=var_question, width=60).grid(row=0, column=1, columnspan=2, pady=5)  # create input field

    ttk.Label(input_frame, text="Option 1:").grid(row=1, column=0, sticky="w", pady=5)  # create label
    ttk.Entry(input_frame, textvariable=var_opt1, width=30).grid(row=1, column=1, pady=5)  # create input field

    ttk.Label(input_frame, text="Option 2:").grid(row=2, column=0, sticky="w", pady=5)  # create label
    ttk.Entry(input_frame, textvariable=var_opt2, width=30).grid(row=2, column=1, pady=5)  # create input field

    ttk.Label(input_frame, text="Option 3:").grid(row=3, column=0, sticky="w", pady=5)  # create label
    ttk.Entry(input_frame, textvariable=var_opt3, width=30).grid(row=3, column=1, pady=5)  # create input field

    ttk.Label(input_frame, text="Correct:").grid(row=1, column=2, sticky="w", padx=(10,0))  # create label
    ttk.Combobox(input_frame, textvariable=var_correct, values=["0", "1", "2"], width=5, state="readonly").grid(row=1, column=3, sticky="w")  # create dropdown

    table_frame = ttk.LabelFrame(root, text="Questions", padding=10)  # create table section frame
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)  # add frame to window

    tree = ttk.Treeview(table_frame, columns=("idx", "question", "correct"), show="headings", height=10)  # create table
    tree.heading("idx", text="#")  # set column header
    tree.heading("question", text="Question")  # set column header
    tree.heading("correct", text="Correct")  # set column header
    tree.column("idx", width=50, anchor="center")  # configure column
    tree.column("question", width=500)  # configure column
    tree.column("correct", width=80, anchor="center")  # configure column
    tree.pack(fill="both", expand=True)  # add table to frame
    tree.bind("<<TreeviewSelect>>", on_select)  # bind selection event

    refresh_table()  # populate table with initial data

    button_frame = ttk.Frame(root)  # create button section frame
    button_frame.pack(fill="x", padx=10, pady=10)  # add frame to window

    ttk.Button(button_frame, text="Add", command=add).pack(side="left", padx=5)  # create add button
    ttk.Button(button_frame, text="Update", command=update).pack(side="left", padx=5)  # create update button
    ttk.Button(button_frame, text="Delete", command=delete).pack(side="left", padx=5)  # create delete button
    ttk.Button(button_frame, text="Clear", command=clear).pack(side="left", padx=5)  # create clear button

    root.mainloop()  # start application event loop