# QUESTIONS_FILE = "../data/questions.json"

# LAST_ID_PROFILES = "../data/last_id_profiles.txt"

# LAST_ID_QUESTIONS = "../data/last_id_questions.txt"

# PROFILES_FOLDER = "../data/profiles/"

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

QUESTIONS_FILE = os.path.join(BASE_DIR, "data/questions.json")

LAST_ID_PROFILES = os.path.join(BASE_DIR, "data/last_id_profiles.txt")

LAST_ID_QUESTIONS = os.path.join(BASE_DIR, "data/last_id_questions.txt")

PROFILES_FOLDER = os.path.join(BASE_DIR, "data/profiles/")
