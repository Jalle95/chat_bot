'''
Intent retrival functions
'''

def indicator(a, b):
    '''
    indicator(a, b) returns 0 if a=b and 1 otherwise
    '''
    if a == b:
        return 0
    return 1


def levenshtein(a, b):
    '''
    levenshtein(a, b) computes the Levenshtein distance between the two
    strings a and b. The Levenshtein distance is minimum number of edits
    (insertions, deletions or substitutions) required to go from one string to
    the other.
    '''
    # Naive implementation that scales super badly. With more time, a better
    # implementation should be made, or a library could be used.
    if min(len(a), len(b)) == 0: # If either a or b is empty
        return max(len(a), len(b)) # Make sufficient inserts
    else:
        return min([
            levenshtein(a[1:], b) + 1, # Insertion b
            levenshtein(a, b[1:]) + 1, # Insertion a
            levenshtein(a[1:], b[1:]) + indicator(a[0], b[0]) # Swap if necessary
            ])


def shortest_levenshtein(keyword, strings):
    '''
    shortest_levenshtein(keyword, strings) returns the string in the list strings
    that has the shortest levenshtein distance to keyword and the corresponding
    levenshtein distance.
    '''
    lev_dist = [levenshtein(keyword, s) for s in strings]
    min_dist = max(lev_dist)
    min_idx = 0
    for i, d in enumerate(lev_dist):
        if d < min_dist:
            min_idx = i
            min_dist = d
    return strings[min_idx], min_dist


def find_intent(intent, possible_intents, lev_th):
    '''
    find_intent(intent, possible_intents, lev_th) compares the input intent
    with the list possible_intents and returns the best fitting intent with
    respect to levenshtein distance. If no possible intent is closer than the
    specified threshhold lev_th, then None is returned.

    This naive implementation of the levenshtein distance scales terribly..
    Efforts should be put into reducing the algorithmic complexity, or a
    library should be used instead. To prevent the function from taking too
    long, a limit of input length is given.
    '''
    if intent in possible_intents: # Exact check of intent
        return intent
    #If no exact match, try levenshtein, but only for inputs shorter than 8 characters
    if len(intent) > 7:
        return None
    closest_intent, lev_dist = shortest_levenshtein(intent, possible_intents)
    if lev_dist < lev_th: # If closest intent is close enough
        return closest_intent
    return None 
