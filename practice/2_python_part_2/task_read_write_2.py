"""
Use function 'generate_words' to generate random words.
Write them to a new file encoded in UTF-8. Separator - '\n'.
Write second file encoded in CP1252, reverse words order. Separator - ','.

Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""


def generate_words(n=20):
    import string
    import random

    words = list()
    for _ in range(n):
        word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)

    return words


def read_write_2(filename_1: str = "file1.txt",
                 filename_2: str = "file2.txt",
                 number_of_words: int = 3) -> None:
    random_words = generate_words(number_of_words)

    with open(filename_1, 'w', encoding='utf-8') as f:
        print(*random_words, sep='\n', end='', file=f)

    with open(filename_2, 'w', encoding='cp1252') as f:
        print(*reversed(random_words), sep=',', end='', file=f)


if __name__ == '__main__':
    read_write_2()
