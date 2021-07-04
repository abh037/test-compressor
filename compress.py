import sys
import operator
import os

class Node:
    def __init__(self, count, letter, left, right):
        self.letter = letter
        self.count = count
        self.right = left
        self.left = right
        
def get_codes(current_code, current_node, codes):
    if current_node.letter == None:
        get_codes(current_code + "0", current_node.left, codes)
        get_codes(current_code + "1", current_node.right, codes)
    else:
        codes.update({current_node.letter : current_code})
    return codes
        
        
def encode():
    print "Reading file..."
    queue = []
    codes = {}
    txt = open(sys.argv[2], 'r')
    curr = ' '
    f = {}
    largest = 0
    let = ''
    while curr:
        curr = txt.read(1)
        if curr is not '':
            if f.get(curr):
                if f.get(curr) > largest:
                    largest = f.get(curr)
                f.update({curr : (f.get(curr) + 1)})
            else:
                f.update({curr : 1})
       
    print "Compressing..."
    for i in f.keys():
        f.update({i : abs(int((255 * f.get(i)) / largest) - 1)})
   
    f = sorted(f.items(), key = operator.itemgetter(1))
    f.reverse()
    for i in f:
        queue.append(Node(i[1], i[0], None, None))
        
    while len(queue) > 1:
        first = queue.pop(-1)
        second = queue.pop(-1)
        idx = 0
        for i in queue:
            if i.count >= first.count + second.count:
                idx += 1
        queue.insert(idx, Node(first.count + second.count, None, first, second))
    tree = queue.pop()
    codes = get_codes("", tree, codes)

    outputtxt = open("compressed_output.txt", 'w')
    bitstring = ""
    bitstring += str(format(len(f), '08b'))
    for i in f:
        if i[0] is not '':
            bitstring += str(format(ord(i[0]), '08b'))
            bitstring += str(format(i[1], '08b'))
    reader = open(sys.argv[2], 'r')
    curr = ' '
    while curr:
        curr = reader.read(1)
        if curr is not '':
            bitstring += str(codes.get(curr))
    while len(bitstring) % 8 != 0:
        bitstring += "0"
    tmp = ""
    for i in bitstring:
        if len(tmp) == 8:
            outputtxt.write(chr(int(tmp, 2)))
            tmp = ""
        tmp += i
    if len(tmp) > 0:
        outputtxt.write(chr(int(tmp, 2)))
    print "Successful!"
    amt = os.path.getsize(sys.argv[2]) - os.path.getsize("compressed_output.txt")
    amt = (100 * amt) / os.path.getsize(sys.argv[2])
    print "Size reduced by " + str(amt) + "%"

    

        
def decode():
    print "Decompressing..."
    f = []
    queue = []
    codes = {}
    txt = open(sys.argv[2])
    l = ord(txt.read(1))
    for i in range(0, l):
        character = chr(int(str(format(ord(txt.read(1)), '08b')), 2))
        count = int(str(format(ord(txt.read(1)), '08b')), 2)
        f.append((character, count))
    for i in f:
        queue.append(Node(i[1], i[0], None, None))
        
    while len(queue) > 1:
        first = queue.pop(-1)
        second = queue.pop(-1)
        idx = 0
        for i in queue:
            if i.count >= first.count + second.count:
                idx += 1
        queue.insert(idx, Node(first.count + second.count, None, first, second))
        
    tree = queue.pop()
    codes = get_codes("", tree, codes)
    chrstr = txt.read()
    remainder = ""
    for i in chrstr:
        remainder += str(format(ord(i), '08b'))
    curr = tree
    output = open("decompressed_output.txt", 'w')
    for p in remainder:
        if p == '0':
            curr = curr.left
        else:
            curr = curr.right
        if curr.letter is not None:
            output.write(curr.letter)
            curr = tree
    print "Successful!"
        

if sys.argv[1] == "encode":
    encode()
elif sys.argv[1] == "decode":
    decode()
else:
    raise Exception("Invalid command")
    




