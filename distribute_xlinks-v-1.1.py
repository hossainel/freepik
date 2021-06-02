distx = 10
distx = int(input('x:'))
with open('xlinks.txt','r') as fob:
    y = fob.readlines()
    fob.close()
for i in range(distx):
    with open('%i/xlinks.txt'%i, 'r') as fob:
         y = y + fob.readlines()
         fob.close()

y.sort()
print(len(y),'->',len(set(y)))
with open('arc.txt','w') as fob:
    [fob.write(i) for i in y]
    fob.close()

with open('dx.txt','r') as fob:
    td=set(fob.readlines())
    fob.close()
    
y = set(y)-td
d = len(y)
dx = (d+distx-(d%distx))//(distx+1)
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

for i in range(distx+1):
    if i==distx:
        print('xlinks.txt(%i)'%len(x[i]))
        with open('xlinks.txt', 'w') as fob:
            for j in x[i]: fob.write(j)
            fob.close()
    else:
        print('%i/xlinks.txt(%i)'%(i,len(x[i])))
        with open('%i/xlinks.txt'%i, 'w') as fob:
            for j in x[i]: fob.write(j)
            fob.close()
