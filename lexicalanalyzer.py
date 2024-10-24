import re
from typing import List, Tuple
from symboltables import SymbolTableIdentifiers, SymbolTableConstants


class LexicalAnalyzer:
    def __init__(self):
        # Initialize symbol tables using the provided implementation
        self.identifier_st = SymbolTableIdentifiers()
        self.constant_st = SymbolTableConstants()

        # Initialize PIF to store tokens and their positions
        self.pif: List[Tuple[str, int]] = []

        # Counter for symbol table positions
        self.id_counter = 0
        self.const_counter = 0

        # Define language specifications as per Lab1b.pdf
        self.reserved_words = {
            'int', 'string', 'array', 'for', 'if', 'else',
            'while', 'input', 'print', 'let', 'return'
        }

        self.operators = {
            '+', '-', '*', '/', '%',
            '=', '<', '<=', '==', '=>', '>'
        }

        self.separators = {
            '(', ')', '[', ']', '{', '}', '?', ',', ';'
        }

        # Regular expressions based on Lab1b specifications
        self.identifier_regex = re.compile(r'^[a-zA-Z][a-zA-Z0-9]*$')
        # Integer constant regex as per specification
        self.integer_regex = re.compile(r'^0$|^[+-]?[1-9][0-9]*$')
        # String constant regex as per specification
        self.string_regex = re.compile(r'^"[a-zA-Z0-9 ]*"$')

    def tokenize(self, line: str) -> List[str]:
        """Split a line into tokens while preserving string literals"""
        # Handle string literals first
        string_tokens = []
        string_pattern = r'"[^"]*"'
        strings = re.finditer(string_pattern, line)
        for i, match in enumerate(strings):
            placeholder = f"STRING_{i}"
            string_tokens.append((placeholder, match.group()))
            line = line.replace(match.group(), placeholder)

        # Add spaces around operators and separators
        for symbol in sorted(self.separators, key=len, reverse=True):
            line = line.replace(symbol, f" {symbol} ")

        # Split by whitespace and filter empty tokens
        tokens = [token.strip() for token in line.split() if token.strip()]

        # Restore string literals
        for placeholder, original in string_tokens:
            tokens = [original if t == placeholder else t for t in tokens]

        return tokens

    def is_identifier(self, token: str) -> bool:
        """Check if token is a valid identifier per Lab1b specifications"""
        if token.lower() in self.reserved_words:
            return False
        return bool(self.identifier_regex.match(token))

    def is_constant(self, token: str) -> bool:
        """Check if token is a valid constant per Lab1b specifications"""
        return bool(self.integer_regex.match(token) or self.string_regex.match(token))

    def analyze(self, code: str) -> Tuple[List[Tuple[str, int]], str]:
        """Analyze source code and return PIF and result message"""
        self.pif = []
        line_number = 0
        errors = []

        for line in code.split('\n'):
            line_number += 1
            line = line.strip()
            if not line:
                continue

            tokens = self.tokenize(line)

            for token in tokens:
                # Check reserved words first (case-insensitive)
                if token.lower() in self.reserved_words:
                    self.pif.append((token.lower(), -1))
                # Check operators
                elif token in self.operators:
                    self.pif.append((token, -1))
                # Check separators
                elif token in self.separators:
                    self.pif.append((token, -1))
                # Check identifiers
                elif self.is_identifier(token):
                    # Add to identifier symbol table if not present
                    if self.identifier_st.get_identifier_value(token) is None:
                        self.identifier_st.add_identifier(token, self.id_counter)
                        self.id_counter += 1
                    pos = self.identifier_st.get_identifier_value(token)
                    self.pif.append(("identifier", pos))
                # Check constants
                elif self.is_constant(token):
                    # Add to constant symbol table if not present
                    if self.constant_st.get_constant_value(token) is None:
                        self.constant_st.add_constant(token, self.const_counter)
                        self.const_counter += 1
                    pos = self.constant_st.get_constant_value(token)
                    self.pif.append(("constant", pos))
                else:
                    errors.append(f"Lexical error at line {line_number}: Invalid token '{token}'")

        if errors:
            return self.pif, "\n".join(errors)
        return self.pif, "Lexically correct"


def analyze_program(program_text: str):
    """Helper function to analyze a program and print results"""
    analyzer = LexicalAnalyzer()
    pif, result = analyzer.analyze(program_text)

    # Write PIF to PIF.out
    with open('PIF.out', 'w') as pif_file:
        print("\nProgram Internal Form (PIF):")
        pif_file.write("Program Internal Form (PIF):\n")
        for token, value in pif:
            print(f"({token}, {value})")
            pif_file.write(f"({token}, {value})\n")

    # Write SymbolTables to ST.out
    with open('ST.out', 'w') as st_file:
        st_file.write("Symbol Table Identifiers:\n")
        st_file.write("Data Structure: HashTable\n")
        st_file.write(str(analyzer.identifier_st.symbol_table))

        st_file.write("\nSymbol Table Constants:\n")
        st_file.write("Data Structure: HashTable\n")
        st_file.write(str(analyzer.constant_st.symbol_table))

        print("Symbol Table Identifiers:")
        print("Data Structure: HashTable")
        print(str(analyzer.identifier_st.symbol_table))

        print("\nSymbol Table Constants:")
        print("Data Structure: HashTable")
        print(str(analyzer.constant_st.symbol_table))

    print("\nAnalysis Result:")
    print(result)


# Test function
def main():
    test_files = ['p1.txt', 'p2.txt', 'p3.txt', 'p1err.txt']
    for file_name in test_files:
        print(f"\nAnalyzing {file_name}:")
        try:
            with open(file_name, 'r') as file:
                code = file.read()
            analyze_program(code)
        except FileNotFoundError:
            print(f"File {file_name} not found")


if __name__ == "__main__":
    main()
