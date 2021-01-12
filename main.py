import os
import timeit
import array


class Node:  # HEAP NODE CLASS
    def __init__(self, value=None, char=None, left=None, right=None):
        self.value = value
        self.char = char
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None

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
    compressed_tree = encode_tree(nodes[0], "")
    d = assign_code(nodes[0], '')
    return d, compressed_tree


def encode_tree(node, code):
    if node.is_leaf():
        code += "1"
        code += f"{ord(node.get_char()):08b}"
    else:
        code += "0"
        code = encode_tree(node.left, code)
        code = encode_tree(node.right, code)
    return code


def decode_tree(data):
    char = data[0]
    del data[0]

    if char == "1":
        byte = ""
        for _ in range(8):
            byte += data[0]
            del data[0]

        return Node(char=int(byte, 2))
    else:
        left = decode_tree(data)
        right = decode_tree(data)

        return Node(None, left=left, right=right)


def assign_code(node, code=''):
    if not node.left and not node.right:
        return {node.get_char(): code}
    d = dict()
    d.update(assign_code(node.left, code + '0'))
    d.update(assign_code(node.right, code + '1'))
    return d


def encode(data, language_map, compressed_header, mode=0):
    compressed_header = str(mode) + compressed_header
    output = ""
    bits = ""
    for char in data:
        bits += language_map[char]
    num = 8 - (len(bits) + len(compressed_header)) % 8
    if num != 0:
        output = num * "0" + bits
    output = f"{compressed_header}{num:08b}{output}"
    return output


def decode(data, language_map):
    code = ""
    output = []
    for bit in data:
        code += bit
        if code in language_map:
            output.append(language_map[code])
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
    data = ""

    # Read the file byte by byte
    byte = f.read(1)
    while len(byte) > 0:
        data += f"{bin(ord(byte))[2:]:0>8}"
        byte = f.read(1)
    data = list(data)
    mode = int(data[0])
    del data[0]
    node = decode_tree(data)
    d = assign_code(node)
    reversed_tree = {v: k for k, v in d.items()}
    n_padding = data[:8]
    n_padding = int("".join(n_padding), 2)
    data = data[8:]
    data = data[n_padding:]
    data = decode(data, reversed_tree)
    if mode == 0:
        output = ""
        for num in data:
            output += format(num, '08b')

        b_arr = bytearray()

        for i in range(0, len(output), 8):
            b_arr.append(int(output[i:i + 8], 2))

        create_output(str(b_arr, 'utf-8'), path, mode=1)
    else:
        op_files = array.array('B', data).tobytes().split(b'\x11\x22\x33')
        for i, file in enumerate(op_files[0:len(op_files) - 1]):
            create_output(str(op_files[i][:len(op_files[i])], 'utf-8'), 'decompressed' + str(i) + '.txt', mode=1)


def compress(path, mode=0):
    if mode == 0:
        data = str(read_file(path), 'utf-8')
        freq_map = frequency_map(data)
        language_map, compressed_header = huffman_coding(freq_map)
        output = encode(data, language_map, compressed_header, mode=mode)
        output = bytes(output, 'UTF-8')
        size = create_output(output, path, 0)
    elif mode == 1:
        os.chdir(path)
        data = bytes()
        for file in os.listdir(path):
            if file.endswith(".txt"):
                data += read_file(file) + b'\x11\x22\x33'
        data = str(data, 'utf-8')
        freq_map = frequency_map(data)
        language_map, compressed_header = huffman_coding(freq_map)
        output = encode(data, language_map, compressed_header, mode=mode)
        output = bytes(output, 'UTF-8')
        os.chdir('..')
        size = create_output(output, "Compressed.bin", 0)
        os.chdir(path)
        os.chdir(cwd)
    return size


def read_file(path):
    f = open(path, 'rb')
    return f.read()


def create_output(data, path, mode=0, first=True):
    extension = os.path.splitext(path)[1]
    name = str(os.path.splitext(path)[0])
    if mode == 0:
        b_arr = bytearray()
        for i in range(0, len(data), 8):
            b_arr.append(int(data[i:i + 8], 2))
        try:
            if first:
                output_path = open(name + extension, "wb")
            else:
                output_path = open(name + extension, "ab")
            output_path.write(b_arr)
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
            os.chdir(p)
            for f_d in os.listdir(p):
                if f_d.endswith(".txt"):
                    original_size += os.stat(f_d).st_size
            os.chdir(cwd)
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
