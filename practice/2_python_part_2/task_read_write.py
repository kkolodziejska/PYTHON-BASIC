"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""
import os


def main():
    directory = 'files'
    values = []
    filenames = os.listdir(directory)
    filenames.sort(key=lambda item: (len(item), item))

    for filename in filenames:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            value = f.read()
            values.append(value)

    with open('result.txt', 'w') as f:
        f.write(', '.join(values))


if __name__ == '__main__':
    main()
