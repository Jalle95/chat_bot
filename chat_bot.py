'''
chat bot is a program that can process test specified by a user, analyze the
intent hidden in the text and perform a command from a predefined list. By giving
the 'secret' command 'config', the configuration board is opened. From here,
items can be added to the list of items, and notices can be viewed and
resolved.
'''
import hashlib
import datetime
import random

import Item
import Notice
import intent_lib

def conversation(lev_threshold):
    '''
    Conversation loop. A user can send lines of text, which the system
    interprets using a set of predefined commands. lev_threshold specifies the
    systems tolerence with respect to misspelling of a command.
    '''
    def print_help(commands, descriptions):
        '''
        print_help displays the available commands
        '''
        print('I can help you with the following:')
        for command, description in zip(commands, descriptions):
            print(command, '-', description)


    def search(keyword, items):
        '''
        search(keyword) lists items with type mathcing the specified keyword.
        If no type matches the keyword or no keyword is given, the user will
        be asked to give a/another keyword to search for. Matching items are
        returned
        '''
        matches = [] # Container for keyword matches
        if keyword: # If keyword is given with the command
            keyword = keyword.lower()
            for item in items:
                if item.type == keyword:
                    matches.append(item)

        if len(matches) == 0: # If no matches were found
            keyword = input('What kind of item are you looking for?: ')
            keyword = keyword.lower()
            for item in items:
                    if item.type == keyword:
                        matches.append(item)

        if len(matches) == 0: # If no matches were found
            new_notice = Notice.Notice( # Create notice for customer reps
                len(notices), # ID
                'search', # Type of notice
                'Customer searched the product: ' + keyword, # Message
                datetime.datetime.now(), # Time of creation
                )
            notices.append(new_notice) # Append to global list of notices
        return matches

    # Defintion of items and notices
    global items, notices

    possible_commands = [
        'help',
        'search',
        'goodbye',
        'config',
        ]
    possible_commands_descriptions = [
        'Displays this message',
        'If you want search for a type of item in the catalogue',
        'Lets me know that you do not need more help',
        ]

    while True: # Run coversation until goodbye is specified
        inp = input()
        inp = inp.split(' ') # Split input into words
        intent = inp[0].lower()
        intent = intent_lib.find_intent(intent, possible_commands, lev_threshold)
        if intent in ['help', None]:
            print_help(possible_commands[:-1], possible_commands_descriptions) # We dont want to tell the user about the config command hence :-1

        elif intent == 'search':
            if len(inp) == 1: # If keyword is not specified with command
                keyword = None
            else:
                keyword = ' '.join(inp[1:])
            matches = search(keyword, items)
            if len(matches) == 0:
                print('I could not find any items matching the given keyword')
            else:
                print('Here are the search results:')
                for match in matches:
                    print('###############')
                    match.print_summary()

        elif intent == 'config':
            configuration_board(lev_threshold) # Enter the configutation board loop

        elif intent == 'goodbye':
            print('I hope that I was able to help you. Goodbye!')
            exit()

        print()
        print('Let me know if I can help you with anything else:')


