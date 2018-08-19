#!/usr/local/bin/python
#
import argparse
import csv

parser = argparse.ArgumentParser(description="Find-S algorithm")
parser.add_argument('-f', '--datafile', type=str, required=True)
args = parser.parse_args()

datafile = args.datafile
dfhandle = open(datafile, "r")
data = list(csv.reader(dfhandle))

validdata = [ ['Sunny', 'Cloudy', 'Rainy']
                , ['Warm', 'Cold']
                , ['High', 'Normal']
                , ['Strong', 'Weak']
                , ['Warm', 'Cool']
                , ['Same', 'Change']
             ]

# Verify that training data has been read properly as list of lists
for datarow in data:
    print datarow

# verify that data is consistent i.e. each list has same attributes
num_attr = len(validdata)
for item in data:
    if (len(item) != (num_attr + 1)):
        print "Input Data inconsistent: ", item
        exit(1)
    for ii in range(len(item) - 1):
        if (item[ii] not in validdata[ii]):
            print "Input data value", item[ii], "not valid"
            exit(1)


# Initialise hypothesis  to reject every instance
# '0' - no value is accepted.
# '?' - every value is accepted.
hypothesis = ['0'] * (num_attr)

print("======================")
print("Initial Hypothesis:", hypothesis)

# Process each data row.
# Consider only positive row i.e. last element is yes.
count = 1
for sample in data:
    if (sample[-1].lower() != "yes"):
        print "Ignoring False Sample: ", sample
        continue
    # training sample data is positive, process it to update hypothesis
    # check for each attribute in sample
    #print "Processing sample: ", sample
    for ii in range(len(sample) - 1):
        # if hypo is '0', replace it with sample
        if (hypothesis[ii] == '0'):
            hypothesis[ii] = sample[ii]
        # if hypo is different from sample, set it to '?'
        elif (hypothesis[ii] != sample[ii]):
            hypothesis[ii] = '?'
    print "Hypothesis after sample number", count, "processed: ", hypothesis
    count = count + 1

print("==================")
print("Final Hypothesis: ", hypothesis)
