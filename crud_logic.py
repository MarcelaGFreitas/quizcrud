# crud_logic.py
import json  # import json module to work with JSON files
import os  # import os module to check file existence

FILE_NAME = "dados_quiz.json"  # constant with the JSON file name

def load_quiz():
    """Load quiz questions from JSON file"""
    if not os.path.exists(FILE_NAME):  # check if file exists
        return []  # return empty list if file doesn't exist
    
    with open(FILE_NAME, 'r', encoding='utf-8') as file:  # open file for reading
        return json.load(file)  # load and return JSON data as list

def save_quiz(questions):
    """Save quiz questions to JSON file"""
    with open(FILE_NAME, 'w', encoding='utf-8') as file:  # open file for writing
        json.dump(questions, file, indent=4, ensure_ascii=False)  # save with formatting

def add_question(questions, payload):
    """Add new question to quiz"""
    # Validate question is not empty
    if not payload["question"].strip():
        raise Exception("Question cannot be empty")  # raise error if invalid
    
    # Validate all options are filled
    if any(not opt.strip() for opt in payload["options"]):
        raise Exception("All options must be filled")  # raise error if any option is empty
    
    # Validate correct index is valid (0, 1, or 2)
    if payload["correct"] not in [0, 1, 2]:
        raise Exception("Correct answer must be 0, 1, or 2")  # raise error if invalid
    
    questions.append(payload)  # add question to list
    save_quiz(questions)  # save to JSON file

def edit_question(questions, index, payload):
    """Edit existing question by index"""
    # Validate index is within valid range
    if index < 0 or index >= len(questions):
        raise Exception("Invalid question index")  # raise error if index is invalid
    
    # Validate question is not empty
    if not payload["question"].strip():
        raise Exception("Question cannot be empty")  # raise error if invalid
    
    # Validate all options are filled
    if any(not opt.strip() for opt in payload["options"]):
        raise Exception("All options must be filled")  # raise error if any option is empty
    
    # Validate correct index is valid (0, 1, or 2)
    if payload["correct"] not in [0, 1, 2]:
        raise Exception("Correct answer must be 0, 1, or 2")  # raise error if invalid
    
    questions[index] = payload  # update question at given index
    save_quiz(questions)  # save to JSON file

def remove_question(questions, index):
    """Remove question by index"""
    # Validate index is within valid range
    if index < 0 or index >= len(questions):
        raise Exception("Invalid question index")  # raise error if index is invalid
    
    questions.pop(index)  # remove question from list
    save_quiz(questions)  # save to JSON file