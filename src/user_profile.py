class Profile: 
  """
    A class representing a user profile.
    
    Note:
        The imports for ProfileManager and QuestionManager are inside the methods to avoid circular import issues.
  """
  
  def __init__(self, name, from_dict=False):
    """
    Initializes a new profile instance.
    
    Args:
        name (str): The name of the profile.
        from_dict (bool): True if the profile is being initialized from a dictionary, False otherwise.
    """
    self._name = name
    
    if not from_dict:
      from controller import ProfileManager  # Import ProfileManager here
      self._id = ProfileManager.generate_id()
      self._questions_stats = ProfileManager.initialize_all_stats_to_zero()
      ProfileManager.save_to_json(self)
  
  def to_dict(self):
    """
    Returns the profile as a dictionary.
    
    Returns:
        dict: The profile as a dictionary.
    """
    return {
      "id": self._id,
      "name": self._name,
      "questions_stats": self._questions_stats
    }
    
  def get_question_probabilities(self):
    """
    Gets the probabilities for all questions in the profile.
    
    Returns:
        list: A list of probabilities.
    """
    from controller import QuestionManager
    probabilities = []
    questions = QuestionManager.load_questions()
    question_status = {q["id"]: q["status"] for q in questions}

    for stats in self._questions_stats:
      if question_status[stats['id']]:
        probabilities.append(float(stats['selection_probability']))

    return probabilities
  
  def get_question_stats(self, question_id):
    """
    Gets the statistics for a specific question in the profile.
    
    Args:
        question_id (str): The ID of the question.

    Returns:
        dict: The statistics for the question.
    """
    for question_stat in self._questions_stats:
      if question_stat["id"] == question_id:
        return question_stat
    
  @classmethod
  def from_dict(cls, data):
    """
    Creates a new profile instance from a dictionary.
    Args:
        data (dict): The dictionary to create the profile from.
    
    Returns:
        Profile: A new profile instance.
    """
    profile = cls(data["name"], from_dict=True)
    profile._questions_stats = data["questions_stats"]
    profile._id = data["id"]
    return profile
    
  @property
  def name(self):
    return self._name
