"""
    Implementazione di un semplice algoritmo che calcola le coordinate pixel
    di rasterizzazione di linee con estremi a e b.
    Ovvero: il codice risolve l'equazione della retta passante per i punti 
    a = (x1, y1) e b = (x2, y2), nei valori di ascissa compresi tra x1 ed x2,
    arrotondando il risultato dell'ordinata ad un numero intero.
"""

#primo punto
a = (2, 7)
#secondo punto 
b = (18, 14)

#calcolo del coefficiente angolare 
m = (a[1] - b[1]) / (a[0] - b[0])
#calcolo dell'ordinata allìorigine
q = a[1] - m * a[0]

#per ogni valore delle ascisse tra i due punti estremi della retta
for x in range(min(a[0], b[0]), max(a[0],b[0])+1):
    #calcolo dell'ordinata, arrotondata a numero intero
    y = round(m * x + q)
    print("("+ str(x) +","+ str(y) +")")