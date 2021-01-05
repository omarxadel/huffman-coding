class Node:
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


def frequency_map(data):
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


def translate(data, language_map):
    # TODO: TRANSLATE THE INPUT DATA INTO THE CORRESPONDING CODE IN MAP
    return ""


def decompress():
    print("Decompression Selected")


def compress(data):
    # TODO: UNCOMMENT THE FOLLOWING WHEN READY
    freq_map = frequency_map(data)
    language_map = huffman_coding(freq_map)
    # compressed_data = translate(data, language_map)
    # return language_map, compressed_data


if __name__ == '__main__':
    # GET FILE NAME
    filename = input("Enter file name ")
    while True:
        try:
            f = open(filename, 'r', encoding="utf8")
            break
        except IOError:
            filename = input("Enter a valid file name ")

    # EXTRACT FILE DATA INTO A VARIABLE
    file_data = f.read()

    # GET OPERATION TYPE ( COMPRESSION or DECOMPRESSION )
    while True:
        op_type = int(input("Enter the mode (0 for Compression | 1 for Decompression) "))
        if op_type == 0:
            compress(file_data)
            break
        elif op_type == 1:
            decompress()
            break
        else:
            print("Please enter a valid number")
            continue
