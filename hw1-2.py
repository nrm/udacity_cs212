# CS 212, hw1-2: Jokers Wild
#
# -----------------
# User Instructions
#
# Write a function best_wild_hand(hand) that takes as
# input a 7-card hand and returns the best 5 card hand.
# In this problem, it is possible for a hand to include
# jokers. Jokers will be treated as 'wild cards' which
# can take any rank or suit of the same color. The
# black joker, '?B', can be used as any spade or club
# and the red joker, '?R', can be used as any heart
# or diamond.
#
# The itertools library may be helpful. Feel free to
# define multiple functions if it helps you solve the
# problem.
#
# -----------------
# Grading Notes
#
# Muliple correct answers will be accepted in cases
# where the best hand is ambiguous (for example, if
# you have 4 kings and 3 queens, there are three best
# hands: 4 kings along with any of the three queens).

import itertools

jocker={'?R':[r+s for r in '23456789TJQK' for s in 'HD'],'?B':[r+s for r in '23456789TJQK' for s in 'SC']}

def best_wild_hand(hand):
    "Try all values for jokers in all 5-card selections."

    # Your code here
    result = 0
    best_hands=[]
    for ihand in [x for x in itertools.combinations(hand, 5)]:
        print 'ihand = %s'%' '.join(ihand)
        if '?B' in ihand and '?R' in ihand:
            print 'Yes'
            result, best_hands = wild_hand2(ihand, ['?B','?R'], result, best_hands)
        if '?B' in ihand and '?R' not in ihand:
            result, best_hands = wild_hand(ihand, '?B', result, best_hands)
        elif '?R' in ihand and '?B' not in ihand:
            result, best_hands = wild_hand(ihand, '?R', result, best_hands)
        elif '?B' not in ihand and '?R' not in ihand:
            print 'not "?" in ihand = %s'%' '.join(ihand)
            result, best_hands = result_wild_hand(result, ihand, best_hands)

    print "\tbest is %s, result is %s"%(best_hands, result)
    return best_hands

def wild_hand(hand, jocker_type, result, best_hands):
    index = hand.index(jocker_type)
    _hand = list(hand)
    #print '\tnew_hand is %s'%_hand
    for el in jocker[jocker_type]:
        new_hand = _hand[:index] + [el] +_hand[index+1:]
        result, best_hands = result_wild_hand(result, new_hand, best_hands)
    return result, best_hands

def wild_hand2(hand, jocker_type, result, best_hands):
    index = hand.index(jocker_type[0])
    _hand = list(hand)
    print '\twild_hand2 new_hand is %s'%_hand
    for el in jocker[jocker_type[0]]:
        new_hand = _hand[:index] + [el] +_hand[index+1:]
        if jocker_type[1] in new_hand:
            result, best_hands = wild_hand(new_hand, jocker_type[1], result, best_hands)
        else:
            result, best_hands = result_wild_hand(result, new_hand, best_hands)
    return result, best_hands

def result_wild_hand(result, new_hand, best_hands):
    cur_result, tmp_best_hands = best_hand(new_hand, best_hands, result)
    if cur_result >= result:
        result = cur_result
        best_hands = tmp_best_hands
    return result, best_hands

def best_hand(hand, best_hands, result):
    "From a 7-card hand, return the best 5 card hand."

    # Your code here
    all_hands = [x for x in itertools.combinations(hand, 5)]
    result = result
    for hand in all_hands:
        ranks = card_ranks(hand)
        if straight(ranks) and flush(hand):
            result, best_hands = res(result, (8, max(ranks)), best_hands, hand)
        elif kind(4, ranks):
            result, best_hands = res(result, (7, kind(4, ranks), kind(1, ranks)), best_hands, hand)
            break
        elif kind(3, ranks) and kind(2, ranks):
            result, best_hands = res(result, (6, kind(3, ranks), kind(2, ranks)), best_hands, hand)
        elif flush(hand):
            result, best_hands = res(result, (5, ranks), best_hands, hand)
        elif straight(ranks):
            result, best_hands = res(result, (4, max(ranks)), best_hands, hand)
        elif kind(3, ranks):
            result, best_hands = res(result, (3, kind(3, ranks), ranks), best_hands, hand)
        elif two_pair(ranks):
            result, best_hands = res(result, (2, two_pair(ranks), ranks), best_hands, hand)
        elif kind(2, ranks):
            result, best_hands = res(result, (1, kind(2, ranks), ranks), best_hands, hand)
        else:
            result, best_hands = res(result, (0, ranks), best_hands, hand)
    return result, best_hands

def res(result, cur_result, best_hands, hand):
    if cur_result >= result:
        result = cur_result
        best_hands = hand
    return result, best_hands


def test_best_wild_hand():
    #assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
    #        == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    #assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
    #        == ['7C', '7D', '7H', '7S', 'JD'])
    return 'test_best_wild_hand passes'

# ------------------
# Provided Functions
#
# You may want to use some of the functions which
# you have already defined in the unit to write
# your best_hand function.

def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks

def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def straight(ranks):
    """Return True if the ordered
    ranks form a 5-card straight."""
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
    """Return the first rank that this hand has
    exactly n-of-a-kind of. Return None if there
    is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None

def two_pair(ranks):
    """If there are two pair here, return the two
    ranks of the two pairs, else None."""
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None

print test_best_wild_hand()
