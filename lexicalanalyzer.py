import re
from typing import List, Tuple
from symboltables import SymbolTableIdentifiers, SymbolTableConstants


class LexicalAnalyzer:
    """
    A class to perform lexical analysis on a given source code.
    """

    def __init__(self):
        """
        Initializes the LexicalAnalyzer with symbol tables for identifiers and constants,
        and sets up the reserved words, operators, and separators.
        """
        self.identifier_st = SymbolTableIdentifiers()
        self.constant_st = SymbolTableConstants()

        self.pif: List[Tuple[str, int]] = []

        self.id_counter = 0
        self.const_counter = 0

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

        self.identifier_regex = re.compile(r'^[a-zA-Z][a-zA-Z0-9]*$')
        self.integer_regex = re.compile(r'^0$|^[+-]?[1-9][0-9]*$')
        self.string_regex = re.compile(r'^"[a-zA-Z0-9 ]*"$')

    def tokenize(self, line: str) -> List[str]:
        """
        Tokenizes a given line of code into a list of tokens.

        Args:
            line (str): A line of source code.

        Returns:
            List[str]: A list of tokens extracted from the line.
        """
        string_tokens = []
        string_pattern = r'"[^"]*"'
        strings = re.finditer(string_pattern, line)
        for i, match in enumerate(strings):
            placeholder = f"STRING_{i}"
            string_tokens.append((placeholder, match.group()))
            line = line.replace(match.group(), placeholder)

        for symbol in sorted(self.separators, key=len, reverse=True):
            line = line.replace(symbol, f" {symbol} ")

        tokens = [token.strip() for token in line.split() if token.strip()]

        for placeholder, original in string_tokens:
            tokens = [original if t == placeholder else t for t in tokens]

        return tokens

    def is_identifier(self, token: str) -> bool:
        """
        Checks if a token is a valid identifier.

        Args:
            token (str): The token to check.

        Returns:
            bool: True if the token is a valid identifier, False otherwise.
        """
        if token.lower() in self.reserved_words:
            return False
        return bool(self.identifier_regex.match(token))

    def is_constant(self, token: str) -> bool:
        """
        Checks if a token is a valid constant (integer or string).

        Args:
            token (str): The token to check.

        Returns:
            bool: True if the token is a valid constant, False otherwise.
        """
        return bool(self.integer_regex.match(token) or self.string_regex.match(token))

    def analyze(self, code: str) -> Tuple[List[Tuple[str, int]], str]:
        """
        Analyzes the given source code and generates the Program Internal Form (PIF)
        and a result message indicating lexical correctness or errors.

        Args:
            code (str): The source code to analyze.

        Returns:
            A tuple containing the PIF and a result message.
        """
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
                if token.lower() in self.reserved_words:
                    self.pif.append((token.lower(), -1))
                elif token in self.operators:
                    self.pif.append((token, -1))
                elif token in self.separators:
                    self.pif.append((token, -1))
                elif self.is_identifier(token):
                    if self.identifier_st.get_identifier_value(token) is None:
                        self.identifier_st.add_identifier(token, self.id_counter)
                        self.id_counter += 1
                    pos = self.identifier_st.get_identifier_value(token)
                    self.pif.append(("identifier", pos))
                elif self.is_constant(token):
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
    """
    Analyzes a given program text and writes the Program Internal Form (PIF)
    and Symbol Tables to output files.

    Args:
        program_text (str): The source code of the program to analyze.
    """
    analyzer = LexicalAnalyzer()
    pif, result = analyzer.analyze(program_text)

    if result != "Lexically correct":
        print(result)
        return

    with open('PIF.out', 'w') as pif_file:
        print("\nProgram Internal Form (PIF):")
        pif_file.write("Program Internal Form (PIF):\n")
        for token, value in pif:
            print(f"({token}, {value})")
            pif_file.write(f"({token}, {value})\n")

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
