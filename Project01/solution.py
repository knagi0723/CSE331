from typing import TypeVar  # For use in type hinting

# Type declarations
T = TypeVar('T')        # generic type
SLL = TypeVar('SLL')    # forward declared Singly Linked List type
Node = TypeVar('Node')  # forward declared Node type


class SLLNode:
    """
    Node implementation
    Do not modify
    """

    __slots__ = ['data', 'next']

    def __init__(self, data: T, next: Node = None) -> None:
        """
        Initialize an SLL Node
        :param data: data value held by the node
        :param next: reference to the next node in the SLL
        :return: None
        """
        self.data = data
        self.next = next

    def __str__(self) -> str:
        """
        Overloads `str()` method, casts SLL nodes to strings
        :return: string representation of node
        """
        return '(Node: ' + str(self.data) + ' )'

    def __repr__(self) -> str:
        """
        Overloads `repr()` method for use in debugging
        :return: string representation of node
        """
        return '(Node: ' + str(self.data) + ' )'

    def __eq__(self, other: Node) -> bool:
        """
        Overloads `==` operator to compare nodes
        :param other: right operand of `==`
        :return: True if the nodes are ==, else False
        """
        return self is other if other is not None else False


class SinglyLinkedList:
    """
    SLL implementation
    """

    __slot__ = ['head', 'tail']

    def __init__(self) -> None:
        """
        Initializes an SLL
        return: None
        DO NOT MODIFY THIS FUNCTION
        """
        self.head = None
        self.tail = None

    def __repr__(self) -> str:
        """
        Represents an SLL as a string
        DO NOT MODIFY THIS FUNCTION
        :return: string representation of SLL
        """
        return self.to_string()

    def __eq__(self, other: SLL) -> bool:
        """
        Overloads `==` operator to compare SLLs
        :param other: right operand of `==`
        :return: True if equal, else False
        DO NOT MODIFY THIS FUNCTION
        """
        comp = lambda n1, n2: n1 == n2 and (comp(n1.next, n2.next) if (n1 and n2) else True)
        return comp(self.head, other.head)

    # ========== Modify below ========== #

    def append(self, data: T) -> None:
        """
        Append an SLLNode to the end of the SLL
        :param data: data to append
        :return: None
        """
        new_node = SLLNode(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def to_string(self) -> str:
        """
        Converts an SLL to a string
        :return: string representation of SLL
        """
        string = ""
        if self.head == None:
            return "None"
        elif self.head == self.tail:
            return str(self.head.data)
        else:
            string += str(self.head.data)
            next = self.head.next
            while next != None:
                string += " --> " + str(next.data)
                next = next.next
            return string

    def length(self) -> int:
        """
        Determines number of nodes in the list
        :return: number of nodes in list
        """
        count = 0
        string = self.head
        while string != None:
            count += 1
            string = string.next
        return count

    def total(self) -> T:
        """
        Sums up the values in the list
        :return: total sum of values in the list
        """
        total = None
        string = self.head
        while string != None:
            if total == None:
                total = string.data
            else:
                total += string.data
            string = string.next
        return total


    def delete(self, data: T) -> bool:
        """
        Deletes the first node containing `data` from the SLL
        :param data: data to remove
        :return: True if a node was removed, else False
        """
        if self.head is None:
            return False

        if self.head.data == data:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            return True

        string = self.head
        while string.next != None and string.next.data != data:
            string = string.next

        if string.next == None:
            return False

        string.next = string.next.next

        if string.next == None:
            self.tail = string

        return True

    def delete_all(self, data: T) -> bool:
        """
        Deletes all instances of a node containing `data` from the SLL
        :param data: data to remove
        :return: True if a node was removed, else False
        """
        if self.head == None:
            return False

        delete = False

        while self.head != None and self.head.data == data:
            self.head = self.head.next
            delete = True

        if self.head == None:
            self.tail = None

        string = self.head
        prev = None

        while string != None:
            if string.data == data:
                if string == self.tail:
                    self.tail = prev
                prev.next = string.next
                string = string.next
                delete = True
            else:
                prev = string
                string = string.next

        return delete


    def find(self, data: T) -> bool:
        """
        Looks through the SLL for a node containing `data`
        :param data: data to search for
        :return: True if found, else False
        """
        string = self.head
        while string != None:
            if string.data == data:
                return True
            string = string.next
        return False


    def find_sum(self, data: T) -> int:
        """
        Returns the number of occurrences of `data` in this list
        :param data: data to find and sum up
        :return: number of times the data occurred
        """
        count = 0
        string = self.head
        while string != None:
            if string.data == data:
                count += 1
            string = string.next
        return count


def help_mario(roster: SLL, ally: str) -> bool:
    """
    Updates the roster of racers to put Mario's ally at the front
    Preserves relative order of racers around ally
    :param roster: initial order of racers
    :param ally: the racer that needs to go first
    :return: True if the roster was changed, else False
    """
    if roster.head == None:
        return False

    if roster.find(ally) == False:
        return False

    if roster.head.data == ally:
        return False

    head = roster.head
    while head == roster.head:
        if head.data != ally:
            roster.append(head.data)
            roster.delete(head.data)
            head = roster.head
        else:
            return True









