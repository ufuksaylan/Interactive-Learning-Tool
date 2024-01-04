import unittest
import json
from quiz_question import QuizQuestion

class TestQuizQuestion(unittest.TestCase):
    
  def setUp(self):
    self.question_text = "What is the capital of France?"
    self.answer_index = 1
    self.options = ["London", "Paris", "Berlin", "Madrid"]
    self.status = True
    self.quiz_question = QuizQuestion(self.question_text, self.answer_index, self.options, self.status)
        
  def test_check_answer(self):
    self.assertTrue(self.quiz_question.check_answer(self.answer_index))
    self.assertFalse(self.quiz_question.check_answer(0))

  def test_to_dict(self):
    expected_dict = {
        'type': 'quiz',
        'id': self.quiz_question._id,
        'question_text': self.question_text,
        'status': self.status,
        'answer_index': self.answer_index,
        'options': self.options
        }
    self.assertEqual(self.quiz_question.to_dict(), expected_dict)
        
if __name__ == '__main__':
  unittest.main()
