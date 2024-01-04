import unittest
from free_form_question import FreeFormQuestion

class TestFreeFormQuestion(unittest.TestCase):
  def setUp(self):
    self.free_form_question = FreeFormQuestion("What is the capital of France?", "Paris")
  
  def test_to_dict(self):
    result = self.free_form_question.to_dict()
    expected = {
        'type': 'freeform',
        'id': self.free_form_question._id,
        'question_text': 'What is the capital of France?',
        'status': True,
        'answer': 'Paris'
        }
    self.assertEqual(result, expected)
    
  def test_from_json(self):
    json_str = '{"question_text": "What is the capital of France?", "answer": "Paris", "status": true}'
    question = FreeFormQuestion.from_json(json_str)
    self.assertIsInstance(question, FreeFormQuestion)
    self.assertEqual(question._question_text, "What is the capital of France?")
    self.assertEqual(question._answer, "Paris")
    self.assertEqual(question._status, True)
  
  def test_check_answer(self):
    self.assertTrue(self.free_form_question.check_answer("Paris"))
    self.assertFalse(self.free_form_question.check_answer("Berlin"))

if __name__ == '__main__':
    unittest.main()