

class Queue:
    objects = []

    def get(self, index):
        return self.objects[index]

    def append(self, obj):
        self.objects.append(obj)

    def shift(self):
        try:
            return self.objects.pop(0)
        except IndexError:
            return None