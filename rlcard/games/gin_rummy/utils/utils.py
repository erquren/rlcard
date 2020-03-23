'''
    File name: gin_rummy/utils.py
    Author: William Hale
    Date created: 2/12/2020
'''

from typing import List, Iterable

import numpy as np

from rlcard.core import Card

valid_rank = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
valid_suit = ['S', 'H', 'D', 'C']

rank_to_deadwood_value = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
                          "T": 10, "J": 10, "Q": 10, "K": 10}


def from_card_id(card_id: int) -> Card:
    ''' Make card from its card_id

    Args:
        card_id: int in range(0, 52)
     '''
    assert 0 <= card_id < 52
    rank_id = card_id % 13
    suit_id = card_id // 13
    rank = Card.valid_rank[rank_id]
    suit = Card.valid_suit[suit_id]
    return Card(rank=rank, suit=suit)


# deck is always in order from AS, 2S, ..., AH, 2H, ..., AD, 2D, ..., AC, 2C, ... QC, KC
_deck = [from_card_id(card_id) for card_id in range(52)]  # want this to be read-only


def from_text(text: str) -> Card:
    assert len(text) == 2
    return Card(rank=text[0], suit=text[1])


def get_deck() -> List[Card]:
    return _deck.copy()


def get_card(card_id: int):
    return _deck[card_id]


def get_card_id(card: Card) -> int:
    rank_id = get_rank_id(card)
    suit_id = get_suit_id(card)
    return rank_id + 13 * suit_id


def get_rank_id(card: Card) -> int:
    return Card.valid_rank.index(card.rank)


def get_suit_id(card: Card) -> int:
    return Card.valid_suit.index(card.suit)


def get_deadwood_value(card: Card) -> int:
    rank = card.rank
    deadwood_value = rank_to_deadwood_value.get(rank, 10)  # default to 10 is key does not exist
    return deadwood_value


def get_deadwood(hand: Iterable[Card], meld_cluster: List[Iterable[Card]], has_extra_card: bool) -> List[Card]:
    meld_cards = [card for meld_pile in meld_cluster for card in meld_pile]
    deadwood = [card for card in hand if card not in meld_cards]
    if deadwood and has_extra_card:
        # drop card with highest deadwood value
        worst_card = max(deadwood, key=lambda card: get_deadwood_value(card))
        deadwood.remove(worst_card)
    return deadwood


def get_deadwood_count(hand: List[Card], meld_cluster: List[Iterable[Card]], has_extra_card: bool) -> int:
    deadwood = get_deadwood(hand=hand, meld_cluster=meld_cluster, has_extra_card=has_extra_card)
    deadwood_values = [get_deadwood_value(card) for card in deadwood]
    return sum(deadwood_values)


def encode_cards(cards: List[Card]):
    plane = np.zeros(52, dtype=int)
    for card in cards:
        card_id = get_card_id(card)
        plane[card_id] = 1
    return plane
