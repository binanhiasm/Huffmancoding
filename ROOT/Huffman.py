import heapq
import operator
import os
from bitstring import BitArray
import json
temp_reverse = {}
DIR_DATA = "data"
DIR_HUFFMAN = os.path.join(DIR_DATA,"huffman")
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
    #print (encoded_content)
    return encoded_content
def prepare_to_convert_bin_to_byte(content):
    added_code = 8 - len(content) % 8
    #print (added_code)
    for i in range(added_code):
        content = "0" + content
    encoded_added_code = "{0:08b}".format(added_code)
    #print (encoded_added_code)
    content = encoded_added_code + content
    return content
def convert_bin_to_byte(content):
    b = bytearray()
    for i in range(0, len(content), 8):
        byte = content[i:i + 8]
        b.append(int(byte, 2))
    return b
def compress(path):
    tree = []
    encoded_sympol = {}
    tempname, _ = os.path.splitext(path)
    filename = tempname.split("/")
    with open(path, 'r+', encoding='utf-8') as f:
        content = f.read()
        frequency = count_frequency(content)
        table_frequency = sort_table_frequency(frequency)
        #print("Table frequency: ", table_frequency)
        tree = tree_maker(tree,table_frequency)
        encoded_tree = encoded(encoded_sympol,temp_reverse,tree)
        #print ("Encoded sympol: " , encoded_sympol)
        file_dict = os.path.join(DIR_HUFFMAN,filename[-1] + "-dictionary" +".txt")
        with open(file_dict,'w+') as fd:
            fd.write(json.dumps(encoded_sympol))
        encoded_content = convert_text_to_code(encoded_sympol,content)
        #print ("Encoded content: \n", encoded_content)
        #print("\n",len(encoded_content))
        new_content = prepare_to_convert_bin_to_byte(encoded_content)
        byte_content = convert_bin_to_byte(new_content)
        #print (byte_content)

    file_com = os.path.join(DIR_HUFFMAN,filename[-1] + ".bin")
    with open(file_com, 'wb') as o:
        o.write(bytes(byte_content))
    print ("Completely compressed")
    return file_com

def decode(new_content):
    temp = new_content.bin
    added_num_info = temp[:8]
    added_num = int(added_num_info, 2)
    #print (added_num)
    temp = temp[8:]
    return temp[added_num:]
def decompress(path):
    with open (path,'rb') as f:
        content = f.read()
        #print(type(content))
        new_content = BitArray(bytes = content)
        new_content = decode(new_content)
        #print(new_content)
        #print (len(new_content))
        current_code = ""
        decoded_text = ""
        for bit in new_content:
            current_code += bit
            if (current_code in temp_reverse):
                character = temp_reverse[current_code]
                decoded_text += character
                current_code = ""
        #print (decoded_text)
    temp_reverse.clear()
    tempname, _ = os.path.splitext(path)
    filename = tempname.split("/")
    file_decom = filename[-1] + "-decoded" + ".txt"
    with open(file_decom, "w+", encoding='utf-8') as o:
        o.write(decoded_text)
    print("Completely decompressed")
    return (len(new_content))
#path = "E:/Hoctrentruong/HK1nam4/Multimedia/project2/ROOT/text.txt"

#print (DIR_HUFFMAN)
#a = compress(path)
#b = decompress(a)
#print(compression_ratio(path,b))
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
