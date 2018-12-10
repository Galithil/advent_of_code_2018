#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import argparse
from itertools import cycle

class Calibrator(object):
    def __init__(self, start):
        self.start = start
        self.updates = []
        self.current_frequency = start

    def load_input_file(self, file_name):
        lines = []
        with open(file_name, "rb") as f:
            lines = f.readlines()
        for line in lines:
            self.updates.append(int(line))

    def run_updates(self):
        for update in self.updates:
            self.current_frequency = self.current_frequency + update

    def reset(self):
        self.current_frequency = self.start
        self.updates = []

    def search_for_twin_frequencies(self):
        seen_frequencies = []
        for update in cycle(self.updates):
            self.current_frequency = self.current_frequency + update
            if self.current_frequency not in seen_frequencies:
                seen_frequencies.append(self.current_frequency)
            else:
                break





def main(args):
    calibrator = Calibrator(args.start)
    calibrator.load_input_file(args.input)
    calibrator.run_updates()
    print("Frequency after 1 run : {0}".format(calibrator.current_frequency))
    calibrator.reset()
    calibrator.load_input_file(args.input)
    calibrator.search_for_twin_frequencies()
    print("First twin frequency : {0}".format(calibrator.current_frequency))




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", required=True)
    parser.add_argument("-s", "--start", dest="start", type=int, default=0)
    args = parser.parse_args()
    main(args)
