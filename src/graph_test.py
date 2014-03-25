import sys
import json
string = ""
for line in sys.stdin:
    string += line



data = json.loads(string)


from pylab import *
figure()
plot(range(len(data)), data, 'r')
xlabel('x')
ylabel('y')
ylim([0,data[-1] +1])
title('title')
show()
