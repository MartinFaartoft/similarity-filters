import json
#data looks like: (k, space, total_input_size, fraction, data_row)
data = []
with open('wildcard/harvard_graph_with_wildcards_100.json', 'r') as datafile:
    data = json.load(datafile)

#print len(data)
#one frame for each step_k
frame = data[0]
#frame is a dictionary with reasonable keys

close_stats = frame['close_stats']
print close_stats
#print max(worst_case_stats)
#print len(close_stats)

#[step_k * [num_candidate * [k * [worst, actual]]]]