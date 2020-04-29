import re
import math

loss_percentage = input('Please enter packet loss percentage')

percentage = loss_percentage
filename1 = "packetloss_"+loss_percentage+".txt"
filename2 = "packetloss_"+loss_percentage+"_client.txt"
file1 = open(filename1,"r") 
file2 = open(filename2,"r") 
f1 = file1.read()
f2 = file2.read()
p = re.compile(r'\d+\.\d+')
time = [float(i) for i in p.findall(f2)]  # Convert strings to float
print('Time for which client executed:',time)

li = []
list = f1.split(",")
for i in range(2):
    li.append(int(list[i]))
list = f2.split (",")
for i in range(2):
    li.append(int(list[i]))
print ('Server received,sent ; Client recvd,sent in order',li)
x1 = min(li[0], li[3])
x2 = min(li[1],li[2])
print('Total packets across network:',x1+x2)

throughput = ((x1+x2) / (time[0]))
print('Throughput',throughput)
#throughput = 1.2

filename = 'graph.txt'      
file_row = percentage + " ," + str(throughput) + "\n"

# out = open(filename, 'w+')
# #out.write(file_row)
# out.append(file_row)
# out.close()

with open(filename, "a") as out:
    out.write(file_row)
