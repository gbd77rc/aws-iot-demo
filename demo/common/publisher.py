class Publisher:
    __dispatched = 0
    def __init__(self, events):
        self.events = { event : dict()
                          for event in events }
    
    def __get_subscribers(self, event):
        return self.events[event]

    def register(self, event, who, callback=None):
        if callback == None:
            callback = getattr(who, 'update')
        self.__get_subscribers(event)[who] = callback
    
    def unregister(self, event, who):
        del self.__get_subscribers(event)[who]
    
    def dispatch(self, event, message):
        for _, callback in self.__get_subscribers(event).items():
            self.__dispatched += 1
            callback(event, message)

    def get_dispatch_count(self):
        return self.__dispatched