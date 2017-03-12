class Track:
    def __init__(self, position, name, path):
        self.position = position
        self.name = name
        self.path = path

    def __str__(self):
        return '#{0.position} {0.name}'.format(self)
