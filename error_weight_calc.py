# Emilie de Longueau
# HMK 5 - Neural networks

# FORMULA:
# Output error: errx = ox*(1-ox)*(tx-ox)
# Hidden layer erry == oy*(1-oy)*sum(errk wyk)
# Find new weights: wij = wij + l*errj*oi
# l: learn rate

o = [[1, 2], [0.7311, 0.0179, 0.9933], 0.8387] # ouputs
t = 0 # Final value expected
w = [[-3, 2, 4], [2, -3, 0.5], [0.2, 0.7, 1.5]] # Weights

output_index = len(o) - 1

# Output error
output_err = o[output_index]*(1-o[output_index])*(t-o[output_index])
print "Output error is {0}".format(output_err)

# Errors for hidden layer (3 nodes)
err = []
for i in range(3):
	err.append (o[1][i]*(1-o[1][i])*output_err*w[2][i])
print "Errors in hidden layer are {0}".format(err)

# New weights from hidden layer to output node
l = 10 # learn rate
new_weight=[]

for j in w[2]:
	calc = j + l * output_err * o[1][w[2].index(j)]
	new_weight.append(calc)
print "New weights from hidden layer to output layer are {0}".format(new_weight)


# New weights from input nodes (2) to hidden layer (3 nodes)
	# Input node 1 to hidden layer
new_weight2=[]
for j in w[0]:
	calc = j + l * err[w[0].index(j)] * o[0][0]
	new_weight2.append(calc)
print "New weights from intput layer node 1 to hidden layer are {0}".format(new_weight2)

	# Input node 2 to hidden layer
new_weight3=[]
for j in w[1]:
	calc = j + l * err[w[1].index(j)] * o[0][1]
	new_weight3.append(calc)
print "New weights from intput layer node 2 to hidden layer are {0}".format(new_weight3)


