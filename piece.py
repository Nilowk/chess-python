class Piece:

    def __init__(self, name, *allowed):
        self.name = name
        self.allowed = allowed

    def get_movement(self):
        return self.allowed

    def get_color(self):
        if self.name[0] == "w":
            return "white"
        elif self.name[0] == "b":
            return "black"
        else:
            return "void"
