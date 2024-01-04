import unittest
from user_profile import Profile

class TestProfile(unittest.TestCase):
    
  def setUp(self):
    self.name = "John Doe"
    self.profile = Profile(self.name)
      
  def test_to_dict(self):
    profile_dict = self.profile.to_dict()
    self.assertEqual(profile_dict['name'], self.name)
    self.assertIsInstance(profile_dict['id'], int)
    self.assertIsInstance(profile_dict['questions_stats'], list)
      
  def test_from_dict(self):
    profile_dict = self.profile.to_dict()
    profile_from_dict = Profile.from_dict(profile_dict)
    self.assertEqual(profile_from_dict.to_dict(), profile_dict)

  def test_get_question_probabilities(self):
    probabilities = self.profile.get_question_probabilities()
    self.assertIsInstance(probabilities, list)
    for prob in probabilities:
      self.assertIsInstance(prob, float)

  def test_get_question_stats(self):
    question_id = self.profile._questions_stats[0]['id']
    question_stats = self.profile.get_question_stats(question_id)
    self.assertIsInstance(question_stats, dict)
    self.assertEqual(question_stats['id'], question_id)

if __name__ == '__main__':
    unittest.main()
