from matplotlib import pyplot as plt


filename = input('Please enter input file name')

file = open(filename + ".txt", "r")
li1 = []
li2 = []
str = file.readline()
while(len(str)) :
    xy = str.split(",")
    li1.append(xy[0])
    xy[1] = xy[1][:-1]
    xy[1] = float(xy[1])
    li2.append(xy[1])
    str = file.readline()
    
# print(li1)
# print(li2)

plt.plot(li1, li2)
plt.xlabel("Loss Percentage")
plt.ylabel("Throughput")
plt.title("Throughput VS Loss %")
plt.draw()
plt.savefig(filename+'.png')
plt.show()
