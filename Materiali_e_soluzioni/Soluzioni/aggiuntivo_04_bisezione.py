"""
Metodo di bisezione per la ricerca delle radici di una funzione.
"""

# definizione di funzione di cui cercare le radici.
def f(x): return x**3-x-2
 
 
"""
metodo di bisezione: 
    f = funzione
    a = estremo inferiore dell'intervallo
    b = estremo superiore dell'intervallo
    n = numeri di passi da eseguire per approssimare la radice della funzione
"""
def bisezione(f, a, b, n):
 
    m = (a+b)/2 #
    fa = f(a) # valutazione della funzione nel punto a
    fm = f(m) # valutazione della funzione nel punto m
    fb = f(b) # valutazione della funzione nel punto b  
    print("\t[a, \t m,\t b] \t\t f(a) \t f(m)) \t f(b)")
    print("%10.6f %10.6f %10.6f %10.6f %10.6f %10.6f" %(a,m,b, fa,fm,fb))
    
    for i in range(5):
        if(fm == 0): # soluzione esatta trovata
            print("Radice trovata!")
            break
        # scelgo il sotto-invervallo giusto
        elif(fb*fm > 0): 
            b = m
            m = (a+b)/2
            fb = f(b)
            fm = f(m) 
        elif(fa*fm > 0):
            a = m
            m = (a+b)/2
            fa = f(a)
            fm = f(m)
            
        else:
            print("Errore")
            break
        print("%10.6f %10.6f %10.6f %10.6f %10.6f %10.6f" %(a,m,b, fa,fm,fb))
    return m
        
        
if __name__ == "__main__":
    
    print("\nLa soluzione è", bisezione(f, 1, 2, 10))