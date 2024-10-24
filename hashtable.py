class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self):
        self.size = 2
        self.table = [None] * self.size

    def _hash(self, key):
        return hash(key) % self.size

    def put(self, key, value):
        index = self._hash(key)
        if self.table[index] is None:
            self.table[index] = Node(key, value)
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    current.next = Node(key, value)
                    return
                current = current.next

    def get(self, key):
        index = self._hash(key)
        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def remove(self, key):
        index = self._hash(key)
        current = self.table[index]
        prev = None

        while current:
            if current.key == key:
                if prev is None:
                    self.table[index] = current.next
                else:
                    prev.next = current.next
                return
            prev = current
            current = current.next

    def __str__(self):
        result = ""
        for i, node in enumerate(self.table):
            result += f"{i}: "
            while node:
                result += f"({node.key}, {node.value}) -> "
                node = node.next
            result += "None\n"
        return result
