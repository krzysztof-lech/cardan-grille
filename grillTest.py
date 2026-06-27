from grillCardana import generacjaKarty, encrypt, decrypt, atakPop

with open('tj.txt', 'r') as file:
    tj = file.read()
    file.close()
tj = tj.replace(" ","").replace(".","").replace(",","").replace("!","").replace("?","").replace("'","").replace("-","")
tj = tj.upper()

bokKarty=5

key0, karta0, elementy0=generacjaKarty(bokKarty)

print( 'uzyta karta =')
for i in range(0,len(karta0)):
    print( karta0[i])
print('użyty klucz = ', key0 )


kt = encrypt( tj, key0 )

rozmPop = 10000
print('rozmPop = ', rozmPop)

bestkey = atakPop( kt, bokKarty, rozmPop )
print( '\nobliczony klucz',bestkey,'\n', decrypt( kt, bestkey ) )

print('użyty klucz = ', key0 )
