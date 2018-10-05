#!/usr/local/bin/python
#
import argparse
import csv

parser = argparse.ArgumentParser(description="Naive Bayes Classifier")
parser.add_argument('-f', '--datafile', type=str, required=True)
parser.add_argument('-r', '--splitratio', type=float, default=0.67)
parser.add_argument('-m', '--mestimate', type=int, default=1)
args = parser.parse_args()

# process command line arguments
datafile = args.datafile
splitratio = args.splitratio
mestimate = args.mestimate

# initialize the various data stucture and elements
data_set = []
train_set = []
test_set = []
class_v = {} # class values vj and its count
class_prob = {} # class probabilities
attrs = []  # list of attributes, each attribute wil have list of attribute values
attrs_class = {} # key is [attr index, attr value, class value], and value is count of element
prob_attrs_class = {} #  key is [index, attr val, class], value is probability with m-estimate
prob_testdata = {} # probability of test data for each class

# verify that data is consistent i.e. each list has same attributes
dfhandle = open(datafile, "r")
data_set = list(csv.reader(dfhandle))
num_attr = len(data_set[0])
for ii in range(num_attr - 1):
    attrs.append([])

for item in data_set:
    if (len(item) != (num_attr )):
        print "Input Data inconsistent: ", item
        exit(1)

print("======================")
#print("Splitting the data into training and test set in the split ratio of ", splitratio)

data_size = len(data_set)
train_size = int(data_size * splitratio)
test_size = data_size - train_size
for ii in range(train_size):
    train_set.append(data_set[ii])
for ii in range(test_size):
    test_set.append(data_set[train_size + ii])

# Process each training set data and update the following.
# count of each classification value i.e vj
# Count of each attribute for each classification value i.e. count of attribute i for value vj
# count of each attribute value for each classification value vj

#count = 1
for sample in train_set:
    if  sample[-1] not in class_v:
        class_v[sample[-1]] = 0.0
        #print "Adding new class value: ", sample[-1]
    class_v[sample[-1]] += 1.0 # number of times a class has occurred
    class_val = sample[-1]
    for ii in range(len(sample)-1): # update attribute list with each new attribute value
        if sample[ii] not in attrs[ii]:
            attrs[ii].append(sample[ii])
        # Update the attribute count for attribute value along with class value
        attr_elem = (ii, sample[ii], class_val)
        #print attr_elem
        if  attr_elem not in attrs_class:
            attrs_class[attr_elem] = 0.0
        attrs_class[attr_elem] += 1.0

# compute class probabilities
for key in class_v:
    #print "key = ", key, "count = ", class_v[key]
    class_prob[key] = class_v[key] / train_size
    print "Probabilities of class ", key, "is ",  class_prob[key]

#print attrs
"""
count = 1
for attr_elem in attrs_class:
    print count, ":", attr_elem, ":", attrs_class[attr_elem], "prob = ", attrs_class[attr_elem] / class_v[attr_elem[2]]
    count += 1
"""

count=1
for ii in range(len(attrs)):
    for attrval in attrs[ii]:
        for key in class_v:
            # adjust the probability with m-estimate
            attr_elem = (ii, attrval, key)
            if attr_elem not in attrs_class:
                prob_attrs_class[attr_elem] = float(mestimate) / (class_v[key] + mestimate)
            else:
                prob_attrs_class[attr_elem] =  (mestimate * 1.0 / len(attrs[ii]) + attrs_class[attr_elem]) / (class_v[key] + mestimate)
                #print "Probability w/o m-estimate for", attr_elem, "is", attrs_class[attr_elem] / class_v[key]
            #print count, ": Probability for ", attr_elem, "is ", prob_attrs_class[attr_elem]
            #print ""
            count += 1

print("======================")
print "Computing probabilities for test set taken from input data"

count=0
cnt_err_classify = 0
cnt_not_classify = 0
for testdata in test_set:
    count += 1
    testelem = testdata[:-1]
    #print "data in testset: ", testelem
    max_prob = 0
    testelem_class = "NC"
    for key in class_v:
        prob_v = (class_v[key] / train_size)
        for ii in range(len(testelem)):
            #print "testelem[", ii, "] = ", testelem[ii]
            if testelem[ii] not in attrs[ii]:
                #print "Value ", testelem[ii], "for  attr # ", ii, "is not in training data", testdata
                prob_v = 0
                break
            attr_elem = (ii, testelem[ii], key)
            if attr_elem not in prob_attrs_class:
                print "The attribute elem ", attr_elem, "is not in training data"
                p_attr_elem = 0
            else:
                p_attr_elem =  prob_attrs_class[attr_elem]
            prob_v = prob_v * p_attr_elem
        #print "P(", key, ") P(", testelem, ") = ", prob_v
        if max_prob < prob_v:
            max_prob = prob_v
            testelem_class = key
    # classify the result
    print "classification for test data", testdata, "is ", testelem_class
    if testelem_class == "NC":
        cnt_not_classify += 1
    elif  testdata[-1] != testelem_class:
        cnt_err_classify += 1
print "Classification Stats, total test cnt = ", count, "NC =  ", cnt_not_classify, " predict error  = ",cnt_err_classify
print("======================")
