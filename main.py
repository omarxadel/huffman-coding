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


def frequency_map(data):    # FREQUENCY MAP GENERATOR
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


def cipher(data, language_map):
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


def decipher(data, language_map, padding):
    # output_path = open ("decompressed_file.txt" , "w")
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
    # output_path.write(output)
    return output


def extract_header(char_count, buff):
    d = {}
    for i in range(char_count):
        line, buff = buff.split("\n", 1)
        char, code_word = line.split(" ")
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
    return decipher(data, language_map, padding)


def compress(data):
    output_path = open("compressed_file.bin", "w")
    freq_map = frequency_map(data)
    language_map = huffman_coding(freq_map)
    compressed_data, padding = cipher(data, language_map)
    header = create_header(language_map, padding)
    output = header + compressed_data
    output_path.write(output)
    print("Compressed")
    return compressed_data, header


def get_file():
    name = input("Enter file name ")
    while True:
        try:
            f = open(name, 'r', encoding="utf8")
            break
        except IOError:
            name = input("Enter a valid file name ")
    return name


if __name__ == '__main__':
    # GET FILE NAME
    filename = get_file()
    file_stats = os.stat(filename)
    filename, file_extension = os.path.splitext(filename)

    # GET OPERATION TYPE ( COMPRESSION or DECOMPRESSION )
    while True:
        op_type = int(input("Enter the mode (0 for Compression | 1 for Decompression) "))
        start = time.time()
        if op_type == 0:
            file_data = f.read()
            # print(f'Original file Size in Bytes is {file_stats.st_size}')
            compress(file_data)
            break
        elif op_type == 1:
            n = f.readline()
            file_data = f.read()
            try:
                n = int(n)
            except TypeError:
                print("Invalid file structure")
                exit(-1)
            decompress(n, file_data)
            break
        else:
            print("Please enter a valid number")
            continue

    end = time.time()
    total = str(round((end - start) * 1000, 2))
    print(f"The execution time of the program is {total}ms")
