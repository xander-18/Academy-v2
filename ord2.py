import pandas as pd

data = {
    "Producto": ["A", "B", "C", "D"],
    "Categoria": ["Electrónica", "Ropa", "Electrónica", "Ropa"],
    "Precio": [200, 30, 100, 40],
}
df = pd.DataFrame(data)

resultado = df.groupby(by=["Categoria"]).mean()

<<<<<<< HEAD
print(resultado)
=======

b = [5, 3, 4, 2, 1]
select_seleccion(b)
print(b)
>>>>>>> a9a0335b8d85cbd652b57652ee5bf4275a2bc7ce
