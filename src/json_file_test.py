import json



#k, space, total_input_size, fraction, data_row

#print len(data[0])

def get_data(fname):
    with open(fname, 'r') as datafile:
        data = json.load(datafile)
        ratios = [value['ratios'] for value in data]
        parameters =  [value['parameters'] for value in data]
        tpr = []
        fnr = []
        fpr = []
        tnr = []
        fraction = []
        for k in ratios:

            tpr.append([a[0] for a in k])
            fnr.append([a[1] for a in k])
            fpr.append([a[2] for a in k])
            tnr.append([a[3] for a in k])

        for k in parameters:
            fraction.append([a[3] for a in k])

        return synthesize(fraction,tpr,fnr,fpr,tnr)


def synthesize(fraction,tpr,fnr,fpr,tnr):
    #print fraction
    fraction = [sum(x) / float(len(x)) for x in fraction]
    tpr = [sum(x) / float(len(x)) for x in tpr]
    fnr = [sum(x) / float(len(x)) for x in fnr]
    fpr = [sum(x) / float(len(x)) for x in fpr]
    tnr = [sum(x) / float(len(x)) for x in tnr]

    return fraction,tpr,fnr,fpr,tnr



fraction_1,tpr_1,fnr_1,fpr_1,tnr_1 = get_data("wildcard/harvard_graph_with_wildcards_0.json")

fraction_2,tpr_2,fnr_2,fpr_2,tnr_2 = get_data("wildcard/harvard_graph_with_wildcards_10.json")

fraction_3,tpr_3,fnr_3,fpr_3,tnr_3 = get_data("wildcard/harvard_graph_with_wildcards_100.json")

fraction_4,tpr_4,fnr_4,fpr_4,tnr_4 = get_data("wildcard/harvard_graph_with_wildcards_1000.json")

#fraction, tpr, fnr, fpr, tnr = synthesize(fraction, tpr, fnr, fpr, tnr)

#print data

from pylab import *
# figure(0)
# plot(fraction, tpr, 'k')
# xlabel('Fraction')
# ylabel('TPR')
# ylim(0,1)
# title('True positive rate')
# savefig('TPR1.eps')

figure(1)
a, = plot(fraction_1, fpr_1, 'k')
#b, = plot(fraction_2, fpr_2, 'r--')
#c, = plot(fraction_3, fpr_3, 'b')
d, = plot(fraction_4, fpr_4, 'r--')
legend([a,d], ['0', '1000'])
xlabel('Fraction')
ylabel('FPR')
ylim(0,0.030)
title('False positive rate')
savefig('FPR1.eps')
show()


# figure(2)
# plot(fraction, tnr, 'k', fraction, tnr1, 'r')
# xlabel('k')
# ylabel('TNR')
# ylim(0)
# title('True negative rate')
# savefig('TNR1.eps')

# figure(3)
# plot(fraction, fnr, 'k', fraction, fnr1, 'r')
# xlabel('k')
# ylabel('FNR')
# ylim(0)
# title('False negative rate')
# savefig('FNR1.eps')


