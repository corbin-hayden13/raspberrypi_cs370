class EventHandler:
    def __init__(self):
        self.events = {}

    def add_event(self, name, function):
        self.events[name] = function

    def handle_event(self, event_request):
        self.events[event_request[0]](event_request[1])

