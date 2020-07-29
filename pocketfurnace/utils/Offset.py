class Offset:

    def __init__(self, i=0):
        self.index = int(i)

    def top_increment(self):
        self.index = self.index + 1
        return self.index

    def top_abatement(self):
        self.index = self.index - 1
        return self.index

    def back_increment(self):
        i = self.index
        self.index = i + 1
        return i

    def back_abatement(self):
        i = self.index
        self.index = i - 1
        return i

    def set(self, i):
        self.index = int(i)

    def __add__(self, other):
        self.index = self.index + int(other)
        return self.index

    def __sub__(self, other):
        self.index = self.index - int(other)
        return self.index

    def __int__(self):
        return self.index
