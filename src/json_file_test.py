import json

data = []
with open('harvard_graph.json', 'r') as datafile:
    data = json.load(datafile)

k   = [value[0] for value in data]
tpr = [value[1][0] for value in data]
fnr = [value[1][1] for value in data]
fpr = [value[1][2] for value in data]
tnr = [value[1][3] for value in data]

print data

from pylab import *
figure(0)
plot(k, tpr, 'k')
xlabel('k')
ylabel('TPR')
title('True positive rate')
savefig('TPR1.eps')

figure(1)
plot(k, fpr, 'k')
xlabel('k')
ylabel('FPR')
title('False positive rate')
savefig('FPR1.eps')

figure(2)
plot(k, tnr, 'k')
xlabel('k')
ylabel('TNR')
title('True negative rate')
savefig('TNR1.eps')

figure(3)
plot(k, fnr, 'k')
xlabel('k')
ylabel('FNR')
title('False negative rate')
savefig('FNR1.eps')

show()
