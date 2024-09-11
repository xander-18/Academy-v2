import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
xpoints = pd.date_range(start='2016-10-03' , end='2016-10-07', freq='D')
ypoints = np.array([20, 40, 60, 80, 100])


plt.plot(xpoints, ypoints, linestyle="dotted", marker="o" ,markerfacecolor="blue" , color="red" )
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator())
plt.gcf().autofmt_xdate()
plt.xlabel("Eje x")
plt.ylabel("Eje y")
plt.title("Gráfico con límite en el eje x")
plt.grid(True)
plt.show()