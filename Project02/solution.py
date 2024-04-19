"""
Project 2
CSE 331 F23 (Onsay)
Authored By: Hank Murdock
Originally Authored By: Andrew McDonald & Alex Woodring & Andrew Haas & Matt Kight & Lukas Richters & Sai Ramesh
solution.py
"""

from typing import TypeVar, List

# for more information on type hinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")  # represents generic type
Node = TypeVar("Node")  # represents a Node object (forward-declare to use in Node __init__)


# pro tip: PyCharm auto-renders docstrings (the multiline strings under each function definition)
# in its "Documentation" view when written in the format we use here. Open the "Documentation"
# view to quickly see what a function does by placing your cursor on it and using CTRL + Q.
# https://www.jetbrains.com/help/pycharm/documentation-tool-window.html


class Node:
    """
    Implementation of a doubly linked list node.
    Do not modify.
    """
    __slots__ = ["value", "next", "prev", "child"]

    def __init__(self, value: T, next: Node = None, prev: Node = None, child: Node = None) -> None:
        """
        Construct a doubly linked list node.

        :param value: value held by the Node.
        :param next: reference to the next Node in the linked list.
        :param prev: reference to the previous Node in the linked list.
        :return: None.
        """
        self.next = next
        self.prev = prev
        self.value = value

        # The child attribute is only used for the application problem
        self.child = child

    def __repr__(self) -> str:
        """
        Represents the Node as a string.

        :return: string representation of the Node.
        """
        return f"Node({str(self.value)})"

    __str__ = __repr__


