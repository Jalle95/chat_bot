# Chat bot
This repository contains my implementation of a chat bot, developed in Python. The chat bot can be accessed by running the file chat_bot.py with Python3.5.3 or similar (I think most Python3.X will work). All other files in the repository must be placed in the same folder as chat_bot.py for it to work. By running the chat bot in a terminal, messages can sent and received.

## Chatting with bot
Chatting with the bot should be straight forward. If the user writes a message to the bot that it cannot understand it will reply with a list of helpful keywords that trigger the implemented commands. The implemented commands are:

- help : Displays the keywords that trigger the chat bot
- search : Search for brands of a type of item in the catalogue. A keyword can be specified with the command or after. 
- goodbye : Ends the conversation with the chat bot

If a user searches for a type of item that is not in the catalogue of items, a notice is appended to the list of active notices, which can be addressed by customer representatives through the configuration board.

The configuration board can be accessed by sending the 'secret' command 'config' to the chat bot.

## Configuration board

The configuration board is hidden behind a password that is: **test1234**. The board works similar to the chat bot. Different commands let the customer representative do different things. The available commands are:
- help : Display the available commands
- print : Display the current active notices. A type of notices can be used as a filter, even though the implementation only has one type of notice, namely notices associated with unknown searches.
- add : Add an item to the catalogue of items. A link is specified, from which the system should retrieve the relevant data. The crawling function is not implemented, but to show the functionality a random item is created and added to the catalogue of items.
- remove : Remove an item for the catalogue of items by specifying the link associated with the item.
- resolve : Resolve an active notice by specifying the ID of the notice. The resolved notice is removed from the list of active notices.
- exit : Exit the configuration board and return to the chat bot conversation.

## Intent analyzer
Misspelling in text messages are common. The chat bot has an implemented intent analyzer that allows the bot to recognize commands even if they are slightly misspelled. The intent analysing function is found in the file intent_lib.py. The functions uses the Levenshtein distance to compare the recieved message with a list of the available commands. The tolerance of allowed difference is controlled with a variable.

The Levenshtein distance between two strings is the minimal number of edits (insertions, deletions or substitutions) required to transform one string to the other. My implementation of the distance is simple. Given more time I would reduce the algorithmic complexity, or use a library that has a faster implementation.
