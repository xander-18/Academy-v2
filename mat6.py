import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta


x_dates = [datetime(2016, 10, 3) + timedelta(days=30*i) for i in range(5)]
y = [772.5, 776.5, 776.6, 776.9, 774]

plt.figure(figsize=(10, 6))
plt.plot(x_dates, y, 'b-', linewidth=2)  

plt.plot(x_dates, y, color='black', linewidth=2, marker='o', label='Línea 1')

plt.title('Gráfico triangular abierto')
plt.xlabel('Fecha')
plt.ylabel('Eje Y')
plt.grid(True)

plt.xlim(x_dates[0], x_dates[-1])
plt.ylim(772.5, 777.0)

plt.plot(x_dates, y, 'ro')  

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))
plt.gcf().autofmt_xdate()
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.5))

plt.legend()
plt.show()