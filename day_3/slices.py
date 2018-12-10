#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import argparse
import re

class FabricHandler(object):
    def __init__(self):
        self.claims = []
        self.claimed_inches = set()
        self.shared_inches = set()
        self.safe_claims = set()
        self.perfect_claim = None
        self.start_pat = re.compile("([0-9]+),([0-9]+)")
        self.size_pat = re.compile("([0-9]+)x([0-9]+)")
        self.id_pat = re.compile("#([0-9]+)")

    def load_input_file(self, file_name):
        with open(file_name, "rb") as f:
            lines = f.readlines()
            self.claims = [x.strip() for x in lines]

    def process_claims(self):
        for claim in self.claims:
            claim_id = self.id_pat.findall(claim)[0][0]
            start = self.start_pat.findall(claim)[0]
            sizes = self.size_pat.findall(claim)[0]
            shared = False
            for i in xrange(int(sizes[0])):
                for j in xrange(int(sizes[1])):
                    current_inch = (int(start[0])+i, int(start[1])+j)
                    if current_inch in self.claimed_inches:
                        self.shared_inches.add(current_inch)
                        shared = True
                    else:
                        self.claimed_inches.add(current_inch)

            if not shared:
                self.safe_claims.add(claim)

    def find_perfect_claim(self):
        if not self.shared_inches:
            self.process_claims()
        for claim in self.safe_claims:
            claim_id = self.id_pat.findall(claim)[0][0]
            start = self.start_pat.findall(claim)[0]
            sizes = self.size_pat.findall(claim)[0]
            shared = False
            for i in xrange(int(sizes[0])):
                for j in xrange(int(sizes[1])):
                    current_inch = (int(start[0])+i, int(start[1])+j)
                    if current_inch in self.shared_inches :
                        shared = True

            if not shared:
                self.perfect_claim = claim
                break




def main(args):
    fh = FabricHandler()
    fh.load_input_file(args.input)
    fh.process_claims()
    print(len(fh.shared_inches))
    fh.find_perfect_claim()
    print("Perfect claim : {0}".format(fh.perfect_claim))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", required=True)
    args = parser.parse_args()
    main(args)
