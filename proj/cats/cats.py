"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime
import math

###########
# Phase 1 #
###########


def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    # new = []
    # for element in paragraphs:
    #     if select(element):
    #         new.append(element)
    # if len(new) > k:#length=3(0,1,2) 
    #     return new[k]
    # return ''
    #method 2: without new list
    idx = 0
    for p in paragraphs:
        if select(p):
            if idx == k:
                return p
            idx += 1 #only add index when select() is true
    return ''

    # END PROBLEM 1

def about(topic):
    """Return a select function that returns whether
    a paragraph contains one of the words in TOPIC.

    Arguments:
        topic: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    # def help(paragraph):
    #     list = split(lower(remove_punctuation(paragraph)))#convert it into a list
    #     for p in list:
    #         for t in topic:
    #             t = lower(remove_punctuation(t))
    #             if p == t:
    #                 return True
    #     return False
    # return help
    #method2
    def help(paragraph):
        list = split(lower(remove_punctuation(paragraph)))#convert it into a list
        for t in topic:
            t = lower(remove_punctuation(t))
            if t in list:
                return True
        return False
    return help
    # END PROBLEM 2


def accuracy(typed, source):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of SOURCE that was typed.

    Arguments:
        typed: a string that may contain typos
        source: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    source_words = split(source)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    # score = 0
    # if len(typed_words) == 0 and len(source_words) == 0:
    #     return 100.0
    # elif len(typed_words) == 0 or len(source_words) == 0:
    #     return 0.0

    # if len(typed_words) <= len(source_words):
    #     for i in range(len(typed_words)):
    #         if typed_words[i] == source_words[i]:
    #             score += 1
    #     return round((score/len(typed_words))*100,1)
    # elif len(typed_words) > len(source_words):
    #     for i in range(len(source_words)):
    #         if typed_words[i] == source_words[i]:
    #             score += 1
    #     return round((score/len(typed_words))*100,2)
    # method 2
    t_len, s_len = len(typed_words), len(source_words)
    if t_len == 0 and s_len == 0:
        return 100.0
    elif t_len == 0 or s_len == 0:
        return 0.0
    score = 0
    for i in range(min(t_len, s_len)):
        if typed_words[i] == source_words[i]:
            score += 1
    return score*100.0 / t_len
    # END PROBLEM 3

def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    l = len(typed)/5
    return (l/elapsed)*60.0
    # END PROBLEM 4

###########
# Phase 2 #
###########

def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD. Instead returns TYPED_WORD if that difference is greater
    than LIMIT.

    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing source words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if typed_word in word_list:
        return typed_word
    minnum = limit+10
    close_word = typed_word
    for word in word_list:
        diff = diff_function(typed_word, word, limit)
        if diff < minnum and diff <= limit:
            minnum = diff
            close_word = word 
    return close_word

    # END PROBLEM 5

def feline_fixes(typed, source, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create SOURCE, then adds the difference in
    their lengths and returns the result.

    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> feline_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> feline_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> feline_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> feline_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> feline_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    '''
    len_t, len_s = len(typed), len(source)
    if len_t == 0 and len_s == 0:
        return 0
    elif len_t == 0 or len_s == 0:
        return abs(len_t - len_s)
    elif typed[0] != source[0]:
        return min(1 + feline_fixes(typed[1:], source[1:], limit-1), limit+1)
    else:
        return min(feline_fixes(typed[1:], source[1:], limit), limit+1)
    '''
    def help(typed, source, cnt):
        len_t, len_s = len(typed), len(source)
        if cnt > limit:
            return limit+1
        if len_t == 0 and len_s == 0:
            return cnt
        elif len_t == 0 or len_s == 0:
            return min(cnt+abs(len_t - len_s), limit+1)
        elif typed[0] != source[0]:
            return help(typed[1:], source[1:], cnt+1)
        else:
            return help(typed[1:], source[1:], cnt)
    return help(typed, source, 0)

    # END PROBLEM 6


def minimum_mewtations(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL.
    This function takes in a string START, a string GOAL, and a number LIMIT.
    Arguments:
        start: a starting word
        goal: a goal word
        limit: a number representing an upper bound on the number of edits
    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
    
    start_l, goal_l = len(start), len(goal)
    if start_l == 0 or goal_l == 0:  # Fill in the condition
        return min(start_l + goal_l, limit+1)
    elif start[0] == goal[0]:  # Feel free to remove or add additional cases
        return min(minimum_mewtations(start[1:], goal[1:], limit), limit+1)
    else:
        add = 1 + minimum_mewtations(start, goal[1:], limit)
        remove = 1 + minimum_mewtations(start[1:], goal, limit)
        substitute = 1 + minimum_mewtations(start[1:], goal[1:], limit)
        return min(add, remove, substitute, limit+1)
        

# LeetCode 72 (Hard): https://leetcode.com/problems/edit-distance/
def final_diff(typed, source, limit):
    """A diff function that takes in a string TYPED, a string SOURCE, and a number LIMIT.
    If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function.'


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far. Your progress is a ratio of the words in the prompt 
    that you have typed correctly, up to the first incorrect word, divided by the number of prompt words

    Arguments:
        typed: a list of the words typed so far
        prompt: a list of the words in the typing prompt
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> prompt = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, prompt, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], prompt, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    cnt = 0
    for t in range(len(typed)):
        if typed[t] == prompt[t]:
            cnt += 1
        else:
            break
    dic = {'id': user_id, 'progress': cnt/len(prompt)}
    upload(dic)
    return cnt/len(prompt)

    # END PROBLEM 8


