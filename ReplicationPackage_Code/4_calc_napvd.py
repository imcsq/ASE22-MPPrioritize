import numpy as np
import argparse

parser = argparse.ArgumentParser(description='prioritize the test case')
parser.add_argument('--violation_record', help='the path to the result of recording the violation information', type=str)
parser.add_argument('--prioritization_file', help='the file including the prioritization of MPs', type=str)

args = parser.parse_args()

order=np.load(args.prioritization_file)

results = np.load(args.violation_record)
results = results.tolist()
violations=[]
count=0
d=dict()
for i in order:
    count += 1
    name = i[0]
    if results[name] == 1:
        violations.append(count)
apvd = 1 - (np.sum(violations) / (len(order) * len(violations))) + 1 / (2 * len(order))
apvd_min = len(violations) / (2 * len(order))
apvd_max = 1 - apvd_min
napvd = (apvd - apvd_min) / (apvd_max - apvd_min)
npavd=format(napvd,'.4f')
print('NAPVD is :')
print(napvd)