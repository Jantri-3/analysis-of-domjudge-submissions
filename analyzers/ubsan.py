import json
import os
import re
from collections import Counter


def parseLogs(): 
    json_object = {}
    count = 0
    with open('index_clase.json', 'r') as index:
        index_json = json.load(index)
    for sid, submission in index_json.items():
        if os.path.exists(f"asan_todos/{sid}"):
            for case in os.listdir(f"asan_todos/{sid}"):
                if os.path.exists(f"asan_todos/{sid}/{case}/ubsan.log"):
                    with open(f"asan_todos/{sid}/{case}/ubsan.log") as readFile:
                        set_errors = set()
                        lines = readFile.readlines()
                        for line in lines:
                            if line == '\n':
                                continue
                            try:
                                error = line.split(':')[4]#[1:14]
                                error = re.sub( "\d" , '',error)
                                error = re.sub( r"of type.*" , '',error)
                                pattern = r"(overflowed)( to (xa|xb|xc|xd|xe|xf).*)?$"
                                error = re.sub( pattern, r"\1",error)
                                pattern2 = r"(base)( (x|xa|xb|xc|xd|xe|xf).*)?$"
                                error = re.sub( pattern2, r"\1",error)
                                pattern3 = r"(address)( (x|xa|xb|xc|xd|xe|xf).*)?$"
                                error = re.sub( pattern3, r"\1",error)
                                error = re.sub("\n", "", error)
                            except IndexError:
                                continue
                            #if error repited in same test case = NOT APPEND
                            set_errors.add(error)
                        submission['runs'][int(case) - 1]['list_errors'] =list(set_errors)
    with open('index_ubsan_case.json','w') as ubs:
        json.dump(index_json, ubs, indent = 4) 

def count_cases():
    with open('index_ubsan_case.json') as ubs:
        index = json.load(ubs)
    
    counter_results_cases = Counter()
    for submission in index.values():
        for run in submission['runs']:
            if run.get('list_errors'):
                counter_results_cases[run['result']] += 1
    print(counter_results_cases)

def count_submissions():
    with open('index_ubsan_case.json') as ubs:
        index = json.load(ubs)

    counter_results = Counter()
    for submission in index.values():
        ubsan_errors = False
        for run in submission['runs']:
            if run.get('list_errors'):
                ubsan_errors = True
                break
        if ubsan_errors:
            counter_results[submission['result']] += 1
    print(counter_results)

if __name__ == '__main__':
    #parseLogs()
    #count_cases()
    count_submissions()
            

