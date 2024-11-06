# password = input("Ingresa tu password:")
# correcto = True
# error = False
# tiene_caracter = ["#", "$", "@"]
# tiene_numero = "0123456789"
# if len(password) < 6:
#     print("Cumple la longitud minima:", correcto)
# if len(password) > 16:
#     print("Cumple la longitud maxima:", correcto)
# if any(caracter in password for caracter in tiene_caracter):
#     print("Tiene almenos un caracter:", correcto)
# else:
#     print("No contiene ni un caracter asignado:", error)
# if any(number in password for number in tiene_numero):
#     print("Tiene almenos un numero del 0 a 9:", correcto)
# else:
#     print("No contiene un numero del 0 al 9:", error)
# print("La contraseña ingresada es:", password)
password = input("Ingresa tu password:")
correcto = True
error = False
tiene_numero = "0123456789"
tiene_caracter = ["#", "@", "$"]

if len(password) < 6:
    print("Cumple la longitud minima", correcto)
else:
    print("No cumple la longitud minima", error)
if len(password) > 16:
    print("Cumple la longitud maxima", correcto)
else:
    print("No cumple la longitud maxima", error)
if any(caracter in password for caracter in tiene_caracter):
    print("Tiene almenos un caracter:", correcto)
else:
    print("No tiene ni un caracter:", error)
if any(number in password for number in tiene_numero):
    print("Tiene almenos un numero:", correcto)
else:
    print("No tiene ni un numero:", error)