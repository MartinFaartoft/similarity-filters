import json
#data looks like: (k, space, total_input_size, fraction, data_row)
def avg(l):
    return sum(l) / float(len(l))

data = []
with open('wildcard/harvard_graph_with_wildcards_50.json', 'r') as datafile:
    data = json.load(datafile)

#print len(data)
#one frame for each step_k
frame = data[0]
#frame is a dictionary with reasonable keys
k, space, total_input_size, fraction, l, k, n, l_prime = frame['parameters']
print l_prime, l, k

close_stats = frame['close_stats']
#print close_stats
print len(close_stats), "should be 100 (number of candidates)"
print len(close_stats[0]), "should be 10, 20 or 30 (k)"
print len(close_stats[0][0]), "should be 2, (worst_case, actual)"
worst_sum = []
worst_max = []
worst_avg = []
actual_sum = []
actual_max = []
actual_avg = []
for i in range(len(close_stats)):
    stats_for_candidate = close_stats[i]
    #print stats_for_candidate
    
    worst_list = [worst for worst, actual in stats_for_candidate]
    actual_list = [actual for (worst, actual) in stats_for_candidate]
    
    worst_sum.append(sum(worst_list))
    worst_max.append(max(worst_list))
    worst_avg.append(avg(worst_list))
    
    actual_sum.append(sum(actual_list))
    actual_max.append(max(actual_list))
    actual_avg.append(avg(actual_list))
    

print sorted(actual_avg)