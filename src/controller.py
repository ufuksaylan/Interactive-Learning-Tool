import os
import json
from config import QUESTIONS_FILE, LAST_ID_QUESTIONS, LAST_ID_PROFILES, PROFILES_FOLDER
from user_profile import Profile

def load_data(file_name):
  """
  Load data from a JSON file.

  Args:
    file_name (str): Name of the JSON file to load data from.

  Returns:
    list: List of items from the JSON file.
  """
  try:
    with open(file_name, 'r') as file:
      existing_data = json.load(file)
  except FileNotFoundError:
    existing_data = []
  return existing_data

def save_data_to_json(file_name, existing_data, data_list):
  """
  Save data to a JSON file.

  Args:
    file_name (str): Name of the JSON file to save data to.
    existing_data (list): List of existing data in the JSON file.
    data_list (list): List of data to append to the JSON file.
  """
  with open(file_name, 'w') as file:
    json_data = [item.to_dict() for item in data_list]
    updated_data = existing_data + json_data
    json.dump(updated_data, file, indent=2)

def generate_unique_id(file_name):
  """
  Generate a unique ID for an item.

  Args:
    file_name (str): Name of the file to get the last ID from.

  Returns:
    int: Unique ID for the item.
  """
  try:
    with open(file_name, 'r') as f:
      last_id = int(f.read().strip())
  except FileNotFoundError:
    last_id = 0
      
  new_id = last_id + 1
  
  with open(file_name, 'w') as f:
    f.write(str(new_id))
    
  return new_id

class QuestionManager: 
  """
  A class for managing questions.
  """
  
  def __init__(self):
    self._questions = []
    
  @property
  def questions(self):
    return self._questions
  
  def add_question(self, question):
    self._questions.append(question)
    
  @classmethod
  def load_questions(cls):
    """
    Load questions from a JSON file.

    Returns:
      list: List of questions.
    """
    return load_data(QUESTIONS_FILE)
  
  def save_to_json(self):
    """
    Save questions to a JSON file.
    """
    existing_questions = self.load_questions()
    save_data_to_json(QUESTIONS_FILE, existing_questions, self.questions)
      
  @classmethod
  def generate_id(cls):
    return generate_unique_id(LAST_ID_QUESTIONS)
  
  @classmethod
  def get_last_id(cls):
    """
    Get the last ID of the questions.

    Returns:
      int: Last ID of the questions.
    """
    try:
      with open(LAST_ID_QUESTIONS, 'r') as f:
        last_id = int(f.read().strip())
    except FileNotFoundError:
      last_id = 0
    return last_id

  @classmethod
  def toggle_question_status(cls, questions_id_list):
    """
    Toggle the status of a list of questions using their ids.

    Args:
      questions_id_list (list): List of question IDs.
    """
    questions = cls.load_questions()
    
    for question_id in questions_id_list:
      for question in questions:
        if question["id"] == question_id:
          question["status"] = not question["status"]
          new_status = "enabled" if question["status"] else "disabled"
          print(f"\nQuestion ID {question_id} is now {new_status}.")
          
    cls.save_questions(questions)
  
  
  @classmethod
  def save_questions(cls, questions):
    with open(QUESTIONS_FILE, 'w') as file:
      json.dump(questions, file, indent=2)

class ProfileManager: 
  """
  A class to manage user profiles.
  """
  @classmethod
  def initialize_all_stats_to_zero(cls):
    """
    Initializes statistics for all questions to zero.
    
    Returns:
    list: A list of dictionaries, each containing the question ID, times shown, correct answers,
          and selection probability.
    """
    questions = QuestionManager.load_questions()
    stats = []
    
    for question in questions: 
      stat = {
        "id": question["id"],
        "times_shown": 0,
        "correct_answers": 0,
        "selection_probability": 1
      }
      stats.append(stat)
      
    return stats
  
  @classmethod
  def load_profiles(cls):
    """
    Loads all profiles from the profiles folder.
    
    Returns:
    list: A list of dictionaries, each containing profile data.
    """
    profiles = []

    for file_name in os.listdir(PROFILES_FOLDER):
      if file_name.endswith('.json'):
        profile_file = os.path.join(PROFILES_FOLDER, file_name)
        with open(profile_file, 'r') as f:
          profile_data = json.load(f)
          
          profiles.append(profile_data) 
          
    return profiles
  
  @classmethod
  def save_to_json(cls, profile):
    """
    Saves a profile to a JSON file.
    
    Args:
    profile (Profile): The profile to be saved.
    """
    file_name = PROFILES_FOLDER + f"{profile._id}.json"
    with open(file_name, 'w') as file:
      json.dump(profile.to_dict(), file, indent=2)

    
  @classmethod
  def generate_id(cls):
    """
    Generates a unique ID for a new profile.
    
    Returns:
    int: A unique ID.
    """
    return generate_unique_id(LAST_ID_PROFILES)
  
  @classmethod
  def add_new_questions_to_each_profile(cls, questions):
    """
    Adds new questions to each profile.
    
    Args:
    questions (list): A list of Question objects to be added to each profile.
    """
    profiles = cls.load_profiles()
    
    for profile_data in profiles:
      profile = Profile.from_dict(profile_data)
      
      for question in questions:
        question_stats = {
          "id": question._id,
          "times_shown": 0,
          "correct_answers": 0,
          "selection_probability": 1
          }
        profile._questions_stats.append(question_stats)
        
      cls.save_to_json(profile)
    
    
    