class Event():
    def __init__(self):
        self.title = 'No title set'
        self.time = 'No time set'
        self.loc = 'No location set'
        self.attendees = set()

    def set_title(self, title):
        self.title = title

    def set_time(self, time):
        self.time = time

    def set_loc(self, loc):
        self.loc = loc

    def get_details(self):
        return "{}\n{}\n{}\nAttendees:\n{}".format(self.title, self.time, self.loc, '\n'.join(list(self.attendees)))

    def add_attendee(self, name):
        self.attendees.add(name)

    def __str__(self):
        return self.title
