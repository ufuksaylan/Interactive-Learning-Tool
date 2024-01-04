from abc import ABC, abstractmethod
import json
from controller import QuestionManager

class Question(ABC): 
  """
  A base class representing a question.
  """
  
  def __init__(self, question_text, status=True):
    self._id = QuestionManager.generate_id()
    self._question_text = question_text 
    self._status = status
    
  def to_json(self):
    """
    Convert the question to a JSON string.

    Returns:
        A JSON string representing the question.
    """
    return json.dumps(self.to_dict(), indent=2)
  
  @abstractmethod
  def to_dict(self):
    """
    Convert the question to a dictionary.
    
    Returns:
        A dictionary representation of the question.
    """
    pass
  
  @abstractmethod
  def from_json(cls, json_str):
    """
    Create a new question instance from a JSON string.

    Args:
        json_str: A JSON string representing the question.

    Returns:
        A new question instance.
    """
    pass