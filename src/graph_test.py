import sys
import json
string = ""
for line in sys.stdin:
    string += line

final_list = json.loads(string)

trues, falses = final_list


from pylab import *

figure()
plot(range(len(trues)), trues, 'r')
xlabel('x')
ylabel('y')
ylim([0,trues[-1] +1])

plot(range(len(falses)), falses, 'b')

t = [7] * len(falses)

plot(range(len(falses)), t, 'y')



title('title')
show()
#savefig("pagh0.1d0.4/"+str(i+1)+'.eps')


