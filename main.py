import os
import time


class Node:  # HEAP NODE CLASS
    def __init__(self, value, char=None, left=None, right=None):
        self.value = value
        self.char = char
        self.left = left
        self.right = right

    def get_children(self):
        return self.left, self.right

    def get_value(self):
        return self.value

    def get_char(self):
        return self.char


def frequency_map(data):  # FREQUENCY MAP GENERATOR
    frequency = {}
    for character in data:
        if character not in frequency:
            frequency[character] = 1
        else:
            frequency[character] += 1
    return frequency


def huffman_coding(freq_map):
    freq_map = sorted(freq_map.items(), key=lambda x: x[1])
    nodes = []
    for key, value in freq_map:
        node = Node(value, key)
        nodes.append(node)
    while len(nodes) > 1:
        node1 = nodes[0]
        node2 = nodes[1]
        nodes = nodes[2:]
        sum_node = node1.get_value() + node2.get_value()
        node = Node(sum_node, left=node1, right=node2)
        i = 0
        while i < len(nodes) and node.get_value() > nodes[i].get_value():
            i += 1
        nodes[i:i] = [node]
    d = assign_code(nodes[0], '')
    return d


def assign_code(node, code):
    if not node.left and not node.right:
        return {node.get_char(): code}
    d = dict()
    d.update(assign_code(node.left, code + '0'))
    d.update(assign_code(node.right, code + '1'))
    return d


def encode(data, language_map):
    output = ""
    bits = ""
    i = 0
    padding = 0
    for char in data:
        bits += language_map[char]
    while len(bits) > 0:
        bit_code = bits[i:i + 8]
        while len(bit_code) < 8:
            bit_code = bit_code + '0'
            padding += 1
        bit_code = chr(int(bit_code, 2))
        output += bit_code
        bits = bits[i + 8:]
    return output, padding


def decode(data, language_map, padding):
    output = ""
    bits = ""
    code = ""
    for c in data:
        c = ord(c)
        c = f'{c:08b}'
        bits += c
    bits = bits[:-padding]
    for bit in bits:
        code += bit
        if code in language_map:
            output += language_map[code]
            code = ""
    return output


def extract_header(char_count, buff):
    d = {}
    for i in range(char_count):
        if buff[0] == '\n':  # CHECK IF NEXT CHAR IS NEW LINE CHAR
            empty, line, buff = buff.split("\n", 2)  # REMOVE TWO LINES
            char = "\n"
            code_word = line.split()[0]  # REMOVE ANY EMPTY SPACES WITH THE CODE WORD
        else:
            line, buff = buff.split("\n", 1)
            line = line.split()
            if len(line) == 1:  # CHECK IF NEXT CHAR IS EMPTY SPACE
                char = " "
                code_word = line[0]
            else:
                char = line[0]
                code_word = line[1]
        d[code_word] = char
    padding, buff = buff.split("\n", 1)
    padding = int(padding)
    return d, padding, buff


def create_header(language_map, padding):
    output = ""
    output += str(len(language_map)) + "\n"
    for key in language_map.keys():
        output += key + " " + str(language_map[key]) + "\n"
    output += str(padding) + "\n"
    return output


def decompress(char_count, buff):
    language_map, padding, data = extract_header(char_count, buff)
    return decode(data, language_map, padding)


def compress(data):
    freq_map = frequency_map(data)
    language_map = huffman_coding(freq_map)
    compressed_data, padding = encode(data, language_map)
    header = create_header(language_map, padding)
    output = header + compressed_data
    return output


def get_file():
    name = input("Enter file name ")
    while True:
        try:
            file = open(name, 'r', encoding='utf-8')
            break
        except IOError:
            name = input("Enter a valid file name ")
    return name, file


def create_output(data, name, extension):
    try:
        output_path = open(name + extension, "w", encoding='utf-8')
        output_path.write(data)
        print("Success, data saved at: " + name + extension)
        return os.stat(name + extension).st_size
    except IOError:
        print("Something went wrong")
        exit(-1)


if __name__ == '__main__':
    run = True
    start = 0
    end = 0

    while run:
        # GET FILE NAME
        file_data = ""
        filename, f = get_file()
        file_stats = os.stat(filename)
        filename, file_extension = os.path.splitext(filename)
        original_size = file_stats.st_size

        # GET OPERATION TYPE ( COMPRESSION or DECOMPRESSION )
        while True:
            op_type = int(input("Enter the mode (0 for Compression | 1 for Decompression) "))
            if op_type == 0:
                file_data = f.read()

                # GET COMPRESSED FILE TYPE
                file_extension = int(input("Enter the compression file type (0 for .txt | 1 for .bin) "))

                if file_extension == 0:
                    file_extension = ".txt"
                else:
                    file_extension = ".bin"

                start = time.time()
                file_data = compress(file_data)
                end = time.time()
                break

            elif op_type == 1:
                n = f.readline()
                file_data = f.read()

                try:
                    n = int(n)
                except TypeError:
                    print("Invalid file structure")
                    exit(-1)

                start = time.time()
                file_data = decompress(n, file_data)
                end = time.time()
                file_extension = ".txt"
                break
            else:
                print("Please enter a valid number")
                continue

        new_size = create_output(file_data, filename, file_extension)
        if op_type == 0:
            percentage = format(new_size / original_size * 100, ".2f")
            print(f"Compression percentage is {percentage}%")
        total = format((end - start) * 1000, ".2f")
        print(f"The execution time of the program is {total}ms")
        x = int(input("Do you want to compress or decompress more files? (0 for NO | 1 for YES) "))
        run = (x == 1)