def time_per_word(words, times_per_player):
    """Given timing data, return a match dictionary, which contains a
    list of words and the amount of time each player took to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> match["words"]
    ['collar', 'plush', 'blush', 'repute']
    >>> match["times"]
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    
    #do not know where wrong
    time = []
    time_all = []
    for i in range(len(times_per_player)):
        player = times_per_player[i]
        for j in range(len(player)-1):
            time.append(player[j+1]-player[j])
        time_all.append(time)
        time = []
    #match = {'words':words, 'times':time_all} this is wrong
    return match(words, time_all)
    
    # wo = words

    # # ti = [[0] * (len(times_per_player[0]) - 1)] * len(times_per_player)
    # # This is wrong due to the difference of copy and deepcopy.
    # ti = [None] * len(times_per_player) #ti = [None, None...]

    # for i in range(len(times_per_player)):

    #     ti[i] = [0] * (len(times_per_player[0]) - 1)

    #     player = times_per_player[i]
    #     for j in range(len(player) - 1):
    #         ti[i][j] = player[j + 1] - player[j]
    # return match(wo, ti)
    # END PROBLEM 9


def fastest_words(match):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        match: a match dictionary as returned by time_per_word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    player_indices = range(len(get_all_times(match)))  # contains an *index* for each player
    word_indices = range(len(get_all_words(match)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    fastest = [None] * len(get_all_times(match))#fatest=[None, None, None...]
    for j in player_indices:
        fastest[j] = [] # [[], [], []...]
    #fatest = [[]]*len(get_all_times(match)) # [[], [], []...] this is wrong!!!

    for i in word_indices:
        word = get_word(match, i)
        min_j, min_time = 0, time(match, 0, i)
        for j in player_indices:
            player = time(match, j, i)
            if player < min_time:
                min_time = player
                min_j = j
        fastest[min_j].append(word)
    return fastest

    # END PROBLEM 10


def match(words, times):
    """A dictionary containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return {"words": words, "times": times}


def get_word(match, word_index):
    """A utility function that gets the word with index word_index"""
    assert 0 <= word_index < len(match["words"]), "word_index out of range of words"
    return match["words"][word_index]


def time(match, player_num, word_index):
    """A utility function for the time it took player_num to type the word at word_index"""
    assert word_index < len(match["words"]), "word_index out of range of words"
    assert player_num < len(match["times"]), "player_num out of range of players"
    return match["times"][player_num][word_index]


def get_all_words(match):
    """A selector function for all the words in the match"""
    return match["words"]


def get_all_times(match):
    """A selector function for all typing times for all players"""
    return match["times"]


def match_string(match):
    """A helper function that takes in a match dictionary and returns a string representation of it"""
    return f"match({match['words']}, {match['times']})"


enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(source)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, source))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
