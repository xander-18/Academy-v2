import pandas as pd

data = {
    "Producto": ["A", "B", "C", "D"],
    "Categoria": ["Electrónica", "Ropa", "Electrónica", "Ropa"],
    "Precio": [200, 30, 100, 40],
}
df = pd.DataFrame(data)

resultado = df.groupby(by=["Categoria"]).mean()

print(resultado)
