from grillCardana import generacjaKarty, encrypt

with open('tj.txt', 'r') as file:
    tj = file.read()
    file.close()
tj = tj.replace(" ","").replace(".","").replace(",","").replace("!","").replace("?","").replace("'","").replace("-","").replace("\n","")
tj = tj.upper()

bokKarty=5

key0, karta0,elementy0=generacjaKarty(bokKarty)

print( 'uzyta karta =')
for i in range(0,len(karta0)):
    print( karta0[i])
print('użyty klucz = ', key0 )


kt = encrypt( tj, key0 )

with open('kt.txt', 'w') as file:
    file.write(kt)
    file.close()

with open('kt_klucz.txt', 'w') as file:
    for i in range(0,len(karta0)):
        file.write( str(karta0[i]))
        file.write("\n")
    file.write(str(key0))
    file.close()



