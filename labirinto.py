from tkinter import *
from PIL import ImageTk, Image
import time

class DoublyLinkedStack:
    class Node:
        def __init__(self, data, next=None, prev=None):
            self.data = data
            self.next = next
            self.prev = prev

    def __init__(self):
        self.top = None
        self.bottom = None
        self.size = 0

    def is_empty(self):
        return self.size == 0

    def printstack(self):
        no = self.top
        temp = []
        while no is not None:
            temp.append(no.data)
            no = no.prev
            return temp

        return temp

    def peek(self):
        if self.is_empty():
            return None
        return self.top.data

    def push(self, data):
        new_node = self.Node(data, next=self.top)
        if self.is_empty():
            self.bottom = new_node
        else:
            self.top.prev = new_node
        self.top = new_node
        self.size += 1

    def pop(self):
        if self.is_empty():
            return None
        data = self.top.data
        self.top = self.top.next
        if self.top is not None:
            self.top.prev = None
        else:
            self.bottom = None
        self.size -= 1
        return data


class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.start = self.find_start()
        self.end = self.find_end()
        self.stack = DoublyLinkedStack()
        self.stack.push((self.start, [self.start]))

    def find_start(self):
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                if self.maze[row][col] == "M":
                    return row, col
        return None

    def find_end(self):
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                if self.maze[row][col] == "E":
                    return row, col
        return None

    def is_valid_position(self, pos_r, pos_c):
        if pos_r < 0 or pos_c < 0:
            return False
        if pos_r >= len(self.maze) or pos_c >= len(self.maze[0]):
            return False
        if self.maze[pos_r][pos_c] in ".1":
            return False
        return True

    def print_maze(self):
        for row in self.maze:
            for item in row:
                print(item, end="")
            print()

    def exit_maze(self):

        while True:
            pos, path = self.stack.pop()
            pos_r, pos_c = pos
            if pos == self.find_end():
                print("Alcançou o objetivo")
                self.maze[pos_r][pos_c] = "X"
                self.print_maze()
                print(path)
                return path

            if self.is_valid_position(pos_r + 1, pos_c):
                self.stack.push(((pos_r + 1, pos_c), path + [(pos_r + 1, pos_c)]))
            if self.is_valid_position(pos_r, pos_c - 1):
                self.stack.push(((pos_r, pos_c - 1), path + [(pos_r, pos_c - 1)]))
            if self.is_valid_position(pos_r - 1, pos_c):
                self.stack.push(((pos_r - 1, pos_c), path + [(pos_r - 1, pos_c)]))
            if self.is_valid_position(pos_r, pos_c + 1):
                self.stack.push(((pos_r, pos_c + 1), path + [(pos_r, pos_c + 1)]))
            self.maze[pos_r][pos_c] = "."


maze = [
    ["1", "1", "1", "M", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "0", "1", "0", "0", "0", "0", "0", "1", "0", "0", "0", "1"],
    ["1", "0", "1", "0", "0", "1", "1", "0", "0", "0", "1", "0", "1"],
    ["1", "0", "1", "0", "0", "1", "1", "0", "1", "1", "1", "0", "1"],
    ["1", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "1"],
    ["1", "0", "1", "0", "1", "1", "1", "1", "1", "0", "1", "0", "1"],
    ["1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "1"],
    ["1", "0", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "0", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
    ["1", "0", "1", "0", "0", "0", "0", "0", "1", "0", "0", "0", "1"],
    ["1", "0", "1", "0", "0", "1", "1", "0", "0", "0", "1", "0", "1"],
    ["1", "0", "1", "0", "0", "1", "1", "0", "1", "1", "1", "0", "1"],
    ["1", "0", "0", "0", "0", "0", "0", "0", "1", "0", "0", "0", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "0", "1", "0", "1"],
    ["1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "1", "0", "1"],
    ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "E", "1"],
]

labirinto = MazeSolver(maze)

# pegar apenas a linha e a coluna de onde o rato está
posRatoY = labirinto.find_start()[0]
posRatoX = labirinto.find_start()[1]

# pegando a posicao de onde o rato e queijo estão para multiplicar por 40 para obter a coordenada correta
posicaoRatoY = (labirinto.find_start()[0]) * 40
posicaoRatoX = (labirinto.find_start()[1]) * 40
posicaoQueijoY = (labirinto.find_end()[0]) * 40
posicaoQueijoX = (labirinto.find_end()[1]) * 40

labirintoSaida = labirinto.exit_maze()


class Rato:
    def __init__(self, cordX, cordY, imageRato, canvas):
        self.cordX = cordX
        self.cordY = cordY
        self.imageRato = imageRato
        self.canvas = canvas

        RatoEnv = self.canvas.create_image(
            self.cordX, self.cordY, image=self.imageRato, anchor=NW
        )

        self.image = RatoEnv


class App(object):
    def __init__(self, app, maze, **kwargs):
        self.maze = maze
        self.app = app
        self.canvas = Canvas(self.app, width=842, height=842)
        self.canvas.pack()

        global imageRato
        global imageQueijo

        imageRato = ImageTk.PhotoImage(Image.open("rato.png").resize((30, 30)))
        imageQueijo = ImageTk.PhotoImage(Image.open("queijo.png").resize((30, 30)))

        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                if self.maze[row][col] == "1":
                    self.canvas.create_rectangle(
                        col * 40, row * 40, (col + 1) * 40, (row + 1) * 40, fill="black"
                    )
                else:
                    pass

        rato = Rato(posicaoRatoX, posicaoRatoY, imageRato, self.canvas)
        queijo = self.canvas.create_image(
            posicaoQueijoX, posicaoQueijoY, image=imageQueijo, anchor=NW
        )
        posicaoInicial = labirintoSaida[0]
        posicaoInicialX = posicaoInicial[1]
        posicaoInicialY = posicaoInicial[0]

        size = len(labirintoSaida)

        for index in range(1, size):
            posicao = labirintoSaida[index]
            posicaoY = posicao[0]
            posicaoX = posicao[1]

            if posicaoY > posicaoInicialY and posicaoX == posicaoInicialX:
                x = 0
                y = 40
                posicaoInicialX = posicaoX
                posicaoInicialY = posicaoY

            if posicaoY < posicaoInicialY and posicaoX == posicaoInicialX:
                x = 0
                y = -40
                posicaoInicialX = posicaoX
                posicaoInicialY = posicaoY

            if posicaoY == posicaoInicialY and posicaoX > posicaoInicialX:
                x = 40
                y = 0
                posicaoInicialX = posicaoX
                posicaoInicialY = posicaoY

            if posicaoY == posicaoInicialY and posicaoX < posicaoInicialX:
                x = -40
                y = 0
                posicaoInicialX = posicaoX
                posicaoInicialY = posicaoY

            self.canvas.move(rato.image, x, y)
            root.update()
            time.sleep(0.5)


root = Tk()
root.title("Labirinto - EDL")
app = App(root, maze)

root.mainloop()
