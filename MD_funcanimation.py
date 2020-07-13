import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

NATOM = 1000  # Number of particles
NRHO = 0.8  # Number density
NCYCLE = 100
LCEL = np.sqrt(float(NATOM/NRHO))  # Box Size

fig = plt.figure(figsize=(10, 10))


def update(i, x, y):
    if i != 0:
        plt.cla()                      # 現在描写されているグラフを消去

    plt.xlim(0, LCEL)
    plt.ylim(0, LCEL)
    plt.scatter(x[i], y[i], c='blue', marker='o')
    plt.title('i=' + str(i))


def main():
    df = pd.read_csv(
        "tekitou7.txt", delim_whitespace=True, header=None, skiprows=1)
    data_kari = df.values
    x = data_kari[0::2]
    y = data_kari[1::2]
    ani = animation.FuncAnimation(
        fig, update, fargs=(x, y), interval=5, frames=NCYCLE)
    ani.save("MD_test_c_N1000_2.gif", writer="imagemagick")


if __name__ == "__main__":
    main()
