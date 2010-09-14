def initDatabase(fname):
    f = open(fname)
    database = {}
    line = f.readline()
    i = 0
    while line != '':
		items = line.split()
		database[i] = [int(item) for item in items]
		line = f.readline()
		i = i + 1
    f.close()
    return database

def support_count(tran, nodes, index, depth_left):
	if depth_left > 0:
		for i in range(len(tran)):
			# a trick, depth_left represents how many item is needed at least
			if depth_left > len(tran[i+1:]):
				return
			if tran[i] in nodes[index]:
				[index2, count] = nodes[index][tran[i]]
				support_count(tran[i+1:], nodes, index2, depth_left - 1)
	else:
		for item in tran:
			if item in nodes[index]:
				nodes[index][item][1] += 1

def frequentItemsets(datafile, begin, end, threshold = 20):
	database = initDatabase(datafile)
	node = {}									# the main structure to maintain the trie
	# node[index][item] = [node_index, count], item is the label of edge, node_index is the index of node linked by the edge,
	# count is the frequent of the itemset represented by the linked node
	node[0] = {}	# root node of trie
	# this structure stores the candidate k-itemsets and frequent itemsets in the same structure, 
	# index k represents this is a k-itemsets candidate or frequent itemsets 
	candidate = {}
	candidate[0] = {():[0,0]}					# key is the itemset, value[0] is trie node index, value[1] is frequent of the itemset
	candidate[1] = {}
	node_index = 1								# iterative index of trie
	for item in range(begin, end+1):
		node[0][item] = [node_index, 0]	
		node[node_index] = {}
		candidate[1][(item,)] = [node_index, 0]
		node_index += 1

	k = 1
	while len(candidate[k]) > 0:
		print '%d-itemsets begin...\tcandidate: %d' % (k, len(candidate[k]))
		# caculate the support count the k-itemsets
		for (tid, tran) in database.items():
			support_count(tran, node, 0, k - 1)

		# find the frequent itemsets in candidate, delete the unfrequent ones
		for (itemset,[i,c]) in candidate[k-1].items():
			for (item, [index, count]) in node[i].items():
				if count < threshold:
					node[i].pop(item)
					candidate[k].pop(itemset + (item,))
				else:
					candidate[k][itemset + (item,)][1] = count

		# construct the candidate k+1-itemsets
		candidate[k+1] = {}
		for (itemset,[i,c]) in candidate[k-1].items():
			keys = node[i].keys()
			keys.sort()							# because the keys may be un-sorted
			for j in range(len(keys)-1):
				for h in range(j+1, len(keys)):
					flag = 1
					tmp = itemset + (keys[j],keys[h])
					for g in range(k-1):
						tmp2 = tmp[:g] + tmp[g+1:]
						if tmp2 not in candidate[k]:
							flag = 0
							break
					if flag == 1:
						index = node[i][keys[j]][0]
						node[index][keys[h]] = [node_index, 0]
						node[node_index] = {}
						candidate[k+1][tmp] = [node_index, 0]
						node_index += 1
		k += 1
	return candidate
