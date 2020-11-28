from random import randint
disk = 100000
config = [[],[],[]]
for i in range(disk):
    config[randint(0, disk)%3].append(i)

config[0].sort(reverse = True)
config[1].sort(reverse = True)
config[2].sort(reverse = True)
if randint(0,disk)%2 == 0:
    print('A*')
else:
    print("IDA*")
print(randint(0,200))
print(disk)
dest = randint(0,disk)%3
if dest == 0:
    print('A')
elif dest == 1:
    print('B')
else:
    print('C')
if len(config[0]):
    for i in range(0, len(config[0])):
        if i != len(config[0])-1:
            print(config[0][i],end="")
            print(',', end="")
        else:
            print(config[0][i])
if len(config[1]):
    for i in range(0, len(config[1])):
        if i != len(config[1])-1:
            print(config[1][i],end="")
            print(',', end="")
        else:
            print(config[1][i])
if len(config[2]):
    for i in range(0, len(config[2])):
        if i != len(config[2])-1:
            print(config[2][i],end="")
            print(',', end="")
        else:
            print(config[2][i])

    '''
    for i in state[GOALINDEX]:
        found = False
        for j in state[prevIndex]:
            if found:
                break
            if i < j:
                y += 1
                found = True
        for j in state[nextIndex]:
            if found:
                break
            if i < j:
                y += 1
                found = True
    '''