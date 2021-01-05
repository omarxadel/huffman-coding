def frequency_map(data):
    return None


# def huffman_coding(map):#TODO:ADD HUFFMAN CODING

def decompress():
    print("Decompression")


def compress():
    print("Compress")


if __name__ == '__main__':
    # GET FILE NAME
    filename = input("Enter file name ")
    while True:
        try:
            f = open(filename, 'r', encoding="utf8")
            break
        except IOError:
            filename = input("Enter a valid file name ")

    # GET OPERATION TYPE ( COMPRESSION or DECOMPRESSION )
    while True:
        op_type = int(input("Enter the mode (0 for Compression | 1 for Decompression) "))
        if op_type == 0:
            compress()
            break
        elif op_type == 1:
            decompress()
            break
        else:
            print("Please enter a valid number")
            continue

