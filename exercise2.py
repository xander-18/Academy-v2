number = input("ingresa los nros:").split()
number = [int(digitos) for digitos in number]
repetidos = {n for n in number if number.count(n) > 1}
print(repetidos)
