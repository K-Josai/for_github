import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def drawMolecularAnimation2D(x, y, cel_length, filename="anime2d.gif", interval=5):
    CYCLE_NUM = x.shape[1]
    fig = plt.figure(figsize=(10, 10))

    def update(i, x, y):
        if i != 0: plt.cla() # 現在描写されているグラフを消去
        plt.xlim(0, cel_length)
        plt.ylim(0, cel_length)
        plt.scatter(x[:,i], y[:,i], c='blue', marker='o')
        plt.title('i=' + str(i))

    ani = animation.FuncAnimation(fig, update, fargs=(x, y), interval=5, frames=CYCLE_NUM)
    
    ani.save(filename, writer="imagemagick")
