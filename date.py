# from datetime import date

# fecha_desde = input("Ingresa la primera fecha desde (YYYYMMDD): ")
# fecha_hasta = input("Ingresa la primera fecha hasta (YYYYMMDD): ")
# fecha_desde = date(fecha_desde, "%Y%m%d")
# fecha_hasta = date(fecha_hasta, "%Y%m%d")
# diferencia = fecha_hasta - fecha_desde
# print(f"Diferencia en dias: {diferencia} días")
# print("Diferencia de dias ", diferencia)
from datetime import datetime

fecha_desde = input("Ingresa la primera fecha desde (DD-MM): ")
fecha_hasta = input("Ingresa la primera fecha hasta (DD-MM): ")

fecha_desde = datetime.strptime(fecha_desde, "%d-%m")
fecha_hasta = datetime.strptime(fecha_hasta, "%d-%m")

if fecha_hasta < fecha_desde:
    print("Error: La fecha 'hasta' no puede ser anterior a la fecha 'desde'.")
else:
    diferencia = (fecha_hasta - fecha_desde).days
    print(f"Diferencia en días: {diferencia} días")
