
with open('xlinks.txt','r') as fob:
    y = fob.readlines()
    fob.close()
for i in range(10):
    with open('%i/xlinks.txt'%i, 'r') as fob:
         y = y + fob.readlines()
         fob.close()

y.sort()
print(len(y),'-',len(set(y)))
with open('arc.txt','w') as fob:
    [fob.write(i) for i in y]
    fob.close()
    
y = set(y)
d = len(y)
dx = (d+11-(d%11))//11
print(d,'->',dx)

l=1
lx=0
x = [[],[],[],[],[],[],[],[],[],[],[]]
for i in y:
    x[lx].append(i)
    if l==dx:
        l=1
        lx=lx+1
    else: l=l+1

for i in range(11):
    if i==10:
        print('xlinks.txt(%i)'%len(x[i]))
        with open('xlinks.txt', 'w') as fob:
            for j in x[i]: fob.write(j)
            fob.close()
    else:
        print('%i/xlinks.txt(%i)'%(i,len(x[i])))
        with open('%i/xlinks.txt'%i, 'w') as fob:
            for j in x[i]: fob.write(j)
            fob.close()
