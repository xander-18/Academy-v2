import matplotlib.pyplot as plt
import numpy as np

xpoints = np.array([10, 20, 30])
ypoints = np.array([20, 40, 10])

apoint = np.array([10, 20 , 30])
bpoint = np.array([40, 10 , 30])

plt.plot(xpoints, ypoints , linestyle = 'dotted' , marker="o" , color='red')
plt.plot(apoint , bpoint , color='black' , label='Nuevos Puntos')
plt.xlabel('Eje x')
plt.ylabel('Eje y')
plt.title('Gráfico con límite en el eje x')
plt.grid(True)
plt.show()
