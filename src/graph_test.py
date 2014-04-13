import sys
import json
string = ""
for line in sys.stdin:
    string += line

final_list = json.loads(string)


from pylab import *
for i,data in enumerate(final_list):
    figure()
    plot(range(len(data)), data, 'r')
    xlabel('x')
    ylabel('y')
    ylim([0,data[-1] +1])
    title('title')
    savefig("pagh0.1d0.4/"+str(i+1)+'.eps')


