from hashtable import HashTable


class SymbolTableIdentifiers:
    def __init__(self):
        self.symbol_table = HashTable()

    def add_identifier(self, identifier, value):
        self.symbol_table.put(identifier, value)

    def get_identifier_value(self, identifier):
        return self.symbol_table.get(identifier)

    def remove_identifier(self, identifier):
        self.symbol_table.remove(identifier)


class SymbolTableConstants:
    def __init__(self):
        self.symbol_table = HashTable()

    def add_constant(self, identifier, value):
        self.symbol_table.put(identifier, value)

    def get_constant_value(self, identifier):
        return self.symbol_table.get(identifier)

    def remove_constant(self, identifier):
        self.symbol_table.remove(identifier)

