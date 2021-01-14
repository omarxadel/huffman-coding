# Huffman Coding in txt Files Compression
  Using huffman coding to compress-decompress text files or folders containing text files.
# About
  Huffman coding algorithm is an algorithm for doing data compression, and it forms the basic idea behind file compression. This program performs text file compressions using the algorithm exactly by forming frequency map of the input characters, creating Huffman tree, encoding each character and finally combining the encoded string into bytes to compress it, then writing it into bin files.
# Usage
  - clone
  - `python3 main.py`
# Header Format
Header file is written by encoding the tree. When we are writing the file, the tree is already formed with its codes, we write it in a way that makes it easy to reconstruct it from the file and reassign the codes to it taking the least possible space in the file. We take the head of the Huffman tree and check whether it’s a leaf node or has children, if the node is a parent, 0 is written to the file and left and write are sent to the encode function, and recursively the tree is encoded until a leaf is reached, where we write 1 and the character code. When decoding the tree, the characters are read and the codes are reassigned.

# Example:
For an input: `aabcbaab`

The output header file is: `00101100011101100010101100001`

# Intuition 
0’s are written until we reach a leaf node, once it’s reached, we write 1 and the node’s character then we return the newly created node as the left node to the previous call of the function encode. The same happens for the right node. Finally all nodes construct the Huffman tree once again. Walking the steps shown in figure 6.1, we will construct the code mentioned above:

0 0 1 01100011 (ascii code for c letter) 1 01100010 (ascii code for b letter) 1 01100001 (ascii code for a letter)

# Algorithm
1. Compression
  1. read file
  1. create frequency map for characters
  1. create min heap as per character frequency
  1. construct huffman tree from min heap
  1. create language map that translates each character to codeword as per huffman tree encoding
  1. encode the huffman tree into bits (1 before a leaf node, 0 before a parent)1
  1. convert each character in the file to its equivalent character and add the encoded tree
  1. end
1. Decompression
  1. read file
  1. decode the encoded tree and create language map that translates bit patterns to characters
  1. convert each bit pattern to its equivalent character in the file
  1. end
# Contributing
Please feel free to submit issues and pull requests. I appreciate bug reports.

