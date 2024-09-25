def select_seleccion(arreglo):
    for i in range(len(arreglo) - 1):
        menor = i

        for j in range(i + 1, len(arreglo)):
            if arreglo[j] < arreglo[menor]:
                menor = j

        if menor != i:
            arreglo[menor], arreglo[i] = arreglo[i], arreglo[menor]


b = [5, 3, 4, 2, 1]
select_seleccion(b)

print(b)