class DLL:
    """
    Implementation of a doubly linked list without padding nodes.
    Modify only below indicated line.
    """
    __slots__ = ["head", "tail", "size"]

    def __init__(self) -> None:
        """
        Construct an empty doubly linked list.

        :return: None.
        """
        self.head = self.tail = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        """
        result = []
        node = self.head
        while node is not None:
            result.append(str(node))
            node = node.next
        return " <-> ".join(result)

    def __str__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        """
        return repr(self)

    # MODIFY BELOW #

    def empty(self) -> bool:
        """
        Check if doubly linked list is empty.
        Return True if it is empty
        Return False if otherwise
        """
        return self.head is None

    def push(self, val, back=True) -> None:
        """
        Adds node to doubly linked list and updates size
        """
        new = Node(val)  # Create a new Node with the given value

        if self.empty():  # Check if the list is empty
            self.head = self.tail = new  # Set both head and tail to the new Node
        elif back:
            # Add the new Node to the back of the list
            self.tail.next = new
            new.prev = self.tail
            self.tail = new
        else:
            # Add the new Node to the front of the list
            new.next = self.head
            self.head.prev = new
            self.head = new

        self.size += 1  # Increase the size of the list

    def pop(self, back=True) -> None:
        """
        Removes node from the doubly linked list and update size
        The node can be removed from the back or front
        """
        if self.empty():
            return

        if back:
            # Remove the Node from the back of the list
            remove = self.tail
            if self.head == self.tail:
                self.head = self.tail = None
            else:
                self.tail = self.tail.prev
                self.tail.next = None
        else:
            # Remove the Node from the front of the list
            remove = self.head
            if self.head == self.tail:
                self.head = self.tail = None
            else:
                self.head = self.head.next
                self.head.prev = None

        del remove  # Delete the removed Node

        self.size -= 1  # Decrease the size of the list

    def list_to_dll(self, source):
        """
        Creates doubly linked list from Python list
        """
        self.head = self.tail = None  # Initialize the list as empty
        self.size = 0

        for item in source:
            new = Node(item)  # Create a new Node for each item in the source list
            if self.head is None:
                self.head = self.tail = new  # If the list is empty, set both head and tail to the new Node
            else:
                new.prev = self.tail
                self.tail.next = new
                self.tail = new
            self.size += 1  # Increase the size of the list for each item

    def dll_to_list(self):
        """
        Creates Python list from a doubly linked list
        """
        result = []
        node = self.head

        while node is not None:
            result.append(node.value)  # Append the value of each Node to the result list
            node = node.next  # Move to the next Node in the list

        return result

    def _find_nodes(self, val, find_first=False):
        """
        Create a list of Node with value val in the DLL and returns the associated Node object list
        """
        result = []

        node = self.head

        while node is not None:
            if node.value == val:
                result.append(node)  # Append Nodes with the specified value to the result list
                if find_first:
                    break
            node = node.next

        return result

    def find(self, val):
        """
        Construct list of Node with value val in the DLL and returns the associated Node object list
        """
        node = self.head

        while node is not None:
            if node.value == val:
                return node  # Return the first Node with the specified value
            node = node.next

        return None

    def find_all(self, val):
        """
        Finds all Node objects with value val in the DLL and returns a standard Python list of the associated Node objects
        """
        result = []
        node = self.head

        while node is not None:
            if node.value == val:
                result.append(node)  # Append all Nodes with the specified value to the result list
            node = node.next

        return result

    def _remove_node(self, to_remove):
        """
        Given a reference to a node in the linked list, remove it
        """
        if to_remove is None:
            return

        prev = to_remove.prev
        next = to_remove.next

        if prev is not None:
            prev.next = next
        else:
            self.head = next

        if next is not None:
            next.prev = prev
        else:
            self.tail = prev

        self.size -= 1  # Decrease the size of the list

    def remove(self, val):
        """
        Removes first with value val in the DLL
        """
        remove = self.find(val)  # Find the first Node with the specified value

        if remove is None:
            return False

        self._remove_node(remove)  # Remove the found Node
        return True

    def remove_all(self, val):
        """
        Remove all Node object with value val in the DLL
        """
        remove = self.find_all(val)  # Find all Nodes with the specified value
        count = len(remove)  # Count the number of Nodes to be removed

        for node in remove:
            self._remove_node(node)  # Remove each found Node

        return count if remove else 0

    def reverse(self):
        """
        Reverses the DLL in-place by modifying all next and prev references of Node objects in DLL
        """
        if self.head is None or self.head == self.tail:
            return

        curr = self.head
        tail_new = self.head

        while curr is not None:
            temp = curr.next
            curr.next = curr.prev
            curr.prev = temp

            curr = temp

        self.head = self.tail
        self.tail = tail_new

class BrowserHistory:

    def __init__(self, homepage: str):
        """
        Initializes BrowserHistory object.
        """
        self.dll = DLL()
        self.dll.push(homepage)
        self.current = self.dll.head

    def visit(self, url: str) -> None:
        """
        Visits a new URL and updates the browsing history.
        """
        self.dll.push(url)
        self.current = self.dll.tail

    def get_current_url(self) -> str:
        """
        Returns the current URL.
        """
        return self.current.value

    def backward(self) -> None:
        """
        Moves backward in the browsing history, skipping bad URLs.
        """
        while self.current.prev != None and metrics_api(self.current.prev.value):
            self.dll.pop(False)  # Remove bad URLs forward of the current page
            self.current = self.current.prev

        if self.current.prev != None:
            self.current = self.current.prev

    def forward(self) -> None:
        """
        Moves forward in the browsing history, skipping bad URLs.
        """
        while self.current.next != None and metrics_api(self.current.next.value):
            self.dll.pop()  # Remove bad URLs ahead of the current page
            self.current = self.current.next

        if self.current.next != None:
            self.current = self.current.next



# DO NOT MODIFY
intervention_set = set(['https://malicious.com', 'https://phishing.com', 'https://malware.com'])
def metrics_api(url: str) -> bool:
    """
    Uses the intervention_set to determine what URLs are bad and which are good.

    :param url: The url to check.
    :returns: True if this is a malicious website, False otherwise.
    """
    if url in intervention_set:
        return True
    return False