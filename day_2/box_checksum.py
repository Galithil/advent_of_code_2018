#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
from collections import Counter
import argparse
import regex

class Checksummer(object):
    def __init__(self):
        self.boxes = []
        self.checksum = 0

    def load_input_file(self, file_name):
        with open(file_name, "rb") as f:
            lines = f.readlines()
            self.boxes = [x.strip() for x in lines]

    def compute_checksum(self):
        boxes_with_twos = 0
        boxes_with_threes = 0
        for box in self.boxes:
            c = Counter(box)
            if 2 in c.values():
                boxes_with_twos +=1
            if 3 in c.values():
                boxes_with_threes +=1

        self.checksum = boxes_with_twos * boxes_with_threes

    def identify_identical_boxes(self):
        sboxes = sorted(self.boxes)
        for i in xrange(len(sboxes)-1):
            pattern = "({0}){1}".format(sboxes[i], "{e<=1}")
            match = regex.findall(pattern, sboxes[i+1])
            if match or sboxes[i][1:] == sboxes[i+1][1:]:
                print("Found '{0}'".format(self.get_common_letters(sboxes[i], sboxes[i+1])))

    def get_common_letters(self, s1, s2):
        letters=[]
        for chars in zip(s1,s2):
            if chars[0] == chars[1]:
                letters.append(chars[0])
        return ''.join(letters)


def main(args):
    cs = Checksummer()
    cs.load_input_file(args.input)
    cs.compute_checksum()
    print("Checksum : {0}".format(cs.checksum))
    cs.identify_identical_boxes()




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", required=True)
    args = parser.parse_args()
    main(args)
