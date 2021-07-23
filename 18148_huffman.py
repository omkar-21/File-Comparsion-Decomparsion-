from huffman import Huffman

path=input("Enter the path of your file : ")

h=Huffman(path)
output=h.compress()
h.decompress(output)
