"""
Project 5: Deque
CSE 331 FS23
Authored by Gabriel Sotelo
starter.py
"""

import gc
from typing import TypeVar, List
from random import randint, shuffle
from timeit import default_timer
# COMMENT OUT THIS LINE (and `plot_speed`) if you don't want matplotlib
#from matplotlib import pyplot as plt

T = TypeVar('T')
CDLLNode = type('CDLLNode')

class CircularDeque:
    """
    Representation of a Circular Deque using an underlying python list
    """

    __slots__ = ['capacity', 'size', 'queue', 'front', 'back']

    def __init__(self, data: List[T] = None, front: int = 0, capacity: int = 4):
        """
        Initializes an instance of a CircularDeque
        :param data: starting data to add to the deque, for testing purposes
        :param front: where to begin the insertions, for testing purposes
        :param capacity: number of slots in the Deque
        """
        if data is None and front != 0:
            # front will get set to 0 by front_enqueue if the initial data is empty
            data = ['Start']
        elif data is None:
            data = []

        self.capacity: int = capacity
        self.size: int = len(data)
        self.queue: List[T] = [None] * capacity
        self.back: int = None if not data else self.size + front - 1
        self.front: int = front if data else None

        for index, value in enumerate(data):
            self.queue[index + front] = value

    def __str__(self) -> str:
        """
        Provides a string representation of a CircularDeque
        'F' indicates front value
        'B' indicates back value
        :return: the instance as a string
        """
        if self.size == 0:
            return "CircularDeque <empty>"

        str_list = [f"CircularDeque <"]
        for i in range(self.capacity):
            str_list.append(f"{self.queue[i]}")
            if i == self.front:
                str_list.append('(F)')
            elif i == self.back:
                str_list.append('(B)')
            if i < self.capacity - 1:
                str_list.append(',')

        str_list.append(">")
        return "".join(str_list)

    __repr__ = __str__

    # ============ Modifiy Functions Below ============#

    def __len__(self) -> int:
        """
        Returns length of the circular deque

        param: self
        return: integer representing length
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Returns a boolean indicating if the circular deque is empty

        param: self
        return: True if empty, False otherise
        """
        return self.size == 0

    def front_element(self) -> T:
        """
        Returns first element in the circular deque

        params: self
        return: first element, if it exists, otherwise None
        """
        if self.size > 0:
            return self.queue[self.front]
        return None

    def back_element(self) -> T:
        """
        Returns last element in the circular deque

        params: self
        returns: last element if it exists, otherwise None
        """
        if self.size > 0:
            return self.queue[self.back]
        return None

    def grow(self) -> None:
        """
        Doubles the capactity of CD by creating new list with double the capacity of the old one and copies the calues from the current list

        params: self
        retern: None
        """
        new = [None] * (len(self.queue) * 2)
        ptr = self.front
        i = 0
        if self.front is not None:
            while i < len(self.queue):
                new[i] = self.queue[ptr]
                if ptr == len(self.queue) - 1:
                    ptr = 0
                else:
                    ptr += 1
                i += 1

            self.front = 0
            self.back = self.size - 1  # check placement/order if having problems with later tests

        self.queue = new
        self.capacity = len(self.queue)


    def shrink(self) -> None:
            """
            Copy over contents of the old list to a new list with half the capacity

            params: self
            retuns: None
            """
            new = [None] * (len(self.queue) // 2)
            ptr = 0  # ptr to insertion in new
            i = 0
            if self.front is not None:
                while i < len(self.queue) and ptr < len(new):
                    if self.back > self.front:  # no wrap-around
                        if i >= self.front and i <= self.back:
                            new[ptr] = self.queue[i]
                            ptr += 1
                        else:
                            new[ptr] = None
                    elif self.back < self.front:  # wrap-around case
                        if i <= self.front and i >= self.back:
                            new[ptr] = self.queue[i]
                            ptr += 1
                        else:
                            new[ptr] = None
                    i += 1

                self.front = 0
                self.back = self.size - 1  # check placement/order if having problems with later tests

            self.queue = new
            self.capacity = len(self.queue)


    def enqueue(self, value: T, front: bool = True) -> None:
            """
            Add a value to either the front or back of the circular dque based off the parameter front

            params: self, value, front
            return: None
            """
            if not self.is_empty():
                if front is True:
                    self.queue[self.front - 1] = value
                    self.front -= 1

                else:
                    self.queue[self.back + 1 - len(self.queue)] = value
                    if self.back == len(self.queue) - 1:
                        self.back = self.back + 1 - len(self.queue)
                    else:
                        self.back = self.back + 1

            else:
                self.queue[0] = value
                self.front = 0
                self.back = 0

            self.size += 1
            if self.front < 0:
                self.front = self.front + len(self.queue)

            if self.size == self.capacity:
                self.grow()

    def dequeue(self, front: bool = True) -> T:
        """
        Removes an item from the queue

        params: self, front, book
        return: removed item, None if empty
        """
        removed = None
        if self.size == 0:
            return None

        if not self.is_empty():
            if front is True:
                removed = self.queue[self.front]
                self.front += 1

            else:
                removed = self.queue[self.back]
                if self.back == 0:
                    self.back = len(self.queue) - 1
                else:
                    self.back -= 1

            self.size -= 1

            if self.front == len(self.queue):
                self.front = 0

            if self.size <= (self.capacity // 4) and (self.capacity // 2) >= 4:
                self.shrink()

            return removed

        return None

class CDLLNode:
    """
    Node for the CDLL
    """

    __slots__ = ['val', 'next', 'prev']

    def __init__(self, val: T, next: CDLLNode = None, prev: CDLLNode = None) -> None:
        """
        Creates a CDLL node
        :param val: value stored by the next
        :param next: the next node in the list
        :param prev: the previous node in the list
        :return: None
        """
        self.val = val
        self.next = next
        self.prev = prev

    def __eq__(self, other: CDLLNode) -> bool:
        """
        Compares two CDLLNodes by value
        :param other: The other node
        :return: true if comparison is true, else false
        """
        return self.val == other.val

    def __str__(self) -> str:
        """
        Returns a string representation of the node
        :return: string
        """
        return "<= (" + str(self.val) + ") =>"

    __repr__ = __str__


class CDLL:
    """
    A (C)ircular (D)oubly (L)inked (L)ist
    """

    __slots__ = ['head', 'size']

    def __init__(self) -> None:
        """
        Creates a CDLL
        :return: None
        """
        self.size = 0
        self.head = None

    def __len__(self) -> int:
        """
        :return: the size of the CDLL
        """
        return self.size

    def __eq__(self, other: 'CDLL') -> bool:
        """
        Compares two CDLLs by value
        :param other: the other CDLL
        :return: true if comparison is true, else false
        """
        n1: CDLLNode = self.head
        n2: CDLLNode = other.head
        for _ in range(self.size):
            if n1 != n2:
                return False
            n1, n2 = n1.next, n2.next
        return True

    def __str__(self) -> str:
        """
        :return: a string representation of the CDLL
        """
        n1: CDLLNode = self.head
        joinable: List[str] = []
        while n1 is not self.head:
            joinable.append(str(n1))
            n1 = n1.next
        return ''.join(joinable)

    __repr__ = __str__

    # ============ Modifiy Functions Below ============#

    def insert(self, val: T, front: bool = True) -> None:
        """
        inserts a node with value val in the front or back of the CDLL

        params: self, val, front
        return: None
        """
        new = CDLLNode(val)

        if self.size == 0:
            self.head = new
            self.head.prev = self.head
            self.head.next = self.head

        elif front:
            new.next = self.head
            new.prev = self.head.prev
            self.head.prev.next = new
            self.head.prev = new
            self.head = new
        else:
            new.prev = self.head.prev
            new.next = self.head
            self.head.prev.next = new
            self.head.prev = new

        self.size += 1

    def remove(self, front: bool = True) -> None:
        """
        removes a node from the CDLL, if the list is empty do nothing

        params: self, front
        return: None
        """
        if self.size == 0:
            return

        elif self.size == 1:
            self.head.prev = None
            self.head.next = None
            self.head = None

        elif front:
            self.head.prev.next = self.head.next
            self.head.next.prev = self.head.prev
            self.head = self.head.next

        else:
            self.head.prev.prev.next = self.head
            self.head.prev = self.head.prev.prev

        self.size -= 1


class CDLLCD:
    """
    (C)ircular (D)oubly (L)inked (L)ist (C)ircular (D)equeue
    This is essentially just an interface for the above
    """

    def __init__(self) -> None:
        """
        Initializes the CDLLCD to an empty CDLL
        :return: None
        """
        self.CDLL: CDLL = CDLL()

    def __eq__(self, other: 'CDLLCD') -> bool:
        """
        Compares two CDLLCDs by value
        :param other: the other CDLLCD
        :return: true if equal, else false
        """
        return self.CDLL == other.CDLL

    def __str__(self) -> str:
        """
        :return: string representation of the CDLLCD
        """
        return str(self.CDLL)

    __repr__ = __str__

    # ============ Modifiy Functions Below ============#
    def __len__(self) -> int:
        """
        Returns lenth of the CDLLCD

        params: self
        return: integer representing length of the CDLLCD
        """
        return len(self.CDLL)

    def is_empty(self) -> bool:
        """
        Returns bool indicating if the CDLLCD is empty or not

        params: self
        return True if empty, False otherwise
        """
        return len(self.CDLL) == 0

    def front_element(self) -> T:
        """
        Returns the first element in the CDLLCD

        params: self
        return: the first element if it exits, otherwise None
        """
        if self.CDLL.head is not None:
            return self.CDLL.head.val
        else:
            return None

    def back_element(self) -> T:
        """
        Returns last element in the CDLLCD

        params: self
        return: last element if it exits, otherwise None
        """
        if self.CDLL.head is not None and self.CDLL.head.prev is not None:
            return self.CDLL.head.prev.val
        else:
            return None

    def enqueue(self, val: T, front: bool = True) -> None:
        """
        Adds a value to the CDLLCD

        params: self, val, front
        return: None
        """

        self.CDLL.insert(val, front)

    def dequeue(self, front: bool = True) -> T:
        """
        Removes a value from the deque, returning it

        params: self, front
        return: the dequeued element, None if empty
        """

        if self.is_empty():
            return None

        if front:
            removed_value = self.CDLL.head.val
            self.CDLL.remove()
        else:
            removed_value = self.CDLL.head.prev.val
            self.CDLL.remove(front=False)

        return removed_value


def plot_speed():
    """
    Compares performance of the CDLLCD and the standard array based deque
    """

    # First we'll test sequences of basic operations

    sizes = [100*i for i in range(0, 200, 5)]

    # (1) Grow large
    grow_avgs_array = []
    grow_avgs_CDLL = []

    for size in sizes:
        grow_avgs_array.append(0)
        grow_avgs_CDLL.append(0)
        data = list(range(size))
        for trial in range(3):

            gc.collect()  # What happens if you remove this? Hint: memory fragmention
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            # randomize data
            shuffle(data)

            start = default_timer()
            for item in data:
                cd_array.enqueue(item, item % 2)
            grow_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            for item in data:
                cd_DLL.enqueue(item, item % 2)
            grow_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(sizes, grow_avgs_array, color='blue', label='Array')
    plt.plot(sizes, grow_avgs_CDLL, color='red', label='CDLL')
    plt.title("Enqueue and Grow")
    plt.legend(loc='best')
    plt.show()

    # (2) Grow Large then Shrink to zero

    shrink_avgs_array = []
    shrink_avgs_CDLL = []

    for size in sizes:
        shrink_avgs_array.append(0)
        shrink_avgs_CDLL.append(0)
        data = list(range(size))

        for trial in range(3):

            gc.collect()
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            # randomize data
            shuffle(data)

            start = default_timer()
            for item in data:
                cd_array.enqueue(item, item % 2)
            for item in data:
                cd_array.dequeue(not item % 2)
            shrink_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            for item in data:
                cd_DLL.enqueue(item, item % 2)
            for item in data:
                cd_DLL.dequeue(not item % 2)
            shrink_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(sizes, shrink_avgs_array, color='blue', label='Array')
    plt.plot(sizes, shrink_avgs_CDLL, color='red', label='CDLL')
    plt.title("Enqueue, Grow, Dequeue, Shrink")
    plt.legend(loc='best')
    plt.show()

    # (3) Test with random operations

    random_avgs_array = []
    random_avgs_CDLL = []

    for size in sizes:
        random_avgs_array.append(0)
        random_avgs_CDLL.append(0)
        data = list(range(size))

        for trial in range(3):

            gc.collect()
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            shuffle(data)

            start = default_timer()
            for item in data:
                if randint(0, 3) <= 2:
                    cd_array.enqueue(item, item % 2)
                else:
                    cd_array.dequeue(item % 2)
            random_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            for item in data:
                if randint(0, 3) <= 2:
                    cd_DLL.enqueue(item, item % 2)
                else:
                    cd_DLL.dequeue(item % 2)
            random_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(sizes, random_avgs_array, color='blue', label='Array')
    plt.plot(sizes, random_avgs_CDLL, color='red', label='CDLL')
    plt.title("Operations in Random Order")
    plt.legend(loc='best')
    plt.show()

    def max_len_subarray(data, bound, structure):
        """
        returns the length of the largest subarray of `data` with sum less or eq to than `bound`
        :param data: list of integers to operate on
        :param bound: largest allowable sum
        :param structure: either a CircularDeque or a CDLLCD
        :return: the length
        """
        index, max_len, subarray_sum = 0, 0, 0
        while index < len(data):

            while subarray_sum <= bound and index < len(data):
                structure.enqueue(data[index])
                subarray_sum += data[index]
                index += 1
            max_len = max(max_len, subarray_sum)

            while subarray_sum > bound:
                subarray_sum -= structure.dequeue(False)

        return max_len

    # (4) A common application

    application_avgs_array = []
    application_avgs_CDLL = []

    data = [randint(0, 1) for i in range(5000)]
    window_lengths = list(range(0, 200, 5))

    for length in window_lengths:
        application_avgs_array.append(0)
        application_avgs_CDLL.append(0)

        for trial in range(3):

            gc.collect()
            cd_array = CircularDeque()
            cd_DLL = CDLLCD()

            start = default_timer()
            max_len_subarray(data, length, cd_array)
            application_avgs_array[-1] += (default_timer() - start)/3

            start = default_timer()
            max_len_subarray(data, length, cd_DLL)
            application_avgs_CDLL[-1] += (default_timer() - start)/3

    plt.plot(window_lengths, application_avgs_array,
             color='blue', label='Array')
    plt.plot(window_lengths, application_avgs_CDLL, color='red', label='CDLL')
    plt.title("Sliding Window Application")
    plt.legend(loc='best')
    plt.show()