import json

data = []
with open('harvard_graph.json', 'r') as datafile:
    data = json.load(datafile)

print [value[0] for value in data]
print [value[1] for value in data]
print [value[2] for value in data]
print [value[3] for value in data]
print [value[4] for value in data]

k   = [value[0] for value in data]
tpr = [value[1] for value in data]
fnr = [value[2] for value in data]
fpr = [value[3] for value in data]
tnr = [value[4] for value in data]

print data

from pylab import *
figure(0)
plot(k, tpr, 'r')
xlabel('k')
ylabel('TPR')
title('True positive rate')

figure(1)
plot(k, fpr, 'r')
xlabel('k')
ylabel('FPR')
title('False positive rate')

figure(2)
plot(k, tnr, 'r')
xlabel('k')
ylabel('TNR')
title('True negative rate')

figure(3)
plot(k, fnr, 'r')
xlabel('k')
ylabel('FNR')
title('False negative rate')

show()