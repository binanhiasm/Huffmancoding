import Huffman
import os, sys
DIR_DATA = "data"
DIR_HUFFMAN = os.path.join(DIR_DATA,"huffman")
test_folder = "text//"
test_list = os.listdir(test_folder)
#print(test_list)
#print(len(test_list))
def run_test (algorithm):
    if algorithm == "hm":
        for each_test in range(0, len(test_list)):
            print("Status: running test ", test_list[each_test])
            source_path = os.path.join(test_folder, test_list[each_test])
            compressed_file = Huffman.compress(source_path)
            decompressed_file = Huffman.decompress(compressed_file)
def compare(algorithm):
    if algorithm == "hm":
        for each_test in range(0, len(test_list)):
            print("Status: check accurency ", test_list[each_test])
            source_path = open(os.path.join(test_folder, test_list[each_test]),"r",encoding='utf-8')
            decoded_path = open(os.path.join(DIR_HUFFMAN,test_list[each_test][:-4]+"-decoded.txt"),"r",encoding='utf-8')
            source_text = source_path.read()
            decoded_text = decoded_path.read()
            source_text_list = source_text.split(" ")
            decode_text_list = decoded_text.split(" ")
            accurency = 0
            for each_text in range(len(source_text_list)):
                if (source_text_list[each_text] == decode_text_list[each_text]):
                    accurency = accurency + 1
                else:
                    print("error at (", each_test, "): ", source_text_list[each_text], " & ",
                          decode_text_list[each_text])
            print("-- Accurency: ", accurency / len(source_text_list))
def compression_ratio(algorithm):
    if algorithm == "hm":
        output_cr_hm = open(os.path.join(DIR_DATA, "compression_ratio_huffman.txt"), "w", encoding='utf-8')
        for each_test in range(0, len(test_list)):
            print("Status : calculate compression ratio ", test_list[each_test])
            source_path = os.path.join(test_folder, test_list[each_test])
            decoded_path = os.path.join(DIR_HUFFMAN, test_list[each_test][:-4] + ".bin")
            b0 = os.path.getsize(source_path)
            b1 = os.path.getsize(decoded_path)
            cr = b0/b1
            print("Compresssion ratio calculated: ", )
            output_cr_hm.write(test_list[each_test] + "\t" + str(cr) + "\n")
        output_cr_hm.close()
def main():
    algorithms = ["lzw","sf","hm"]
    for each_algorithm in algorithms:
        run_test(each_algorithm)
        compare(each_algorithm)
        compression_ratio(each_algorithm)
main()