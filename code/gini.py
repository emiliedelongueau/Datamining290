# Emilie de Longueau
# HMK Gini_Index


#!/usr/bin/python

"""Script can be used to calculate the Gini Index of a column in a CSV file.

Classes are strings."""

import fileinput
import csv

(
    CMTE_ID, AMNDT_IND, RPT_TP, TRANSACTION_PGI, IMAGE_NUM, TRANSACTION_TP,
    ENTITY_TP, NAME, CITY, STATE, ZIP_CODE, EMPLOYER, OCCUPATION,
    TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID, CAND_ID, TRAN_ID, FILE_NUM,
    MEMO_CD, MEMO_TEXT, SUB_ID
) = range(22)

CANDIDATES = {
    'P80003338': 'Obama',
    'P80003353': 'Romney',
}

############### Set up variables
# TODO: declare datastructures
selection = []
obama_count = 0
romney_count =0

zipcode_dict = {} # Store information with zipcode as key and dict {'Obama': ob_cnt, 'Romney': ro_cnt} as value
gini_per_zipcode = []# store gini index 
split_gini = 0 # average weight gini index score over zipcode partition

count1_obama = 0 # obama counts for contribution < splitting value
count1_romney = 0
count2_obama = 0 # obama counts for contribution >= splitting value
count2_romney = 0
gini_min=[0, 1] # [splitting contribution value, min gini index associated]


############### Read through files
for row in csv.reader(fileinput.input('itpas2.txt'), delimiter='|'):
    candidate_id = row[CAND_ID]
    if candidate_id not in CANDIDATES:
        continue

    candidate_name = CANDIDATES[candidate_id]
    zip_code = row[ZIP_CODE][:5] # We only consider the 5 first digits for a zipcode
    contribution = row[TRANSACTION_AMT]
    ###
    # TODO: save information to calculate Gini Index
    selection.append([candidate_name, zip_code, contribution])
    

total = len(selection) # total number of records in the dataset (only for Obama & Romney)




## 1- current Gini Index using candidate name as the class

for i in selection:
    if i[0] == 'Obama':
        obama_count +=1
    elif i[0] == 'Romney':
        romney_count +=1    


gini = 1- (obama_count/float(total))**2 - (romney_count/float(total))**2  




## 2- Weighted average of the Gini Indexes using candidate names, split up by zip code

for i in selection:
    if i[1] not in zipcode_dict.keys():
        if i[0] == 'Obama':
            zipcode_dict[i[1]]= {'Obama': 1, 'Romney': 0}
        elif i[0] == 'Romney':
            zipcode_dict[i[1]] = {'Obama' : 0, 'Romney' : 1}
    else :
        if i[0] == 'Obama':
            zipcode_dict[i[1]]['Obama'] +=1
        elif i[0] == 'Romney':
            zipcode_dict[i[1]]['Romney'] +=1 

for j in zipcode_dict.keys():
    total_tmp = zipcode_dict[j]['Obama']+zipcode_dict[j]['Romney']
    gini_tmp = 1- (zipcode_dict[j]['Obama']/float(total_tmp))**2 - (zipcode_dict[j]['Romney']/float(total_tmp))**2
    gini_per_zipcode.append([gini_tmp, total_tmp])


for k in gini_per_zipcode:
    split_gini += k[0]*k[1]/float(total)


# 3- Weighted average of the Gini Indexes with continuous field attribute:
# We assume we use binary decision based on one splitting value for the continuous attribute "contribution amount"
 # We want to find the best splitting value, thus minimize the Gini index
 # For that, we sort the database on contribution amount(attribute) and linearly scan the values
 # each time updating the class counts in each of the partition, and computing Gini index
 
# Algorithm to find the contribution splitting value with lowest weighted gini index:

def gini_minimize(split_val, count1_ob, count2_ob, count1_rom, count2_rom, gini_m): 
#calculate gini_weighted for new splitting value, compare with minimum gini so far and update if lower
    tot1 = count1_ob+count1_rom
    gini1 = 1-(count1_ob/float(tot1))**2-(count1_rom/float(tot1))**2
    tot2 = count2_ob+count2_rom
    gini2 = 1-(count2_ob/float(tot2))**2-(count2_rom/float(tot2))**2
    gini_weighted = gini1*tot1/float(tot1+tot2) + gini2*tot2/float(tot1+tot2) #calculate weighted gini for the splitting value tested
    if gini_weighted < gini_m[1]:
        gini_m[0] = split_val
        gini_m[1] = gini_weighted


selection.sort(key = lambda x : int(x[2])) # sorted by increasing contributions
split_value = int(selection[0][2]) # initiation with lowest contribution (every contribution is higher than split_value at the beginning)
for i in selection: # initiate count values by scanning the sorted list
    if i[0] == 'Obama':
        count2_obama +=1
    elif i[0] == 'Romney':
        count2_romney +=1
total2 = count2_romney + count2_obama
gini_min = [split_value, 1-(count2_obama/float(total2))**2-(count2_romney/float(total2))**2] # no weight at the beginning


for j in selection[1:]: # test each splitting value, update of the count matrix and calculate new gini_min
    split_value = int(j[2]) # test a new splitting value
    if j[0] == 'Obama': 
        count1_obama+=1
        count2_obama-=1
    elif j[0] == 'Romney':
        count1_romney+=1
        count2_romney-=1
    gini_minimize(split_value,count1_obama, count2_obama, count1_romney, count2_romney, gini_min)

## Output

print "Gini Index: %s" % gini
print "Gini Index after split: %s" % split_gini
print "If we assume binary decision tree based on one splitting value for the continuous attribute 'contribution amount'"
print "[Best contribution splitting value, Lowest Gini Index after binary split]: %s " % gini_min
