# Emilie de Longueau
# HMK Data Stats 02-13-2014

#!/usr/bin/python

"""This script can be used to analyze data in the 2012 Presidential Campaign,
available from ftp://ftp.fec.gov/FEC/2012/pas212.zip - data dictionary is at
http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml
"""

import fileinput
import csv

transactions = []
candidates = {} # dictionary for the analysis per candidate : keys: candidate unique ID number, values: list of transactions


for row in csv.reader(fileinput.input("/Users/Emilie/_Github/Datamining290T/code/itpas2.txt"), delimiter='|'):
    #if not fileinput.isfirstline(): #no longer necessary as there are no headers 
        
        transactions.append(float(row[14])) # create list of all transaction amounts

        # for the transaction analysis per candidate
        if row[16] not in candidates.keys(): # if candidate ID not in the dictionnary, we add him and the correponding transaction as value
            candidates[row[16]] = [float(row[14])]
        else : # if candidate already listed in the dictionary, we add the transaction to the list of transactions values for this candidate ID
            candidates[row[16]].append(float(row[14]))


# Total

total = sum (transactions)

# Minimum

minimum = min(transactions)

# Maximum

maximum = max(transactions)

# Mean

def mean_find (liste):
    return (sum(liste) / len(liste))

mean = mean_find(transactions)

# Median  

def median_find (liste):
    liste.sort()
    med = 0
    i = len(liste)
    if i%2 == 0 :
        med = (liste[i/2-1]+liste[i/2])/2 # mean of two central elements in the sorted list
    else :
        med = liste[i/2-1]
    return med

median = median_find(transactions)

# Standard deviation

def standard_deviation (liste):
    m = mean_find(liste)
    s = map(lambda x: (x-m)**2, liste)
    moy = mean_find(s)
    std = moy**0.5
    return std

standard_dev = standard_deviation(transactions)

# Zscore

zscore = map(lambda x: (x-mean)/standard_dev, transactions)

# min max normalize

def minmax_normalize(value):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normalization should use the minimum and maximum amounts from the full dataset"""
    norm = (value - minimum)/(maximum - minimum)
    return norm


### PRINT STATS
print 'STATS' + '\n'

print "Number of transactions: " + str(len(transactions))
print "Total: %s" % total
print "Minimum: %s" % minimum
print "Maximum: %s" % maximum
print "Mean: %s" % mean
print "Median: %s" % median
print "Standard Deviation: " + str(standard_dev)
print "Number of candidates: " + str(len(candidates))
print "Unique Candidates ID numbers:" + ' ,'.join(candidates.keys())
print "List of Zscores for each transactions" + ' ,'.join(map(str, zscore))
print "Min-max normalized values: %r" % map(minmax_normalize, transactions)
print '\n'




# EXTRA CREDIT: Stats per candidate

candidate_total = {}
candidate_min = {}
candidate_max = {}
candidate_mean = {}
candidate_med = {}
candidate_std ={}
candidate_zscore ={}

for ID in candidates.keys():
    candidate_total[ID] = sum(candidates[ID])
    candidate_min[ID] = min(candidates[ID])
    candidate_max[ID] = max(candidates[ID])
    candidate_mean[ID] = sum(candidates[ID])/len(candidates[ID])
    candidate_med[ID] = median_find(candidates[ID])
    candidate_std[ID] = standard_deviation(candidates[ID])

# Z-score of each ID candidate's total contributions within the distribution of all candidates' contributions
for ID in candidates.keys():
   candidate_zscore[ID] = (candidate_total[ID] - mean_find(candidate_total.values())) / standard_deviation(candidate_total.values())



### PRINT STATS PER CANDIDATE 
print 'STATS PER CANDIDATE + Z Score' +'\n'

print "Total per candidate: "
for keys, values in candidate_total.items():
    print (keys) + ' : ' + str(values) 
print '\n'

print "Minimum per candidate: "
for keys, values in candidate_min.items():
    print (keys) + ' : ' + str(values) 
print '\n'

print "Maximum per candidate: "
for keys, values in candidate_max.items():
    print (keys) + ' : ' + str(values) 
print '\n'

print "Mean per candidate: "
for keys, values in candidate_mean.items():
    print (keys) + ' : ' + str(values) 
print '\n'

print "Median per candidate: "
for keys, values in candidate_med.items():
    print (keys) + ' : ' + str(values)
print '\n' 

print "Standard deviation per candidate: "
for keys, values in candidate_std.items():
    print (keys) + ' : ' + str(values) 
print '\n'

print "Z-score of each candidate's total contribution within the distribution of all candidates'\
contributions: " 
for keys, values in candidate_zscore.items():
    print (keys) + ' : ' + str(values) 
print '\n'

