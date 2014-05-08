import json
import math
#data looks like: (k, space, total_input_size, fraction, data_row)
def avg(l):
    return sum(l) / float(len(l))

data = []
with open('wildcard/work_over_wildcards_101.json', 'r') as datafile:
    data = json.load(datafile)

#print len(data)
#one frame for each step_w
frame = data[7]
#frame is a dictionary with reasonable keys
k, space, total_input_size, fraction, l, k, n, l_prime, number_of_candidates = frame['parameters']
print l_prime, l, k


#print close_stats
#print len(close_stats), "should be 1000 (number of candidates)"
#print len(close_stats[0]), "should be 10, 20 or 30 (W)"
#print len(close_stats[0][0]), "should be 2, (worst_case, actual)"

x = []
y_naive_worst = []
y_naive_worst_log = []
y_close_smart_worst = []
y_close_smart_worst_log =[]
y_close_smart_actual = []
y_close_smart_actual_log = []

y_far_smart_worst = []
y_far_smart_worst_log =[]
y_far_smart_actual = []
y_far_smart_actual_log = []

for frame in data:
    close_worst_sum = []
    close_worst_max = []
    close_worst_avg = []
    close_actual_sum = []
    close_actual_max = []
    close_actual_avg = []

    far_worst_sum = []
    far_worst_max = []
    far_worst_avg = []
    far_actual_sum = []
    far_actual_max = []
    far_actual_avg = []

    close_stats = frame['close_stats']
    far_stats = frame['far_stats']
    for i in range(len(close_stats)):
        far_stats_for_candidate = far_stats[i]#close_stats[i]
        close_stats_for_candidate = close_stats[i]
        #print stats_for_candidate
        
        worst_list = [worst for worst, actual in close_stats_for_candidate]
        actual_list = [actual for (worst, actual) in close_stats_for_candidate]

        close_worst_sum.append(sum(worst_list))
        close_worst_max.append(max(worst_list))
        close_worst_avg.append(avg(worst_list))
        
        close_actual_sum.append(sum(actual_list))
        close_actual_max.append(max(actual_list))
        close_actual_avg.append(avg(actual_list))

        worst_list = [worst for worst, actual in far_stats_for_candidate]
        actual_list = [actual for (worst, actual) in far_stats_for_candidate]

        far_worst_sum.append(sum(worst_list))
        far_worst_max.append(max(worst_list))
        far_worst_avg.append(avg(worst_list))
        
        far_actual_sum.append(sum(actual_list))
        far_actual_max.append(max(actual_list))
        far_actual_avg.append(avg(actual_list))
        #contains 1000 integers, one for each candidate
        

    #create 3 data points from this
    w = len(frame['wildcards'])
    x.append(w)
    y_naive_worst_log.append(math.log(2 ** w, 2))

    y_close_smart_worst_log.append(math.log(avg(close_worst_max), 2))
    y_close_smart_actual_log.append(math.log(avg(close_actual_max), 2))

    y_far_smart_worst_log.append(math.log(avg(far_worst_max), 2))
    y_far_smart_actual_log.append(math.log(avg(far_actual_max), 2))

    y_naive_worst.append(2 ** w)

    y_close_smart_worst.append(avg(close_worst_max))
    y_close_smart_actual.append(avg(close_actual_max))

    y_far_smart_worst.append(avg(far_worst_max))
    y_far_smart_actual.append(avg(far_actual_max))

#plot that thing
#print y_smart_actual

#convert x to fraction
print x
x = [val / 100.0 for val in x]
print x

from pylab import *

figure(0)
yscale('log')
b, = plot(x, y_close_smart_worst, 'r')
c, = plot(x, y_close_smart_actual, 'k--')
#d, = plot(x, y_far_smart_worst, 'g')
#e, = plot(x, y_far_smart_actual_log, 'k:')

legend([b,c], ['no short-circuit', 'short-circuit'], loc='best')
title('Wildcard query performance - Effects of short-circuiting')
xlabel('Fraction of wildcarded bits')
ylabel('# of sub-queries')

savefig('work_over_wildcards_short-circuit.eps')
show()


figure(1)
yscale('log')
a, = plot(x, y_naive_worst, 'r')
b, = plot(x, y_close_smart_worst, 'k--')
#c, = plot(x, y_close_smart_actual_log, 'k--')
#d, = plot(x, y_far_smart_worst, 'g')
#e, = plot(x, y_far_smart_actual_log, 'k:')
legend([a,b], ['Naive', 'Improved'], loc='best')
xlabel('Fraction of wildcarded bits')
ylabel('# of sub-queries')
#ylim(0,0.030)
title('Wildcard query performance - Effects of Improving approach 2')
savefig('work_over_wildcards_approaches.eps')
show()