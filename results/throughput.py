import re
import math
percentage = "40%"
filename1 = "packetloss_10%.txt"
filename2 = "packetloss_10%_client.txt"
file1 = open(filename1,"r") 
file2 = open(filename2,"r") 
f1 = file1.read()
f2 = file2.read()
p = re.compile(r'\d+\.\d+')
time = [float(i) for i in p.findall(f2)]  # Convert strings to float
print(time)

li = []
list = f1.split(",")
for i in range(2):
    li.append(int(list[i]))
list = f2.split (",")
for i in range(2):
    li.append(int(list[i]))
print (li)
x = min(li[0], li[2])
# print(type(x))
# throughput = x / math.floor(time)
# print(throughput)
throughput = 1.2

filename = 'graph.txt'      
file_row = percentage + " ," + str(throughput) + "\n"

# out = open(filename, 'w+')
# #out.write(file_row)
# out.append(file_row)
# out.close()

with open(filename, "a") as out:
    out.write(file_row)