#!/usr/local/bin/python
#
import argparse
import csv
import random

parser = argparse.ArgumentParser(description="Naive Bayes Classifier")
parser.add_argument('-f', '--datafile', type=str, required=True)
parser.add_argument('-r', '--splitratio', type=float, default=0.67)
parser.add_argument('-t', '--testdata', type=str, default = "")
args = parser.parse_args()

#testdata = ['sunny', 'cool', 'high', 'strong']
datafile = args.datafile
splitratio = args.splitratio
testdata = args.testdata.split(',')

train_set = []
test_set = []
class_v = {} # class values vj and its count
class_prob = {} # class probabilities
attrs = []  # list of attributes, each attribute wil have list of attribute values
attrs_class = {} # key is [attr index, attr value, class value]
prob_testdata = {} # probability of test data for each class

# verify that data is consistent i.e. each list has same attributes
dfhandle = open(datafile, "r")
data_set = list(csv.reader(dfhandle))
random.shuffle(data_set)
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
train_set = data_set[:train_size]
test_set = data_set[train_size:]

# Process each training set data and update the following.
# count of each classification value i.e vj
# Count of each attribute for each classification value i.e. count of attribute i for value vj
# count of each attribute value for each classification value vj

for sample in train_set:
    class_val = sample[-1]
    if  class_val not in class_v:
        class_v[class_val] = 0.0  # new class value
    class_v[class_val] += 1.0 # count of this class value
    for ii in range(len(sample)-1): # update attribute list
        if sample[ii] not in attrs[ii]:
            attrs[ii].append(sample[ii])
        # Update the attribute count for attribute value along with class value
        attr_elem = (ii, sample[ii], class_val)
        #print attr_elem
        if  attr_elem not in attrs_class:
            attrs_class[attr_elem] = 0.0
        attrs_class[attr_elem] += 1.0 # count of attribute value for the given class value


# compute class probabilities
for key in class_v:
    #print "key = ", key, "count = ", class_v[key]
    class_prob[key] = class_v[key] / train_size
    print "Probabilities of class ", key, "is ",  class_prob[key]

#print attrs
count = 1
print class_v
for attr_elem in attrs_class:
    print  attr_elem, ":  prob = ", attrs_class[attr_elem],  "/",  class_v[attr_elem[2]],  "=", attrs_class[attr_elem] / class_v[attr_elem[2]]
    count += 1

if len(testdata) != num_attr - 1:
    print "Test data improper, len =", len(testdata), testdata
else:
    print "probability for testdata ", testdata
    for key in class_v:
        prob_v = (class_v[key] / train_size)
        for ii in range(len(testdata)):
            if testdata[ii] not in attrs[ii]:
                print "The attribute value ", testdata[ii], "for attribute num ", ii, "is not in training data"
            attr_elem = (ii, testdata[ii], key)
            if attr_elem not in attrs_class:
                print "The attribute elem ", attr_elem, "is not in training data"
                break
            prob_v = prob_v * (attrs_class[attr_elem] / class_v[key])
        print "P(", key, ") P(", testdata, ") = ", prob_v

print("======================")
print "Computing probabilities for test set taken from input data"

count=0
cnt_err_classify = 0
for testdata in test_set:
    count += 1
    testelem = testdata[:-1]
    #print "data in testset: ", testelem
    max_prob = 0
    for key in class_v:
        prob_v = (class_v[key] / train_size)
        for ii in range(len(testelem)):
            #print "testelem[", ii, "] = ", testelem[ii]
            if testelem[ii] not in attrs[ii]:
                print "The attribute value ", testelem[ii], "for attribute num ", ii, "is not in training data"
                #break
            attr_elem = (ii, testelem[ii], key)
            if attr_elem not in attrs_class:
                print "The attribute elem ", attr_elem, "is not in training data"
                p_attr_elem = 0
            else:
                p_attr_elem =  attrs_class[attr_elem] / class_v[key]
                #break
            prob_v = prob_v * p_attr_elem
        print "P(", key, ") P(", testelem, ") = ", prob_v
        if max_prob < prob_v:
            max_prob = prob_v
            testelem_class = key
    # classify the result
    print "classification for test data", testdata, "is ", testelem_class
    if testdata[-1] != testelem_class:
        cnt_err_classify += 1
print "Error rate in classification: ", cnt_err_classify, "out of ", count
print("======================")
