#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import argparse
import re
from datetime import datetime
from collections import Counter


class Guard(object):
    def __init__(self, id=None):
        self.id = id
        self.time_slept = 0
        self.minute_most_slept = None
        self.occurences_sleeping_on_minute = None
        self.logs = []
        self.minutes_slept = []

    def __repr__(self):
        return "Slept {0} minutes, most often on {1}".format(self.time_slept, self.minute_most_slept)

class SnoozeHandler(object):
    def __init__(self):
        self.logs = []
        self.guards = {}
        self.log_pattern = re.compile("\[([0-9]+\-[0-9]+\-[0-9]+\s+[0-9]+\:[0-9]+)\]\s+(.+)")
        self.guard_id_pattern = re.compile("#([0-9]+)")
        self.minute_most_slept = 0
        self.sleepyhead_id = None
        self.best_naptime = None
        self.nappyhead_id = None

    def load_input_file(self, file_name):
        with open(file_name, "rb") as f:
            lines = f.readlines()
            self.logs = sorted([x.strip() for x in lines])

    def set_guards_schedules(self):
        current_guard = Guard()
        for log in self.logs:
            matches = self.log_pattern.findall(log)[0]
            time = datetime.strptime(matches[0], '%Y-%m-%d %H:%M')
            message = matches[1]
            try:
                current_id = self.guard_id_pattern.findall(message)[0]
            except IndexError:
                #not a taking shift line
                if 'asleep' in message:
                    minutes = time.minute
                    current_guard.minutes_slept.append(minutes)
                elif 'wakes up' in message:
                    for i in xrange(current_guard.minutes_slept[-1]+1, time.minute):
                        current_guard.minutes_slept.append(i)

            else:
                if current_guard.id is not None:
                    self.guards[current_guard.id] = current_guard
                if current_id in self.guards:
                    current_guard = self.guards[current_id]
                else:
                    current_guard = Guard(current_id)


    def compute_time_specs(self):
        for guard_id in self.guards:
            guard = self.guards[guard_id]
            guard.time_slept = len(guard.minutes_slept)
            c = Counter(guard.minutes_slept)
            try:
                guard.minute_most_slept = int(c.most_common(1)[0][0])
                guard.occurences_sleeping_on_minute = c.most_common(1)[0][1]

            except:
                pass


    def find_best_sleepyhead(self):
        most_minutes_slept = 0
        for guard_id in self.guards:
            guard = self.guards[guard_id]
            if guard.time_slept > most_minutes_slept:
                most_minutes_slept = guard.time_slept
                self.minute_most_slept = guard.minute_most_slept
                self.sleepyhead_id = int(guard.id)

    def find_best_naptime(self):
        best_score = 0
        for guard_id in self.guards:
            guard = self.guards[guard_id]
            if guard.occurences_sleeping_on_minute > best_score:
                best_score = guard.occurences_sleeping_on_minute
                self.best_naptime = guard.minute_most_slept
                self.nappyhead_id = int(guard.id)







def main(args):
    sh = SnoozeHandler()
    sh.load_input_file(args.input)
    sh.set_guards_schedules()
    sh.compute_time_specs()
    #from pprint import pprint
    #pprint(sh.guards)
    sh.find_best_sleepyhead()
    print("Expected Result : {0}".format(sh.sleepyhead_id * sh.minute_most_slept))
    sh.find_best_naptime()
    print("Expected Result (2): {0}".format(sh.nappyhead_id * sh.best_naptime))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", required=True)
    args = parser.parse_args()
    main(args)
