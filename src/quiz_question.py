import json
from question import Question

class QuizQuestion(Question): 
  """
  A class to represent a quiz question.
  """
  
  def __init__(self, question_text, answer_index, options,status=True):
    """
    Initializes a new QuizQuestion object.
    
    Args:
    question_text (str): The text of the question.
    answer_index (int): The index of the correct answer in the options list.
    options (list): A list of strings representing the options for the question.
    status (bool): The status of the question (True for active, False for inactive).
    """
    super().__init__(question_text, status)
    self._answer_index = answer_index
    self._options = options
    self._type = "quiz"
    
  def check_answer(self, answer): 
    return answer == self._answer_index

  def to_dict(self):
    """
    Converts the quiz question object to a dictionary.
    
    Returns:
    dict: A dictionary representation of the quiz question object.
    """
    return {
      'type': 'quiz',
      'id': self._id,
      'question_text': self._question_text,
      'status': self._status,
      'answer_index': self._answer_index,
      'options': self._options
    }
    
  @classmethod
  def from_json(cls, json_str):
    """
    Creates a new QuizQuestion object from a JSON string.
    
    Args:
    json_str (str): The JSON string representing the quiz question object.
    
    Returns:
    QuizQuestion: A new QuizQuestion object.
    """
    data = json.loads(json_str)
    question_text = data['question_text']
    answer_index = data['answer_index']
    options = data['options']
    status = data['status']
    return cls(question_text, answer_index, options, status)