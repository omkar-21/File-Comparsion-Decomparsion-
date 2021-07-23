
import heapq
import os
from collections import Counter
import json

class HuffmanTree(object):
    
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __eq__(self, other):
        return HuffmanTree.__check(other) and self.freq == other.freq

    def __ne__(self, other):
        return HuffmanTree.__check(other) and self.freq != other.freq

    def __lt__(self, other):
        return HuffmanTree.__check(other) and self.freq < other.freq

    def __le__(self, other):
        return HuffmanTree.__check(other) and self.freq <= other.freq

    def __gt__(self, other):
        return HuffmanTree.__check(other) and self.freq > other.freq

    def __ge__(self, other):
        return HuffmanTree.__check(other) and self.freq >= other.freq

    
    def __check(other):
        if other is None:
            return False
        if not isinstance(other, HuffmanTree):
            return False
        return True

    def __repr__(self):
        return "Char[%s]->Freq[%s]" % (self.c, self.freq)


def apply_merge(heap):

    n1 = heapq.heappop(heap)
    n2 = heapq.heappop(heap)
    merged = HuffmanTree(None, n1.freq + n2.freq)
    merged.left = n1
    merged.right = n2
    heapq.heappush(heap, merged)


def con_heap(d):
    
    heap = []
    for k, v in d.items():
        heapq.heappush(heap, HuffmanTree(k, v))
    return heap





def codify(codes, reverse_mapping, root, current=''):
    
    if root is not None:
        if root.char is not None:
            codes[root.char] = current
            reverse_mapping[current] = root.char
            return
        codify(codes, reverse_mapping, root.left, current + "0")
        codify(codes, reverse_mapping, root.right, current + "1")


def padding(enc_text):
    
    extra_pad = 8 - len(enc_text) % 8
    pad_info = "{0:08b}".format(extra_pad)
    return pad_info + enc_text + ''.join(["0"] * extra_pad)


def byte_dump(padded_encoded_text):
    
    if len(padded_encoded_text) % 8 != 0:
        raise Exception("Encoded text not padded properly")
    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i + 8]
        b.append(int(byte, 2))
    return b


def huffman_compress(text):

    heap = con_heap(Counter(text))
    while len(heap) > 1:
        # merge shall be repeated until all
        # of Huffman's trees has been combined into one
        apply_merge(heap)

    codes, reverse_mapping = {}, {}
    codify(codes, reverse_mapping, heapq.heappop(heap))

    encoded_text = ''.join([codes[c] for c in text])
    padded_encoded_text = padding(encoded_text)

    return reverse_mapping, bytes(byte_dump(padded_encoded_text))


def decode_text(reverse_mapping, encoded_text):
    
    current = ""
    decoded_text = ""
    for bit in encoded_text:
        current += bit
        if (current in reverse_mapping):
            character = reverse_mapping[current]
            decoded_text += character
            current = ""
    return decoded_text


def get_ridof_padding(padded_encoded_text):

    padded_info = padded_encoded_text[:8]
    extrapadding = int(padded_info, 2)

    padded_encoded_text = padded_encoded_text[8:]
    encoded_text = padded_encoded_text[:-1 * extrapadding]

    return encoded_text


class Huffman(object):

    def __init__(self, path):
        self.path = path
        self.reverse_mapping = {}

    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"
        output_path2 = filename + "_table" + ".bin"

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output,open(output_path2, 'wb') as table:
            text = file.read()
            text = text.rstrip()

            reverse_mapping, ba = huffman_compress(text)
            input=json.dumps(reverse_mapping)
            p=input.encode()
            table.write(p)
            output.write(ba)

        print("Compressed")
        return output_path

    def decompress(self, input_path):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"
        output_path2 = filename + "_table" + ".bin"

        with open(input_path, 'rb') as file, open(output_path, 'w') as output, open(output_path2, 'rb') as table:
            bit_string = ""
            input=table.read()
            p=input.decode()
            reverse_mapping=json.loads(p)
            byte = file.read(1)
            while (byte != " " and len(byte)!= 0):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = get_ridof_padding(bit_string)

            decompressed_text = decode_text(reverse_mapping, encoded_text)
            output.write(decompressed_text)

        print("Decompressed")
        return output_path

