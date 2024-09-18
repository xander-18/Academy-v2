# from flask import (
#     Flask,
#     render_template,
#     request,
#     send_from_directory,
#     redirect,
#     url_for,
#     flash,
# )
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# app = Flask(__name__)
# app.secret_key = "supersecretkey"


# def leer_csv_seguro(path):
#     try:
#         # Primer intento: Leer con configuración predeterminada
#         df = pd.read_csv(path, delimiter=',')  # Asegúrate de usar el delimitador correcto
#     except pd.errors.ParserError:
#         try:
#             # Segundo intento: Leer ignorando líneas problemáticas
#             df = pd.read_csv(path, delimiter=',', on_bad_lines="skip")
#         except pd.errors.ParserError:
#             # Tercer intento: Leer con separación de campos manual
#             df = pd.read_csv(path, delimiter=',', sep=None, engine="python")

#     return df

# def limpiar_dataframe(df):
#     # Elimina columnas no deseadas
#     df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
#     # Elimina filas con valores nulos en todas las columnas
#     df = df.dropna(how='all')
#     return df

# # Leer el archivo CSV de forma segura
# products = leer_csv_seguro("data/product.csv")
# ventas = leer_csv_seguro("data/ventas.csv")
# user = leer_csv_seguro("data/user.csv")


# # usuario = leer_csv_seguro("data/usuarios.csv")
# # Función para generar recomendaciones basadas en intereses
# def generate_recommendations(interests):
#     # Vectorizar las categorías de productos
#     vectorizer = CountVectorizer().fit_transform(products["categoria"])
#     similarity_matrix = cosine_similarity(vectorizer)

#     # Encontrar productos relacionados con los intereses
#     recommendations = []
#     for interest in interests.split(","):
#         interest = interest.strip().lower()
#         for index, row in products.iterrows():
#             if interest in row["categoria"].lower():
#                 recommendations.append(row)

#     # Convertir la lista de Series a DataFrame
#     recommendations_df = pd.DataFrame(recommendations)
#     return recommendations_df


# @app.route("/ventas")
# def ventas_page():
#     # Agrupa por id_producto y fecha_vendida, sumando las cantidades
#     ventas_totales = (
#         ventas.groupby(["id_producto", "fecha_vendida"])["cantidad"].sum().reset_index()
#     )

#     # Luego realiza el merge con los productos para obtener información adicional
#     ventas_totales = ventas_totales.merge(
#         products, left_on="id_producto", right_on="id"
#     )

#     # Convierte el DataFrame en una lista de diccionarios para pasar a la plantilla
#     ventas_list = ventas_totales.to_dict(orient="records")
#     return render_template("ventas.html", sales=ventas_list)


# @app.route("/usuarios/list")
# def list_user():
#     user = leer_csv_seguro("data/user.csv")
#     user = limpiar_dataframe(user)
#     num_usuarios = len(user)
#     print(user.head())  # Imprime las primeras filas del DataFrame para depuración
#     return render_template("history_user.html", sales=user.to_dict(orient="records"), total_usuarios=num_usuarios)


# @app.route("/img/<path:filename>")
# def custom_static(filename):
#     return send_from_directory("img", filename)


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         nombre = request.form["name"]
#         email = request.form["email"]
#         password = request.form["password"]
#         fecha_registro = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

#         # Cargar el historial de usuarios
#         usuarios_path = "data/user.csv"
#         usuarios_df = leer_csv_seguro(usuarios_path)

#         # Agregar el nuevo usuario
#         nuevo_usuario = pd.DataFrame(
#             [[nombre, email, password, fecha_registro]],
#             columns=["Nombre", "Email", "Password", "Fecha de Registro"],
#         )
#         usuarios_df = pd.concat([usuarios_df, nuevo_usuario], ignore_index=True)
#         usuarios_df.to_csv(usuarios_path, index=False)

#         # Mostrar mensaje de éxito
#         flash("¡Eres parte de nuestra comunidad!", "success")
#         return redirect(url_for("index"))

#     return render_template("register.html")


# @app.route("/recommendations", methods=["POST"])
# def recommendations():
#     interests = request.form.get("interests", "")
#     if interests:
#         recommended_products = generate_recommendations(interests)
#     else:
#         recommended_products = pd.DataFrame()  # No hay recomendaciones

#     # Convertir el DataFrame a una lista de diccionarios
#     recommendations_list = recommended_products.to_dict(orient="records")
#     return render_template("index.html", recommendations=recommendations_list)
                                                  

# if __name__ == "__main__":
#     app.run(debug=True, port=5001)