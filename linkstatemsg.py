__author__ = 'Allen'


class LinkStateMsg:
    def __init__(self, source, destination, distance, direction):
        self.source = source
        self.destination = destination
        self.distance = distance
        self.direction = direction

    def __str__(self):
        return "%s %s %f %s" % (self.source, self.destination, self.distance, self.direction)
