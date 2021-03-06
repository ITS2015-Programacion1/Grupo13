import pilasengine
import sys
import random

pilas = pilasengine.iniciar()





fondo = pilas.fondos.Fondo()
fondo.imagen = pilas.imagenes.cargar('imagenes/images.jpeg')

fondo.imagen.repetir_vertical = True
fondo.imagen.repetir_horizontal = True


def iniciar_juego():


    menu.eliminar()

    fondo = pilas.fondos.Fondo()
    fondo.imagen = pilas.imagenes.cargar('imagenes/Regal_Blue_Skulls.jpg')
 
        
 
    class MiProtagonista(pilasengine.actores.Actor):

        def iniciar(self):
            self.imagen = "imagenes/baby.png"
            self.escala = 0.175
            self.x = -250


        def actualizar(self):

            if pilas.control.izquierda:
                self.x -= 6

            if pilas.control.derecha:
                self.x += 6

            if pilas.control.arriba:
                self.y += 6

            if pilas.control.abajo:
                self.y -= 6


    pilas.actores.vincular(MiProtagonista)
    protagonista = pilas.actores.MiProtagonista()
    protagonista.aprender(pilas.habilidades.LimitadoABordesDePantalla)
    protagonista.radio_de_colision= 20


    puntos = pilas.actores.Puntaje(x=230, y=200, color=pilas.colores.blanco)
    puntos.magnitud = 40


    class Estrellita(pilasengine.actores.Estrella):

        def iniciar(self):
            pilasengine.actores.Estrella.iniciar(self)
            self.escala = 0.4
            self.x = pilas.azar(-280, 280)
            self.y = pilas.azar(-250, 250)
            self.radio_de_colision= 20

        def actualizar(self):
            self.rotacion += 5

    estrellas = []

    def crear_estrella():
        estrella = Estrellita(pilas)
        estrellas.append(estrella)
        return True


    pilas.tareas.agregar(1.0, crear_estrella)
    

    def cuanto_toca_estrella(protagonista, estrella):
        estrella.eliminar()
        puntos.aumentar(5)

    pilas.colisiones.agregar(protagonista, estrellas, cuanto_toca_estrella)



    class Enemigo(pilasengine.actores.Bomba):

        def iniciar(self):
            pilasengine.actores.Bomba.iniciar(self)
            self.aprender( pilas.habilidades.PuedeExplotar )
            self.escala = 0.75
            self.x = 290
            self.y = pilas.azar(-200, 200)
            self.velocidad = pilas.azar(30, 70) / 4.0
            self.radio_de_colision= 20

        def actualizar(self):
            self.rotacion += 7
            self.x -= self.velocidad

    enemigos = []
    

    def crear_enemigo():
        un_enemigo = Enemigo(pilas)
        enemigos.append(un_enemigo)
        return True


    pilas.tareas.agregar(1.0, crear_enemigo)
    

    def cuanto_toca_enemigo(protagonista, enemigo):
        protagonista.eliminar()
        enemigo.eliminar()
        pilas.avisar("perdiste.")
        archivo = open('puntaje.txt', 'a')
        archivo.write('Puntaje = %d puntos' %(puntos.obtener()))

    pilas.colisiones.agregar(protagonista, enemigos, cuanto_toca_enemigo)


    pilas.avisar('Cuidado con las bombas')



def cj():

    menu.eliminar()

    texto = pilas.actores.Texto("Muevete con las flechas del teclado", y = 100)
    texto.color = pilas.colores.rojo

    rectangulo = pilas.fisica.Rectangulo(0, 0, 450, 40, sensor=True, dinamica=False)
    texto.figura_de_colision = rectangulo


    class Ejemplo(pilasengine.actores.Actor):

        def iniciar(self):
            self.imagen = "imagenes/baby.png"
            self.escala = 0.25
            self.radio_de_colision = 30
            self.texto = None

        def actualizar(self):

            if pilas.control.izquierda:
                self.x -= 7

            if pilas.control.derecha:
                self.x += 7

            if pilas.control.arriba:
                self.y += 7

            if pilas.control.abajo:
                self.y -= 7


            if self.x > 350:
                self.x = -350

            if self.x < -350:
                self.x = 350

            if self.y > 300:
                self.y = -300

            if self.y < -300:
                self.y = 300


    pilas.actores.vincular(Ejemplo)
    protagonista = pilas.actores.Ejemplo()

    def toca_texto(protagonista, texto):
        texto.eliminar()

    pilas.colisiones.agregar(protagonista, texto, toca_texto)        
        




def salir_del_juego():
    sys.exit()






menu = pilas.actores.Menu(
        [
            ('Iniciar Juego', iniciar_juego),
            ('Como jugar', cj),
            ('Salir', salir_del_juego),
        ])





pilas.ejecutar()
