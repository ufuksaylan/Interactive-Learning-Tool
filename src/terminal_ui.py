import random
import datetime
import re
from controller import ProfileManager, QuestionManager
from user_profile import Profile
from free_form_question import FreeFormQuestion
from quiz_question import QuizQuestion

class TerminalUI:
  """
  Terminal UI class handles all the terminal-based user interactions for the quiz application. 
  It supports user profile selection, quiz question addition, viewing statistics, 
  enabling/disabling questions, and both practice and test modes.
  """
  def __init__(self):
    """
    Initializes Terminal UI by loading profiles and questions.
    """
    self._profiles = ProfileManager.load_profiles()
    self._questions = QuestionManager.load_questions()
    self._profile = None

  def print_main_menu(self):
    """
    Prints the main menu options to the terminal.
    """
    print("Please choose an option:")
    print("1. Add a question")
    print("2. View statistics")
    print("3. Enable/disable questions")
    print("4. Practice mode")
    print("5. Test mode")
    print("6. Change profile")
    print("7. Exit")

  def get_menu_choice(self, from_number, to_number, text="Enter the number of your choice: "):
    """
    Asks the user for a menu choice within a specific range and returns the choice.

    Args:
      from_number: The smallest valid choice.
      to_number: The largest valid choice.
      text: The prompt to display to the user.

    Returns:
      The user's menu choice as an integer.
    """
    while True:
      choice = input(text)
      if choice.isdigit() and from_number <= int(choice) <= to_number:
        return int(choice)
      print(f"Invalid choice. Please enter a number between {from_number} and {to_number}.")

  def select_or_create_profile(self):
    """
    Allows the user to either select an existing profile or create a new one.
    """
    print("Select an existing profile or create a new one:")
    profiles = self._profiles

    for i, profile in enumerate(profiles, start=1):
      print(f"{i}. {profile['name']}")

    print(f"{len(profiles) + 1}. Create new profile")

    while True:
      choice = input("Enter the number of your choice: ")
      if choice.isdigit() and 1 <= int(choice) <= len(profiles) + 1:
        break
      print("Invalid choice. Please enter a valid number.")

    if int(choice) == len(profiles) + 1:
      profile_name = input("Enter the name for the new profile: ")
      self._profile = Profile(profile_name)
    else:
      self._profile = Profile.from_dict(profiles[int(choice) - 1])
      print(self._profile.name)

  def run(self):
    """
    Runs the terminal UI, providing the main loop for the program.
    """
    self.select_or_create_profile()

    while True:
      self.print_main_menu()
      choice = self.get_menu_choice(1, 7)

      if choice == 1:
        self.add_question()
      elif choice == 2:
        self.view_statistics()
      elif choice == 3:
        self.enable_disable_question()
      elif choice == 4:
        self.practice_mode()
      elif choice == 5:
        self.test_mode()
      elif choice == 6:
        self.select_or_create_profile()
      else:
        print("Goodbye!")
        break
      
  def add_question(self):
    """
    Allows the user to add a new question to the question set.
    """
    print("Add questions (press Ctrl+D to quit the mode):")
    question_manager = QuestionManager()
    
    while True:
      try:
        print("Select question type:")
        print("1. Quiz")
        print("2. Freeform")
        print("3. Quit")

        choice = self.get_menu_choice(1, 3)

        if choice == 3:
          break
        question_text = input("Enter the question text: ").strip()

        if choice == 1:
          num_options = self.get_menu_choice(2, 5, "Enter the number of options (2-5): ")

          options = [input(f"Option {i}: ").strip() for i in range(1, num_options + 1)]
          answer_index = int(input(f"Enter the correct answer index (1-{num_options}): ")) - 1
          question = QuizQuestion(question_text, answer_index, options)
          question_manager.add_question(question)
          
        elif choice == 2:
          answer = input("Enter the correct answer: ").strip()
          question = FreeFormQuestion(question_text, answer)
          question_manager.add_question(question)
        else:
          print("Invalid choice. Please enter a valid number.")

      except EOFError:
        print("\nExiting question addition mode.")
        break
    
    question_manager.save_to_json()
    ProfileManager.add_new_questions_to_each_profile(question_manager.questions)
  
  def view_statistics(self):
    """
    Displays statistics for the questions, including how often they have been shown 
    and the percentage of correct answers.
    """
    questions = QuestionManager.load_questions()
    question_stats = self._profile._questions_stats

    print(f"Question Statistics for {self._profile.name}:\n")
    for question in questions:
      for q_stat in question_stats:
        if q_stat["id"] == question["id"]:
          correct_percentage = (q_stat["correct_answers"] / q_stat["times_shown"]) * 100 if q_stat["times_shown"] > 0 else 0
          print(f"ID: {question['id']} | Active: {question['status']} | Question: {question['question_text']}")
          print(f"Times shown: {q_stat['times_shown']} | Correct answers: {q_stat['correct_answers']} ({correct_percentage:.2f}%)")
          print("-" * 80)
          break

    print("\nPress Enter to continue...")
    input()

  def enable_disable_question(self):
    """
    Allows the user to enable or disable questions for their profile.
    """
    print("Disable/Enable Questions mode (press Ctrl+D to quit the mode):\n")
    question_ids_to_toggle = []
    
    while True: 
      try:
        question_id = self.get_menu_choice(1, QuestionManager.get_last_id(), "Enter the ID of the question you want to enable/disable: ")
        questions = QuestionManager.load_questions()
        
        for question in questions:
          if question_id == question["id"]:
            if question['type'] == 'freeform':
              question_answer = question['answer']
            else: 
              question_answer = question['options'][question['answer_index']]
              
            print(f"ID: {question['id']} | Question Answer: {question_answer} | Question: {question['question_text']}")
            print("-" * 80)
        
            confirm = input(f"Do you want to {'disable' if question['status'] else 'enable'} this question? (y/n): ").lower()
            if confirm.lower() == 'y':
              question_ids_to_toggle.append(question["id"])
                  
      except EOFError: 
        break
    
    QuestionManager.toggle_question_status(question_ids_to_toggle)

  def ask_question(self, question_json):
    """
    Asks the user a question based on the provided question JSON.

    Args:
      question_json: A dictionary containing question information.

    Returns:
      A boolean indicating whether the user's answer was correct.
    """
    if question_json["type"] == "quiz":
      return self.ask_quiz_question(question_json)
    elif question_json["type"] == "freeform":
      return self.ask_freeform_question(question_json)

  def ask_quiz_question(self, question_json):
    """
    Asks the user a multiple choice question based on the provided question JSON.

    Args:
      question_json: A dictionary containing question information.

    Returns:
      A boolean indicating whether the user's answer was correct.
    """
    print(f"\n{question_json['question_text']}")
    for index, option in enumerate(question_json['options']):
      print(f"{index + 1}. {option}")

    choice = self.get_menu_choice(1, len(question_json['options']), "Enter your answer: ")
    return choice - 1 == question_json['answer_index']

  def ask_freeform_question(self, question_json):
    """
    Asks the user a freeform question based on the provided question JSON.

    Args:
      question_json: A dictionary containing question information.

    Returns:
      A boolean indicating whether the user's answer was correct.
    """
    print(f"\n{question_json['question_text']}")
    answer = input("Enter your answer: ").strip()
    
    # Use regular expressions to remove extra spaces
    normalized_answer = re.sub(r'\s+', ' ', answer).lower()
    normalized_correct_answer = re.sub(r'\s+', ' ', question_json['answer']).lower()
    
    return normalized_answer == normalized_correct_answer

  def calculate_new_probability(self, question_stats):
    """
    Calculates a new selection probability for a question based on its statistics.

    Args:
      question_stats: A dictionary containing question statistics.

    Returns:
      The new selection probability as a float.
    """
    times_shown = question_stats["times_shown"]
    correct_answers = question_stats["correct_answers"]
    incorrect_answers = times_shown - correct_answers
    
    new_probability = 1 - (incorrect_answers / (times_shown + 1))
    return new_probability
  
  def practice_mode(self):
    """
    Puts the user into practice mode, where they can answer questions without keeping score.
    """
    print("Practice mode (press Ctrl+D to quit the mode):\n")  
    
    questions = QuestionManager.load_questions()
    active_questions = [q for q in questions if q["status"]]

    while True:
      try:
        question_probabilities = self._profile.get_question_probabilities()
        selected_question = random.choices(active_questions, weights=question_probabilities, k=1)[0]
        correct = self.ask_question(selected_question)

        # Update the profile's question statistics
        question_stats = self._profile.get_question_stats(selected_question["id"])
        question_stats["times_shown"] += 1
        if correct:
          question_stats["correct_answers"] += 1

        # Update the selection probability for the question
        question_stats["selection_probability"] = self.calculate_new_probability(question_stats)
        ProfileManager.save_to_json(self._profile)
        
      except EOFError:
        break
      
  def test_mode(self):
    """
    Puts the user into test mode, where they answer a set number of questions and receive a score.
    """
    print("Test mode (press Ctrl+D to quit the mode):\n")

    questions = QuestionManager.load_questions()
    active_questions = [q for q in questions if q["status"]]

    num_questions = self.get_menu_choice(1, len(active_questions), "Enter the number of questions for the test: ")

    random.shuffle(active_questions)
    selected_questions = active_questions[:num_questions]

    correct_answers = 0

    try:
      for question in selected_questions:
        is_correct = self.ask_question(question)
        if is_correct:
          correct_answers += 1
    except EOFError:
      print("Test mode aborted.\n")
      return

    score = (correct_answers / num_questions) * 100
    print(f"Your score: {score:.2f}%")

    with open("results.txt", "a") as results_file:
      timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      results_file.write(f"{timestamp} - Score: {score:.2f}%\n")