def configuration_board(lev_threshold):
    '''
    Configuration board loop. The user must specify the correct password to
    access to configuration board. The user can then specify a command from a
    predefined list. After completion of a command, the user can specify a
    new command. When exitting the configuration board, the user is returned
    to the conversation loop. lev_threshold specifies the systems tolerence
    with respect to misspelling of a command.
    '''
    def check_password(passwd):
        '''
        check_password(passwd) checks if passwd is the correct password.
        Passwords should obviously never be stored as plain text, but
        for this task it is: test1234.
        '''
        if hashlib.sha256(passwd.encode()).hexdigest() == '937e8d5fbb48bd4949536cd65b8d35c426b80d2f830c5c308e2cdec422ae2244':
            return True
        return False


    def print_help(commands, descriptions):
        '''
        print_help displays the available commands
        '''
        print('Available commands:')
        for command, description in zip(commands, descriptions):
            print(command, '-', description)


    def print_notices(type_, local_notices):
        '''
        print_notices(local_notices) prints the all notices with the matching type_
        '''
        print('Displaying all notices:')
        for notice in local_notices:
            if type_ in [notice.type, 'all']:
                print('#######################')
                notice.print_summary()
        print('#######################')


    def retrieve_info(link):
        '''
        retrieve_info retrieves the relevant information from the spefied link.
        The current function generates a random product.
        '''
        #info = crawl(link) # A function should crawl the link and extract the relevant information

        #Generate random item:
        adjective = ['Cool', 'Crazy', 'Dull', 'Sharp', 'Rusty']
        types = ['hammer', 'nail', 'saw']
        type_ = types[random.randint(0, 2)]
        brand = adjective[random.randint(0, 4)] + type_
        price = random.randint(0, 1000)
        stock = random.randint(0, 100)

        new_item = Item.Item(type_, brand, price, stock, link)
        print('The following information has been retrieved from the link:')
        print('#######################')
        new_item.print_summary()
        print('#######################')
        return new_item


    def detect_item(link, local_items):
        '''
        detect_item(link) returns the index of the item in the list of items
        assocated with the given link. If no link matches, the function
        returns -1.
        '''
        for idx, item in enumerate(local_items):
            if item.link == link:
                return idx
        return -1


    def detect_notice(id_, local_notices):
        '''
        detect_notice(link) returns the index of notice in the list of notices
        assocated with the given id.
        If no id matches, the function returns -1.
        '''
        for idx, notice in enumerate(local_notices):
            if notice.id == int(id_):
                return idx
        return -1

    print('Please specify the password for the configuration board')
    password_tries = 0
    while password_tries < 3:
        passwd = input('Password: ')
        if check_password(passwd):
            break
        password_tries += 1
        print('Wrong password, try again')
    if password_tries >= 3:
        print('You typed the password wrong too many times.')
        print('Closing the configuation board')
        return 0

    # Load commands similar to the conversation loop
    global notices, items
    possible_commands = [
        'help',
        'print',
        'add',
        'remove',
        'resolve',
        'exit'
        ]
    possible_commands_descriptions = [
        'Prints this list of commands',
        'Prints current notices. Allows for specication of notice type',
        'Add an item to the list of items',
        'Remove an item from the list of items',
        'Resolve a notice',
        'Exit the configuration board'
        ]
    print()
    print('##########################################')
    print('### Welcome to the configuration board ###')
    print('##########################################')
    print()
    print_help(possible_commands, possible_commands_descriptions)

    while True: # Run configuration board until exit command is given
        inp = input()
        inp = inp.split(' ')
        intent = inp[0].lower()
        intent = intent_lib.find_intent(intent, possible_commands, lev_threshold)

        if intent == 'help':
            print_help(possible_commands, possible_commands_descriptions)

        elif intent == 'print':
            keyword = input('Specify which type of notices you would like to see: ')
            possible_keywords = set([notice.type for notice in notices])
            if keyword not in possible_keywords:
                keyword = 'all'
            print_notices(keyword, notices)

        elif intent == 'add':
            link = input('Specify link to the item you would like to add: ')
            new_item = retrieve_info(link)
            items.append(new_item)

        elif intent == 'remove':
            link = input('Specify link to the item you would like to remove: ')
            remove_idx = detect_item(link, items)
            if remove_idx >= 0:
                print('Are you sure you want to delete them folowing item:')
                print('#######################')
                items[remove_idx].print_summary()
                print('#######################')
                answer = input('Answer (y/n): ')
                while answer  not in ['y', 'n']:
                    print('Please answer y (yes) or n (no)')
                    answer = input('Answer (y/n): ')
                if answer == 'y':
                    del items[remove_idx]
                    print('Removed the item')
                else:
                    print('Did not remove the item')
            else:
                print('No mathcing item was found')

        elif intent == 'resolve':
            id_ = input('Specify id of the notice you would like to resolve: ')
            resolve_idx = detect_notice(id_, notices)
            if resolve_idx >= 0:
                print('Are you sure you want to resolve them folowing notice:')
                print('#######################')
                notices[resolve_idx].print_summary()
                print('#######################')
                answer = input('Answer (y/n): ')
                while answer  not in ['y', 'n']:
                    print('Please answer y (yes) or n (no)')
                    answer = input('Answer (y/n): ')
                if answer == 'y':
                    print('Resolved the notice')
                    del notices[resolve_idx]
                else:
                    print('Did not resolve the notice')
            else:
                print('No notice was not found')

        elif intent == 'exit':
            print('Exitting the configuration board...')
            return 0

        else:
            print('Did not understand the given command')

        print()


if __name__ == '__main__':
    # Setup of thresholds
    lev_threshold = 3 # Levenshtein distance threshold (Edit distance)

    # Creation of database
    hammertime = Item.Item('hammer', 'Hammertime', 250, 3, 'www.bewhaos.com/hammertime')
    hardhit = Item.Item('hammer', 'Hardhit', 150, 20, 'www.bewhaos.com/hardhit')
    sawk = Item.Item('saw', 'Sawk', 250, 10, 'www.bewhaos.com/sawk')
    nailed = Item.Item('nail', 'Nailed it', 2, 100, 'www.bewhaos.com/nailed')
    items = [
        hammertime,
        hardhit,
        sawk,
        nailed
        ]

    #Defintion of a global list of notices for customer reps
    search1 = Notice.Notice(0, 'search', 'Customer searched the product: paint', datetime.datetime.now())
    search2 = Notice.Notice(1, 'search', 'Customer searched the product: brush', datetime.datetime.now())
    notices = [
        search1,
        search2
        ]

    print('Hello, how can I help you?')
    conversation(lev_threshold)
