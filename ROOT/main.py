import Huffman
import os, sys
test_folder = "text//"
test_list = os.listdir(test_folder)
#print(test_list)
#print(len(test_list))
def run_test (algorithm):
    if algorithm == "huffman":
        for each_test in range(0, len(test_list)):
            print("Status: running test ", test_list[each_test])
            source_file = open(os.path.join(test_folder, test_list[each_test]), "r", encoding='utf-8')
            Huffman.compress(source_file)
            Huffman.decompress(dict_file, code_file)

