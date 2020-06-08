class Notice():
    '''
    Notice is a container for notices for service reps at Bewhous. It contains
        ID - Unique ID that allow customer reps to asses the notice
        Type - Type of notice (search, etc.)
        Message - A message associated with the notice

    The class can easily be exstended with more relevant information.
    '''

    def __init__(self, id_, typ, message, time):
        self.id = id_
        self.type = typ
        self.message = message
        self.time = time


    def print_summary(self):
        '''
        Prints a summary of the relevant information
        '''
        print('Notice ID:', self.id)
        print('Recived:', self.time)
        print('Type:', self.type)
        print('Message:', self.message)
