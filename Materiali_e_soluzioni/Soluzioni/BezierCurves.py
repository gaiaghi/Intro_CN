from tkinter import Tk, Canvas, mainloop, Frame
import math
import random

WIDTH = 1000
HEIGHT = 600
TIME_INT = .005

IS_UP = 1
IS_DOWN = 0
state = IS_UP
movingPoint = None
RADIUS = 5


class Curva_Bezier():
    nodes = []  # lista dei punti in cui l'utente ha cliccato = nodi di controllo
    points = [] # lista dei punti della curva di bezier
    linePoints = [] # lista per la creazione dell'animazione
    n_seg = 60  # numero di segmenti per disegnare bezier
    animate = False
    t_animate = 0
    colors = [] # lista di colori per la poligonale di controllo nell'animazioe
    colorsCtrl = [] # lista di colori per le rette intermedie nell'animazione
    switch_canvas = None
    repeat = None

    def __init__(self):
        self.window = Tk()
        self.window.title("Curve di Bezier")
        self.window.resizable(width=False, height=False)

        self.frame = Frame(self.window, width=WIDTH, height=HEIGHT, highlightthickness=0, bg="#303030")
        self.frame.pack()

        self.canvas = Canvas(self.frame, width=WIDTH, height=HEIGHT, highlightthickness=0, bg="#303030")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.focus_set()
        # eventi di click dei tasti destro e sinistro:
        self.canvas.bind("<Button-3>", self.clickDX)
        self.canvas.bind("<Button-1>", self.clickSX)
        # evento rilascio tasto sinistro
        self.canvas.bind("<ButtonRelease-1>", self.releaseCallback)
        # evento tasto sinistro cliccato e in movimento
        self.canvas.bind("<B1-Motion>", self.movingCallback)
        # evento tastiera
        self.canvas.bind("<Key>", self.keyboardCallback)

        # canvas per l'animazione
        self.animate_canvas = Canvas(self.frame, width=WIDTH, height=HEIGHT, highlightthickness=0, bg="#303030")
        self.animate_canvas.focus_set()
        self.animate_canvas.bind("<Key>", self.keyboardCallback)

        # self.animate()
        mainloop()  # mostra la finestra


    """Metodo callback dell'evento click tasto sx del mouse.
        Se la posizione del mouse è vicina ad un punto esistente: 
            -> si più modificare la posizione del punto tenendo cliccato e muovendo il mouse
        Se non ci sono punti esistenti vicini:
            -> si aggiunge un nuovo punto
    """
    def clickSX(self, event):
        global state, movingPoint

        clickedPoint = (event.x, event.y)

        if self.findNearbyPoint(clickedPoint) is not None:
            state = IS_DOWN
            movingPoint = self.findNearbyPoint(clickedPoint)
            self.movingCallback(event)

        else:
            movingPoint = None
            self.nodes.append(clickedPoint)  # aggiungo il punto
            del self.colors[:]
            for _ in range(len(self.nodes)):
                self.colors.append(self.random_color())

        self.render()


    """Metodo callback dell'evento click tasto sx del mouse rilasciato"""
    def releaseCallback(self, event):
        global state
        state = IS_UP


    """
    Metodo callback dell'evento tasto sx del mouse cliccato e in movimento.
        Aggiorna la posizione dei punti esistenti che si vogliono modificare.
    """
    def movingCallback(self, event):
        global state
        if state is IS_DOWN:
            self.nodes[movingPoint] = (event.x, event.y)

        self.render()


    """Metodo callback dell'evento click tasto dx del mouse"""
    def clickDX(self, event):
        if len(self.nodes) > 0:
            # cerco se c'è un punto vicino
            delPoint = self.findNearbyPoint((event.x, event.y))

            # se c'è un punto vicino lo rimuovo (altrimenti non faccio niente)
            if delPoint is not None:
                del self.nodes[delPoint]
        self.render()


    """Metodo callback per la gestione dei tasti della tastiera"""
    def keyboardCallback(self, event):
        if event.char == "c":
            del self.points[:]
            del self.nodes[:]
            del self.colors[:]
            self.canvas.delete("all")

        elif event.char == "q":
            self.canvas.quit()

        elif event.char == "a":
            self.canvas.pack_forget()
            self.animate = not self.animate
            if self.animate:
                self.switch_canvas = self.canvas
                self.canvas = self.animate_canvas
                self.canvas.pack()
                self.colorsCtrl = [self.random_color() for _ in range(len(self.nodes) - 1)]
                self.animate_render()
            else:
                self.canvas = self.switch_canvas
                self.switch_canvas = None
                self.canvas.pack()
                self.canvas.update()
                self.render()


    """Metodo che calcola, se presente, il punto più vicino alla posizione in cui si trova il click del mouse sx"""
    def findNearbyPoint(self, point):
        closest = None
        # per ogni punto della curva...
        for i in range(len(self.nodes)):
            # calcolo la distanza tra i due punti
            distanza = math.sqrt(pow(point[0] - self.nodes[i][0], 2) + pow(point[1] - self.nodes[i][1], 2))
            if distanza < RADIUS + 2:
                closest = i

        return closest


    """Metodo per disegnare e aggiornare la scena"""
    def render(self):
        self.canvas.delete("all")
        # disegno i punti di controllo
        for p in self.nodes:
            self.draw_point(p)

        # disegno statico della curva e del poligono di controllo
        if len(self.nodes) > 1:
            # disegno il poligono di controllo
            for i in range(len(self.nodes) - 1):
                self.draw_line(self.nodes[i], self.nodes[i + 1], dash=(4, 4))

            for i in range(self.n_seg):
                self.points.append(self.deCasteljau(i / self.n_seg))
        for i in range(len(self.points) - 1):
            self.draw_line(self.points[i], self.points[i + 1], width=2, color="#8AAAE5")
        self.points = []


    def animate_render(self):
        self.canvas.delete("all")
        # disegno i punti di controllo
        for p in self.nodes:
            self.draw_point(p)

        # animazione della creazione della curva
        if self.animate and len(self.nodes) > 0:
            self.t_animate += TIME_INT
            # controllo il valore t per l'interpolazione
            if self.t_animate > 1:
                self.t_animate = 0

            if len(self.nodes) > 1:
                # disegno il poligono di controllo
                for i in range(len(self.nodes) - 1):
                    self.draw_line(self.nodes[i], self.nodes[i + 1], color=self.colorsCtrl[-1])

                # calcolo dei punti per la curva di bezier
                for i in range(self.n_seg):
                    self.points.append(self.deCasteljau(i / self.n_seg))

            tPerc = self.t_animate * 100
            endPoint = round(len(self.points) * tPerc / 100)
            self.draw_point(self.points[endPoint-1])

            #curva di bezier
            for i in range(endPoint - 1):
                self.draw_line(self.points[i], self.points[i + 1], color="white", width=2)


            pointsOnLine = [[] for _ in range (len(self.nodes))]
            pointsOnLine[0] = self.nodes
            for i in range(1,len( self.nodes)):  # indice delle iterazioni
                for w in range(len(self.nodes) - i):  # w = indice dei punti
                    a = pointsOnLine[i-1][w]
                    b = pointsOnLine[i-1][w+1]
                    # P(t) = (1-t)*A + t*B
                    pointsOnLine[i].append(((1 - self.t_animate) * a[0] + self.t_animate * b[0],
                                            (1 - self.t_animate) * a[1] + self.t_animate * b[1]))
                    #punti che si muovono sulle rette intermedie
                    self.draw_point(pointsOnLine[i][-1], radius=RADIUS - 1 if RADIUS - 2 > 0 else RADIUS,
                                    color=self.colorsCtrl[i-1])
                #rette intermedie
                for v in range(len(pointsOnLine[i])-1):
                    self.draw_line(pointsOnLine[i][v], pointsOnLine[i][v+1], color=self.colorsCtrl[i-1])

            self.points = []
            self.repeat = self.canvas.after(int(TIME_INT * 1000), self.animate_render)


    """Algoritmo di de Casteljau"""
    def deCasteljau(self, t):
        # copio le coordinate dei punti per usarli nel calcolo delle Lerp
        xs = [p[0] for p in self.nodes]
        ys = [p[1] for p in self.nodes]

        for i in range(1, len(self.nodes)):  # indice delle iterazioni
            for w in range(len(self.nodes) - i):  # w = indice dei punti
                xs[w] = (1 - t) * xs[w] + t * xs[w + 1]  # lerp sulla coordinata x
                ys[w] = (1 - t) * ys[w] + t * ys[w + 1]  # lerp sulla coordinata y
        point = (xs[0], ys[0])
        return point


    """Metodo per disegnare i punti
        input:
    """
    def draw_point(self, point, radius=RADIUS, color="white"):
        return self.canvas.create_oval(point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius,
                                       fill=color)


    """Metodo per disegnare le rette del poligono di controllo
        input:
    """
    def draw_line(self, p0, p1, color="white", width=1, dash=(0, 0)):
        if dash != (0, 0):
            line = self.canvas.create_line(p0[0], p0[1], p1[0], p1[1], dash=dash, fill=color, width=width)
        else:
            line = self.canvas.create_line(p0[0], p0[1], p1[0], p1[1], fill=color, width=width)

        return line


    @staticmethod
    def random_color() -> str:
        return "#%02x%02x%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


if __name__ == "__main__":
    Curva_Bezier()
