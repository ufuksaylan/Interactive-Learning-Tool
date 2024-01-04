import json
from question import Question

class FreeFormQuestion(Question): 
  """
  A class to represent a free-form question.
  """
  def __init__(self, question_text, answer,status=True):
    """
    Initializes a new FreeFormQuestion object.
    
    Args:
    question_text (str): The text of the question.
    answer (str): The correct answer for the question.
    status (bool): The status of the question (True for active, False for inactive).
    """
    super().__init__(question_text, status)
    self._answer = answer
    self._type = "quiz"
  
  def to_dict(self):
    return {
      'type': 'freeform',
      'id': self._id,
      'question_text': self._question_text,
      'status': self._status,
      'answer': self._answer
    }
    
  @classmethod
  def from_json(cls, json_str):
    data = json.loads(json_str)
    question_text = data['question_text']
    answer = data['answer']
    status = data['status']
    return cls(question_text, answer, status)
  
  def check_answer(self, answer): 
    return self._answer == answer  