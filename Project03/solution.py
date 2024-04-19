"""
Nathan Gu and Blake Potvin
Sorting Project - Starter
CSE 331 Fall 2023
"""

import random
import time
from typing import TypeVar, List, Callable, Dict, Tuple
from dataclasses import dataclass

T = TypeVar("T")  # represents generic type


# do_comparison is an optional helper function but HIGHLY recommended!!!
def do_comparison(first: T, second: T, comparator: Callable[[T, T], bool], descending: bool) -> bool:
    """
    Compare two elements given the comparator

    Parameters: first, second, comparator, descending
    Returns: bool True/False whether comparison is successful or not
    """
    if descending:
        return comparator(second, first)
    else:
        return comparator(first, second)


def selection_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
    Sorts a list in place using selection sort algorithm

    Parameters: data, comparator, descending
    Return: None
    """
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if do_comparison(data[j], data[min_idx], comparator, descending):
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]


def bubble_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                descending: bool = False) -> None:
    """
    Sorts list in place using bubble sort algorithm

    Parameters: data, comparator, descending
    Return: None
    """
    n = len(data)
    for i in range(n-1):
        swapped = False
        for j in range(0, n-i-1):
            if do_comparison(data[j+1], data[j], comparator, descending):
                data[j], data[j+1] = data[j+1], data[j]
                swapped = True
        if not swapped:
            break


def insertion_sort(data: List[T], *, comparator: Callable[[T, T], bool] = lambda x, y: x < y,
                   descending: bool = False) -> None:
    """
S   orts list in place using insertion sort algorithm

    Parameters: data, comparator, descending
    Return: None
    """
    n = len(data)
    for i in range(1, n):
        key = data[i]
        j = i - 1
        while j >= 0 and do_comparison(key, data[j], comparator, descending):
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key

def merge(part1, part2, data, comparator, descending):
    '''
    Merges two sub-arrays into a single sorted array

    Parameters: part1, part2, data, comparator, descending
    Returns: None
    '''
    i = j = 0

    while i + j < len(data):
        if j == len(part2) or (i < len(part1) and do_comparison(part1[i], part2[j], comparator = comparator, descending=descending)):
            data[i+j] = part1[i]
            i += 1
        else:
            data[i+j] = part2[j]
            j += 1
def hybrid_merge_sort(data: List[T], *, threshold: int = 12,
                      comparator: Callable[[T, T], bool] = lambda x, y: x < y, descending: bool = False) -> None:
    """
    Sorts list in place using hybrid merge sort algorithm

    Parameters: data, threshold, comparator, descending
    Return: None
    """
    if len(data) < 2:
        return
    if len(data) <= threshold:
        insertion_sort(data, comparator = comparator, descending = descending)
    else:
        mid = len(data) // 2
        left = data[:mid]
        right = data[mid:]

        hybrid_merge_sort(left, threshold = threshold, comparator = comparator, descending = descending)
        hybrid_merge_sort(right, threshold = threshold, comparator = comparator, descending = descending)
        merge(left, right, data, comparator, descending)

def maximize_rewards(item_prices: List[int]) -> Tuple[List[Tuple[int, int]], int]:
    '''
    Splits input list of item prices so that sum of each pair is consistent. Calculates
    reward points for all pairs

    Parameters: item prices
    Returns: tuple containing list of tuples which are pairs of the item prices
    '''
    tuples = []
    points = 0

    if len(item_prices) == 0 or len(item_prices) % 2 == 1:
        return ([], -1)

    hybrid_merge_sort(item_prices)

    check_val = item_prices[0] + item_prices[-1]
    condition = all(check_val == item_prices[i] + item_prices[-i - 1] for i in range(len(item_prices) // 2))

    if condition:
        tuples = [(item_prices[i], item_prices[-i - 1]) for i in range(len(item_prices) // 2)]
        points = sum(x * y for x, y in tuples)

    return (tuples, points) if condition else ([], -1)