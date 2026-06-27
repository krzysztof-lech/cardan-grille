from grillCardana import decrypt, atakPop

bokKarty=5


rozmPop = 10000
print('rozmPop = ', rozmPop)

with open('kt.txt', 'r') as file:
    kt = file.read()
    file.close()

bestkey = atakPop( kt, bokKarty, rozmPop )
dt=decrypt( kt, bestkey )
print( '\nobliczony klucz',bestkey,'\n', dt )

with open('dt.txt', 'w') as file:
    file.write(dt)
    file.close()

with open('dt_klucz.txt', 'w') as file:
    file.write(str(bestkey))
    file.close()

