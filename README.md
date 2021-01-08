# Huffman Coding in txt Files Compression
  Using huffman coding to compress-decompress text files or folders containing text files.
# About
  Huffman coding algorithm is an algorithm for doing data compression, and it forms the basic idea behind file compression. This program performs txt file compressions using the algorithm exactly by forming frequency map of the input characters, creating huffman heap, encoding each character and finally combining code in bytes to compress it, encoding it in UTF-8 then writing it in either txt or bin files.
# Usage
  - clone
  - `python3 main.py`
# Compressed File Structure
<table>
<tr> <td colspan="2">  N= total number of unique characters                      </td> </tr>
<tr> <td> Character[1 byte]   </td><td>  Binary codeword String Form             </td> </tr>
<tr> <td> Character[1 byte]   </td><td>  Binary codeword String Form             </td> </tr>
<tr> <td colspan="2">              N times                                       </td> </tr>
<tr> <td> padding             </td><td> p times 0's (padding bits)               </td> </tr>
<tr> <td colspan="2">  DATA                                                      </td> </tr>
</table>

p = Padding done to ensure file fits in whole number of bytes. eg, file of 4 bytes + 3 bits must ne padded by 5 bits to make it 5 bytes.
# Example
Text: aabcbaab

| Content                           | Comment                               |
|-----------------------------------|---------------------------------------|
|3                                  | N=3 (a,b,c)                           |
|c 00                               | character and corresponding code "00" |
|b 01                               | character and corresponding code "01" |
|a 1                                | character and corresponding code "1"  |
|4              		                | Padding count                         |
|ÑÐ                                 | Actual data, code in place of char    |
# Algorithm
0. Compression
  0.0. read file
  0.0. create frequency map for characters
  0.0. create min heap as per character frequency
  0.0. construct huffman tree from min heap
  0.0. create language map that translates each character to codeword as per huffman tree encoding
  0.0. convert each character in the file to its equivalent character and add the header file
  0.0. end
0. Decompression
  0.0. read file
  0.0. extract the header and create language map that translates bit patterns to characters
  0.0. convert each bit pattern to its equivalent character in the file
  0.0. end
# Contributing
Please feel free to submit issues and pull requests. I appreciate bug reports.

