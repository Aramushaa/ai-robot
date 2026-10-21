class Robot:
    def __init__(self,name):
        self.name = name
        self.status = "sleeping"
    def wake(self):
        if self.status == "awake":
            return f"{self.name} is already {self.status}!"
        
        self.status = "awake"
        return f"{self.name} is now {self.status}!"

    def sleep(self): 
        self.status = "sleeping"
        return f"{self.name} is now {self.status}!"


