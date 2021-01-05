def frequency_map(data):
    # TODO: GET FREQUENCY OF EACH CHARACTER
    frequency ={}
    for character in data:
        if not character in frequency:
            frequency[character] = 0
        else:
            frequency[character] += 1
    return frequency


def huffman_coding(frequency_map):
    # TODO: HUFFMAN CODING ALGORITHM
    return {}, ""


def translate(data, language_map):
    # TODO: TRANSLATE THE INPUT DATA INTO THE CORRESPONDING CODE IN MAP
    return ""


def decompress():
    print("Decompression Selected")


def compress(data):
    print(data)
    # TODO: UNCOMMENT THE FOLLOWING WHEN READY
    #freq_map = {}
    #freq_map = frequency_map(data)
    #language_map = huffman_coding(freq_map)
    #compressed_data = translate(data, language_map)
    #return language_map, compressed_data


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
