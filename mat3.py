import matplotlib.pyplot as plt
import numpy as np

xpoints = np.array([1, 4, 5, 6, 7])
ypoints = np.array([2, 6, 3, 6, 3])

plt.ylim(0, 8)

plt.plot(xpoints, ypoints, linestyle="dotted", marker="o" ,markerfacecolor="blue" , color="red" )
plt.xlabel("Eje x")
plt.ylabel("Eje y")
plt.title("Gráfico con límite en el eje x")
plt.grid(True)  
plt.show()
