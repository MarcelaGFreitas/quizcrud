# quiz_manager.py
"""
Backend CRUD for quiz questions stored in JSON.
Each record uses the structure:
{
    "question": str,
    "options": [str, str, str],  # 3 options
    "correct": int               # index 0..2
}
"""

import json  # import json to read/write data in JSON format
from pathlib import Path  # import Path for safe file path handling

DATA_FILE = Path("dados_quiz.json")  # define the JSON data file path

def load_quiz():
    """Load the quiz list from JSON file or create an empty list if not found."""
    if not DATA_FILE.exists():  # check if the data file does not exist
        save_quiz([])  # create the file with an empty list if missing
        return []  # return an empty list as the initial dataset
    with DATA_FILE.open("r", encoding="utf-8") as f:  # open the JSON file for reading with UTF-8
        return json.load(f)  # parse JSON content into a Python list and return it

def save_quiz(questions):
    """Save the quiz list to JSON with formatting."""
    with DATA_FILE.open("w", encoding="utf-8") as f:  # open the JSON file for writing with UTF-8
        json.dump(questions, f, indent=4, ensure_ascii=False)  # serialize list to JSON with pretty formatting

def validate_question_payload(payload):
    """Validate a question payload; raise ValueError on invalid data."""
    for key in ("question", "options", "correct"):  # iterate required keys
        if key not in payload:  # check if a required key is missing
            raise ValueError(f"Missing key: {key}")  # raise error for missing key

    if not isinstance(payload["question"], str) or not payload["question"].strip():  # ensure question is a non-empty string
        raise ValueError("Question must be a non-empty string")  # raise error for invalid question

    options = payload["options"]  # get the options list from payload
    if not isinstance(options, list) or len(options) != 3:  # validate that options is a list of exactly 3 items
        raise ValueError("Options must be a list of exactly 3 strings")  # raise error for invalid list size
    if any(not isinstance(opt, str) or not opt.strip() for opt in options):  # ensure each option is a non-empty string
        raise ValueError("Each option must be a non-empty string")  # raise error for invalid options

    correct = payload["correct"]  # get the correct index from payload
    if not isinstance(correct, int) or correct not in (0, 1, 2):  # validate correct index is 0, 1, or 2
        raise ValueError("Correct must be an integer index: 0, 1, or 2")  # raise error for invalid index

def add_question(questions, payload):
    """Add a new question to the list after validation; return updated list."""
    validate_question_payload(payload)  # validate the incoming question payload
    questions.append(payload)  # append the new question to the list
    save_quiz(questions)  # persist the updated list to the JSON file
    return questions  # return the updated list

def edit_question(questions, index, payload):
    """Edit an existing question by index after validation; return updated list."""
    if not isinstance(index, int) or not (0 <= index < len(questions)):  # validate index is within bounds
        raise IndexError("Index out of bounds")  # raise error for invalid index
    validate_question_payload(payload)  # validate the updated payload
    questions[index] = payload  # replace the question at the given index
    save_quiz(questions)  # persist changes to the JSON file
    return questions  # return the updated list

def remove_question(questions, index):
    """Remove a question by index; return updated list."""
    if not isinstance(index, int) or not (0 <= index < len(questions)):  # validate index is within bounds
        raise IndexError("Index out of bounds")  # raise error for invalid index
    del questions[index]  # delete the question at the given index
    save_quiz(questions)  # persist changes to the JSON file
    return questions  # return the updated list
