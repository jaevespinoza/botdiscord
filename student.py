class Student:
    def __init__(self, name, status, talent):
         self.name = name
         self.is_alive = status
         self.talent = talent

    def kill(self):
        self.is_alive = "Dead"

    def getname(self):
        return "Name: " + self.name

    def getstatus(self):
        return "Status: " + self.is_alive

    def gettalent(self):
        return "Talent: " + self.talent
        
