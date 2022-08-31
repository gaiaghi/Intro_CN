import math

r = 1   # raggio
n = 6   # numero di lati del poligono

l = 1   # lunghezza del lato del poligono

for i in range(1,15):
    '''poligono inscritto'''
    #lato b dello schema 1
    b = l/2 
    # calcolo dell'altezza del triangolo con base = lato del 
    # poligono e vertice opposto = centro del cerchio
    h = math.sqrt(1 - (l / 2)**2 )
    
    #calcolo dell'area del poligono = limite inferiore di pi
    l_inf = n * (l * h) / 2
    
    '''poligono circoscritto'''
    h1 = r          # altezza
    rapp = h1 / h   # rapporto dei lati dei triangoli simili
    b1 = rapp * b   # lato b' dello schema 2
    l1 = 2 * b1     # lato del poligono circoscritto
    l_sup = n * (l1 * h1) / 2
    
    '''poligono successivo'''
    n = 2 * n   # raddoppiano i lati del poligono regolare
    d = r - h   # lato d dello schema 1
    l = math.sqrt(d**2 + b**2) # lunghezza del lato
    
    print("%5d - %.16f %.16f" %(n, l_inf, l_sup))