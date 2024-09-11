import matplotlib.pyplot as plt
import numpy as np

xpoints1 = np.array([0, 1, 2, 3, 4, 5])
ypoints1 = np.array([0, 0, 0, 0, 0, 0])

x_squares = np.array([0, 1, 2, 3, 4])
y_squares = np.array([0, 1, 4, 9, 16])

x_triangles = np.array([0, 1, 2, 3, 4])
y_triangles = np.array([0, 3, 10, 30, 60])

plt.figure(figsize=(10, 6))
plt.ylim(0, 120)

plt.plot(xpoints1, ypoints1, linestyle='--', color='green', label='Línea Punteada', marker='v')
plt.plot(x_squares, y_squares, 'bs-', label='Serie Cuadrados')
plt.plot(x_triangles, y_triangles, 'r^-', label='Serie Triángulos')

plt.xlabel('Eje X')
plt.ylabel('Eje Y')
plt.grid(True)
plt.legend()

plt.show()