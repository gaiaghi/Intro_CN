
def riemann(a, b, c, x1, x2, n):
    """
    a, b, c: coefficienti dell'equazione di secondo grado
    x1: estremo sx dell'integrale
    x2: estremo dx dell'integrale
    n: numero di intervalli 
    """
    
    # controllo sul numero di intervalli: deve essere >0
    if (n<1) :
        n = 1
    
    # larghezza degli intervalli = base dei rettangoli
    base = (abs(x1 - x2)) / n
    
    # inizio dell'intervallo corrente
    x = x1
    #sommatore per l'area
    area = 0
    
    #per ogni intervallo
    for _ in range(n):
        #punto medio
        m = x + base / 2
        #altezza
        h = a * m**2 + b * m + c
        
        # sommo le aree
        area = area + base * h
        #passo al prossimo intervallo
        x += base
    
    return area

if __name__ == "__main__":
    print("METODO DEI RETTANGOLI PER IL CALCOLO DEGLI INTEGRALI DEFINITI \n")
    par = input("Inserire i parametri dell'equazione di secondo grado, separati da virgola: ")
    par = tuple(map(int, par.replace(" ","").split(",")))
    
    est = input("Inserire gli estremi dell'integrale, separati da virgola: ")
    est = tuple(map(int, est.replace(" ", "").split(",")))    
    
    while True:
        num = int(input("Inserire il numero di intervalli di suddivione: "))
        if num < 1:
            print("Valore non valido. Gli intervalli devono essere maggiori di 1.")
            continue
        else:
            break
    
    
    print(riemann(par[0], par[1], par[2], est[0], est[1], num))
    #print(riemann(-1,4,-3,-1,3,1000))
        