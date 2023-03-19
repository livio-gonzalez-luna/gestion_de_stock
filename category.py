



class Category:
    def __init__(self, idCategory, name):
        self.idCategory = idCategory
        self.name = name

    def getCategory(self):
        return (self.idCategory, self.name)
    
    def setName(self, newName):
        self.name = newName

    def addCategory(self):
        pass


    def __repr__(self):
        return f"Category({self.idCategory}, {self.name})"