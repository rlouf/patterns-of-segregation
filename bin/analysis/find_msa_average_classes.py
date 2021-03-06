"""find_classes.py

Find the emergent classes from the exposure matrix averaged over all MSAs in the
US
"""
import csv
import marble as mb


#
# Import exposure data
#

## List of MSA
msa = {}
with open('data/names/msa.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    reader.next()
    for rows in reader:
        msa[rows[0]] = rows[1]

## Import exposure values
exposure_val = {}
with open('extr/exposure/categories/us/msa_average/values.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    categories = reader.next()[1:]
    for rows in reader:
        exposure_val[int(rows[0])] = {int(cat): float(val) for cat, val 
                                          in zip(categories, rows[1:])}

## Import exposure variance
exposure_var = {}
with open('extr/exposure/categories/us/msa_average/variance.csv', 'r') as source:
    reader = csv.reader(source, delimiter='\t')
    categories = reader.next()[1:]
    for rows in reader:
        exposure_var[int(rows[0])] = {int(cat): float(var) for cat, var 
                                          in zip(categories, rows[1:])}

## Households income
households_all = {}
for i, city in enumerate(msa):
    ## Import household income distribution
    households = {}
    with open('data/income/msa/%s/income.csv'%city, 'r') as source:
        reader = csv.reader(source, delimiter='\t')
        reader.next()
        for rows in reader:
            num_cat = len(rows[1:])
            households[rows[0]] = {c:int(h) for c,h in enumerate(rows[1:])}
            households_all[rows[0]] = {c:int(h) for c,h in enumerate(rows[1:])}



#
# Concantenate exposure values and variance
#
categories = [int(k) for k in exposure_val.iterkeys()]
exp = {c0: {c1: (exposure_val[c0][c1],
                 exposure_var[c0][c1])
            for c1 in categories}
       for c0 in categories}


#
# Extract linkage matrix
#
classes = mb.uncover_classes(households_all, exp)

#
# Prompt for names
#
print "Classes have been found! We need you to name them..."
print "Classes are the following:"
for cl in classes:
    print cl
print "\n"

names = []
for cl in classes:
    names.append(raw_input("Give a name for the class containing %s\n"%cl))
print "Thanks!"


#
# Print classes and their composition
#
with open('extr/classes/msa_average/classes.csv', 'w') as output:
    output.write('Class name\tComposition\n')
    for name, cl in zip(names, classes):
        output.write("%s\t"%name + "\t".join(map(str, cl)) + "\n")
