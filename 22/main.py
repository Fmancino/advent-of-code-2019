#!/usr/bin/env python3
import sys
import argparse
import re

def deal_into_new_stack(deck, N=None):
    deck.reverse()
    return deck

def cut_N_cards(deck, N):
    return deck[N:] + deck[:N]

def deal_with_increment_N(deck, N):
    deck_len = len(deck)
    table = [-1] * deck_len
    pos = 0
    for card in deck:
        table[pos] = card
        pos = (pos + N) % deck_len
    return table

def deal_into_new_stack_pos(size, pos, N=None):
    return size - pos - 1

def cut_N_cards_pos(size, pos, N):
    return (pos - N) % size

def deal_with_increment_N_pos(size, pos, N):
    return (N * pos) % size

shuffle_handler = [ (re.compile("deal with increment (\d+)"), deal_with_increment_N),
                (re.compile("deal into new stack"), deal_into_new_stack),
                (re.compile("cut (-?\d+)"), cut_N_cards)]

shuffle_handler_pos = [ (re.compile("deal with increment (\d+)"), deal_with_increment_N_pos),
                (re.compile("deal into new stack"), deal_into_new_stack_pos),
                (re.compile("cut (-?\d+)"), cut_N_cards_pos)]

def match(line, sh_handler):
    for pattern, function in sh_handler:
        obj = pattern.match(line)
        if obj:
            try:
                n = int(obj.group(1))
            except IndexError:
                n = None
            return function, n
    raise ValueError



def main():

    parser = argparse.ArgumentParser(description='Shuffle space cards')
    parser.add_argument('--num_cards', type=int,
                                help='the number of space cards in deck', default= 10007)
    parser.add_argument('--start_pos', type=int,
                                help='the position you are interested in', default= 2019)
    parser.add_argument('--times', type=int,
                                help='the number of times you mix', default= 2019)
    args = parser.parse_args()
    std_in = sys.stdin.readlines()
    print(f"number of cards: {args.num_cards}")
    parsed_input = []
    parsed_input_pos = []
    for line in std_in:
        function, arg = match(line, shuffle_handler)
        parsed_input.append((function, arg))

    for line in std_in:
        function, arg = match(line, shuffle_handler_pos)
        parsed_input_pos.append((function, arg))


    #  deck = list(range(args.num_cards))
    #  for function, arg in parsed_input:
        #  #  print(deck)
        #  deck = function(deck, arg)
    #  print(deck)
    #  print("first star")
    #  print(deck.index(args.start_pos))

    print("first star pos")
    pos = args.start_pos
    for i in range(args.times):
        #  print(pos)
        for function, arg in parsed_input_pos:
            #  print(pos)
            pos = function(args.num_cards, pos, arg)
        if pos == args.start_pos:
            print("circle")
    print(pos)

    #---- seconds part
    #  huge_deck_size = 119315717514047
    #  pos = 2020
    #  times_to_do = 101741582076661
    #  left = times_to_do

    #  for i in range(times_to_do):
        #  left -= 1
        #  print(f"left = {left}")
        #  for function, arg in parsed_input_pos:
            #  pos = function(huge_deck_size, pos, arg)

    #  print("second star")
    #  print(pos)

if __name__ == "__main__":
    main()
