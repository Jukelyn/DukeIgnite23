class Course:
    """
    Course class to keep track of each course as an object.
    """
    def __init__(self, subject_line:str, title: str, crse_id: int, desc: int, offering: str):
        """
        Creates a Course object with the parameters that we care about... surely
        """
        self.subject_line = subject_line;
        self.title = title
        self.crse_id = crse_id
        self.desc = desc
        self.offering = offering

    def __str__(self):
        return f"{self.subject_line} | {self.title} | {self.crse_id} | {self.desc} | {self.offering}"
    
    def valid(self):
        if self.title is None:
            return False
        
        if self.subject_line is None:
            return False
        
        if self.offering is None:
            return False
        
        if self.desc is None:
            return False
        
        if self.crse_id is None:
            return False
        
        return True
    