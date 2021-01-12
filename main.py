import os
import timeit


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


cwd = os.getcwd()


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
        if len(bits) > 8:
            bit_code = bits[i:i + 8]
            bit_code = chr(int(bit_code, 2))
            output += bit_code
            bits = bits[i + 8:]
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
    if padding > 0:
        bits = bits[:-padding]
    for bit in bits:
        code += bit
        if code in language_map:
            output += language_map[code]
            code = ""
    return output


def extract_header(char_count, buff):
    d = {}
    buff = str(buff, 'utf-8')
    for i in range(char_count):
        line, buff = buff.split("\n", 1)
        if not line:
            line, buff = buff.split("\n", 1)
            char = "\n"
            code_word = line.split(None, 1)[0]
        elif line[0] == " " or line[0] == "\r":
            char = line[0]
            code_word = line.split(None, 1)[0]
        else:
            char, code_word = line.split()
        d[code_word] = char
    padding, buff = buff.split("\n", 1)
    padding = int(padding)
    return d, padding, buff


def create_header(language_map, padding):
    output = ""
    output += str(len(language_map)) + "\n"
    header_size = len(bytes(output, 'utf-8'))
    for key in language_map.keys():
        output += key + " " + str(language_map[key]) + "\n"
    output += str(padding) + "\n"
    return output, header_size


def decompress(path):
    f = open(path, 'rb')
    n = str(f.readline(), 'utf-8')
    i = 0
    while n:
        name = str(f.readline(), 'utf-8').rstrip()
        try:
            n = int(n)
        except ValueError:
            break
        char_count = int(str(f.readline(), 'utf-8'))
        buff = f.read(n)
        language_map, padding, data = extract_header(char_count, buff)
        data = decode(data, language_map, padding)
        create_output(data, name + ".txt", mode=1)
        i += 1
        n = str(f.readline(), 'utf-8')


def compress(path, mode=0):
    if mode == 0:
        name = str(os.path.splitext(path)[0])
        name = name + '\n'
        data = str(read_file(path), 'utf-8')
        freq_map = frequency_map(data)
        language_map = huffman_coding(freq_map)
        compressed_data, padding = encode(data, language_map)
        header, header_size = create_header(language_map, padding)
        output = name + header + compressed_data
        header_size += len(bytes(name, 'UTF-8'))
        output = bytes(output, 'UTF-8')
        output = b"".join([bytes(str(len(output) - header_size) + "\n", 'utf-8'), output])
        size = create_output(output, path, 0)
    elif mode == 1:
        os.chdir(path)
        first = True
        for file in os.listdir(path):
            if file.endswith(".txt"):
                name = str(os.path.splitext(file)[0])
                name = name + '\n'
                data = str(read_file(file), 'utf-8')
                freq_map = frequency_map(data)
                language_map = huffman_coding(freq_map)
                compressed_data, padding = encode(data, language_map)
                header, header_size = create_header(language_map, padding)
                output = name + header + compressed_data
                header_size += len(bytes(name, 'UTF-8'))
                output = bytes(output, 'UTF-8')
                output = b"".join([bytes(str(len(output) - header_size) + "\n", 'utf-8'), output])
                os.chdir('..')
                size = create_output(output, "Compressed.bin", 0, first)
                os.chdir(path)
                first = False
        os.chdir(cwd)
    return size


def read_file(path):
    f = open(path, 'rb')
    return f.read()


def create_output(data, path, mode=0, first=True):
    extension = os.path.splitext(path)[1]
    name = str(os.path.splitext(path)[0])
    if mode == 0:
        try:
            if first:
                output_path = open(name + extension, "wb")
            else:
                output_path = open(name + extension, "ab")
            output_path.write(data)
            print("Success, data saved at: " + name + extension)
            return os.stat(name + extension).st_size
        except IOError:
            print("Something went wrong")
            exit(-1)
    else:
        try:
            output_path = open(name + extension, "w", encoding='utf-8', newline='\n')
            output_path.write(data)
            print("Success, data saved at: " + name + extension)
            return os.stat(name + extension).st_size
        except IOError:
            print("Something went wrong")
            exit(-1)


if __name__ == '__main__':
    run = True
    print("Enter operation type:")

    while run:
        original_size = 0
        new_size = 0
        # GET OPERATION FROM USER
        op = int(input("Compression of a File (0) | Compression of a Folder (1) | Decompression (2) "))
        if op == 0:  # COMPRESSION OF A FILE
            p = str(input("Enter a file name in the current directory "))
            file_stats = os.stat(p)
            original_size = file_stats.st_size
            start = timeit.timeit()
            new_size = compress(p, op)
            end = timeit.timeit()
        elif op == 1:  # COMPRESSION OF A FOLDER
            p = str(input("Enter path to the directory "))
            for f_d in os.listdir(p):
                if f_d.endswith(".txt"):
                    original_size += os.stat(f_d).st_size
            start = timeit.timeit()
            new_size = compress(p, op)
            end = timeit.timeit()
        elif op == 2:  # DECOMPRESSION
            p = str(input("Enter a file name in the current directory "))
            start = timeit.timeit()
            decompress(p)
            end = timeit.timeit()
        else:
            print("Enter a valid operation type")
            continue
        print("Execution time of the program is ", str(abs(round(end - start, 5))) + " seconds")
        if op != 2:
            print("Compression rate is ", str((new_size / original_size) * 100) + " %")
