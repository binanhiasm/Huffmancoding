import heapq
import operator
import os
class Node:
    #build a class node with sympol, frequency, left node, right node
    def __init__(self,sympol=None,frequency=None,left_node=None,right_node=None):
        self.sympol = sympol
        self.frequency = frequency
        self.left_node = left_node
        self.right_node = right_node
    # defining comparators less_than
    def __lt__(self, other):
        return self.frequency < other.frequency
def count_frequency(content):
    table_frequency = {}
    for sym in content:
        if not sym in table_frequency:
            table_frequency[sym] = 0;
        table_frequency[sym] +=1
    return table_frequency
def sort_table_frequency(table_frequency):
    sorted_table_frequency = sorted(table_frequency.items(), key=operator.itemgetter(1))
    sorted_table_frequency = dict(sorted_table_frequency)
    return sorted_table_frequency
def tree_maker(tree,table_frequency):
    for each_sym in table_frequency:
        node = Node(each_sym,table_frequency[each_sym])
        heapq.heappush(tree,node)
    #print(len(tree))
    while (len(tree)>1):
        nodel = heapq.heappop(tree)
        noder = heapq.heappop(tree)
        internal_weight = nodel.frequency + noder.frequency
        #print(internal_weight)
        internal_node = Node(None,internal_weight,nodel,noder)
        heapq.heappush(tree,internal_node)
    return tree
def encode_reverse(encoded_sympol,temp_reverse,parent, temp_way):
    if (parent == None ):
        return
    if (parent.sympol != None):
        encoded_sympol[parent.sympol] = temp_way
        temp_reverse[temp_way] = parent.sympol
        return
    encode_reverse(encoded_sympol,temp_reverse,parent.left_node,temp_way + "0")
    encode_reverse(encoded_sympol,temp_reverse,parent.right_node,temp_way + "1")
def encoded(encoded_sympol,temp_reverse,tree):
    parent = heapq.heappop(tree)
    temp_path = ""
    encode_reverse(encoded_sympol,temp_reverse,parent,temp_path)
def convert_text_to_code(encoded_sympol,content):
    encoded_content = ""
    for sym in content:
        encoded_content = encoded_content + encoded_sympol[sym]
    return encoded_content
def prepare_to_convert_bin_to_byte(content):
    added_code = 8 - len(content) % 8
    for i in range(added_code):
        content = content + "0"
    return content
def convert_bin_to_byte(content):
    v = int(content, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])
def compress(path):
    tree = []
    encoded_sympol = {}
    temp_reverse = {}
    with open(path, 'r+', encoding='utf-8') as f:
        content = f.read()
        frequency = count_frequency(content)
        table_frequency = sort_table_frequency(frequency)
        #print("Table frequency: ", table_frequency)
        tree = tree_maker(tree,table_frequency)
        encoded_tree = encoded(encoded_sympol,temp_reverse,tree)
        #print ("Encoded sympol: " , encoded_sympol)
        encoded_content = convert_text_to_code(encoded_sympol,content)
        print ("Encoded content: \n", encoded_content)
        new_content = prepare_to_convert_bin_to_byte(encoded_content)
        byte_content = convert_bin_to_byte(new_content)
        #print (byte_content)
    filename, _ = os.path.splitext(path)
    file_out = filename +"_com" + ".bin"
    with open(file_out, 'wb') as o:
        o.write(bytes(byte_content))
    print ("Completely compressed")
    return file_out
def decode(new_content):
    ...

def decompress(path):
    filename, _ = os.path.splitext(path)
    file_out = filename + "-decom" + ".txt"
    with open (path,'rb') as f:
        content = f.read(1)
        print(type(content))
        #print (content)
        new_content = ""
        while(len(content)>0):
            content = ord(content)
            bits = bin(content)[2:].rjust(8, '0')
            new_content += bits
            content = f.read()
        print (new_content)
path = "E:/Hoctrentruong/HK1nam4/Multimedia/project2/text.txt"
a = compress(path)
b = decompress(a)
#print (a)
#content = "AAXAXSAAXAXAXACACAXACASXACASCSAXAXACACXACAXAXASADSDCCSXSXSCS"
#          111110111001111111011101110
#result    111110111001111111011101110110011001110110011011101100110110001111101110110011001011001110111011011110100110100000011100111001100011

#a = count_frequency(content)
#print (a)
#print (type(a))
#b = sort_table_frequency(a)
#print(b)
#print(type(b))
#c = tree_maker(tree,b)
#print (c)
#d = encoded(encoded_sympol,temp_reverse,c)
#print ("Encoded sympol: " , encoded_sympol)
#f = convert_text_to_code(encoded_sympol,content)
#print ("Encoded content: ",f)
