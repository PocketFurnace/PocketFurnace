
class Node:

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:

    def __init__(self):
        self.head = None

    def push(self, new_data):

        new_node = Node(new_data)
        new_node.next = self.head

        if self.head is not None:
            self.head.prev = new_node
        self.head = new_node

    @staticmethod
    def insert_after(prev_node, new_data):

        if prev_node is None:
            return

        new_node = Node(new_data)
        new_node.next = prev_node.next
        prev_node.next = new_node
        new_node.prev = prev_node
        if new_node.next is not None:
            new_node.next.prev = new_node

    def append(self, new_data):

        new_node = Node(new_data)
        new_node.next = None
        if self.head is None:
            new_node.prev = None
            self.head = new_node
            return

        last = self.head
        while last.next is not None:
            last = last.next

        last.next = new_node
        new_node.prev = last

        return

    @staticmethod
    def print_list(node):
        while node is not None:
            last = node
            node = node.next

        # noinspection PyUnboundLocalVariable
        while last is not None:
            last = last.prev
