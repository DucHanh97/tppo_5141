f = open('test.txt', 'r')
l1 = f.readline()
l2 = f.readline()
l3 = f.readline()
f.close
for i in range(len(l1)):
    if l1[i] == '=':
        s1 = int(l1[i+1:])
for i in range(len(l2)):
    if l2[i] == '=':
        s2 = int(l2[i+1:])

for i in range(len(l3)):
    if l3[i] == '=':
        s3 = int(l3[i+1:])

print(s1)
print(s2)
print(s3)