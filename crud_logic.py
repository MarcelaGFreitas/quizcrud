# crud_logic.py

import json
import os

file_name = "questions.json"


def load_quiz():
    """Load all questions from the JSON file and return as list"""
    if os.path.exists(file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def save_quiz(questions):
    """Save all questions into the JSON file"""
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)


def add_question(questions, payload):
    """Add question - UI branch modification"""
    if not payload["question"]:
        raise ValueError("Question cannot be empty")
    
    if any(not opt for opt in payload["options"]):
        raise ValueError("All options must be filled")
    
    if payload["correct"] not in [0, 1, 2]:
        raise ValueError("Correct answer must be 0, 1, or 2")
    
    new_question = {
        "question": payload["question"],
        "options": payload["options"],
        "correct": payload["correct"]
    }
    
    questions.append(new_question)
    save_quiz(questions)


def edit_question(questions, idx, payload):
    """Update an existing question by index"""
    if idx < 0 or idx >= len(questions):
        raise ValueError("Invalid question index")
    
    if not payload["question"]:
        raise ValueError("Question cannot be empty")
    
    if any(not opt for opt in payload["options"]):
        raise ValueError("All options must be filled")
    
    if payload["correct"] not in [0, 1, 2]:
        raise ValueError("Correct answer must be 0, 1, or 2")
    
    questions[idx] = {
        "question": payload["question"],
        "options": payload["options"],
        "correct": payload["correct"]
    }
    
    save_quiz(questions)


def remove_question(questions, idx):
    """Delete a question by index"""
    if idx < 0 or idx >= len(questions):
        raise ValueError("Invalid question index")
    
    questions.pop(idx)
    save_quiz(questions)