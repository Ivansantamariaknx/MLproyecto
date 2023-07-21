from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def clean_data(datanew):
    # Realizar la limpieza de datos según tus instrucciones
    datanew = datanew.drop(columns=['CLIENTE', 'TELEF'])
    datanew = datanew.rename(columns={"RTM": "Emp"})
    datanew = datanew[datanew['Emp'] == 'RTM']
    datanew = datanew[datanew['ESTADO'] == 'PENDIENTE']
    
    # Correccion comerciales
    datanew['COMERCIAL'] = datanew['COMERCIAL'].replace('JL CARCEDO ', 'JL CARCEDO')
    datanew['COMERCIAL'] = datanew['COMERCIAL'].replace('NICOLAS ', 'NICOLAS')
    datanew['COMERCIAL'] = datanew['COMERCIAL'].replace('NICOLAS IERINO', 'NICOLAS')
    datanew['COMERCIAL'] = datanew['COMERCIAL'].replace('JL CARCEDO', 'CARCEDO')
    
    comercial_dict = {"MOISES": 1, "REBOLLEDO": 2, "JOSE PASCUAL": 3, "NICOLAS": 4, "CARCEDO": 5, "FCO SAMPEDRO": 6, "ELIEZER": 7, "MARCO": 8}
    datanew["COMERCIAL_NUM"] = datanew["COMERCIAL"].map(comercial_dict)
    
    # Teleoperadores
    valores_a_excluir = ['WEBMAIL', 'FACEBOOK', 'MARTA-WEB', 'CAROL-WEB', 'MARTA CHAT', 'WEB DANIEL', 'ABRAHAM', 'NATALIA WEB HDG', 'CAROL-WEB HDG']
    datanew = datanew[~datanew['TELEOPERADOR'].isin(valores_a_excluir)]
    datanew["TELEOPERADOR"] = datanew["TELEOPERADOR"].replace('TERESA-WEB', 'TERESA WEB')
    datanew["TELEOPERADOR"] = datanew["TELEOPERADOR"].replace('MA CARMEN-WEB', 'MA CARMEN WEB')
    datanew["TELEOPERADOR"] = datanew["TELEOPERADOR"].replace('MARI CARMEN WEB ', 'MA CARMEN WEB')
    datanew["TELEOPERADOR"] = datanew["TELEOPERADOR"].replace('NARCISA-WEB', 'NARCISA WEB')
    
    teleop_dict = {'MA CARMEN WEB': 1, 'MONICA CHAT': 2, 'AMPARO WEB': 3, 'TERESA WEB': 4, 'NARCISA WEB': 5, 'DOLORES WEB': 6, 'MONICA WEB': 7, 'ELENA WEB': 8, 'ROSA WEB': 9, 'IVAN WEB': 10, 'LOLI CHAT': 11}
    datanew["TELEOP_NUM"] = datanew["TELEOPERADOR"].map(teleop_dict)
    
    # Canal
    datanew["CANAL"] = datanew["CANAL"].replace('FOrmulario', 'Formulario')
    datanew["CANAL"] = datanew["CANAL"].replace('FORMULARIO', 'Formulario')
    datanew["CANAL"] = datanew["CANAL"].replace('Telefónico', 'TELEFONO')
    
    canal_dict = {'Formulario': 1, 'CHAT': 2, 'TELEFONO': 3, 'Referenciado': 4}
    datanew["CANAL_NUM"] = datanew["CANAL"].map(canal_dict)
    
    # Definir una función personalizada para asignar el tipo de obra según el texto de las observaciones
    def asignar_tipo_obra(texto):
        if 'general' in texto or 'integral' in texto or 'INTEGRAL' in texto or 'GENERAL' in texto:
            return '1'
        elif 'BAÑO' in texto and 'COCINA' in texto or 'baño' in texto and 'cocina' in texto:
            return '2'
        elif 'baño' in texto or 'BAÑO' in texto:
            return '3'
        elif 'cocina' in texto or 'COCINA' in texto:
            return '4'
        else:
            return '5'
    
    # Aplicar la función personalizada a la columna de observaciones para asignar el tipo de obra
    datanew['tipodeobra'] = datanew['OBSERVACIONES'].apply(asignar_tipo_obra)
    datanew["MES"] = datanew["MES"].str.replace(",00", "").astype(int)

    # Guardar la columna de direcciones en una variable antes de eliminarla
    directions = datanew['DIRECCIÓN'].copy()

    datanew = datanew[["MES", "COMERCIAL_NUM", "TELEOP_NUM", "CANAL_NUM", "tipodeobra"]]
    
    # Devolver los datos limpios junto con las direcciones
    return datanew, directions

@app.route('/upload', methods=['POST'])
def upload():
    # Obtener el archivo CSV subido desde el formulario
    file = request.files['file']

    # Cargar el archivo CSV en un DataFrame
    datanew = pd.read_csv(file, sep=";", encoding="utf-8")

    # Realizar la limpieza de datos y recuperar las direcciones
    datanew, directions = clean_data(datanew)

    # Cargar el modelo
    model = joblib.load('D:\Bootcamp\MLproyecto\Flaskv2\my_model.pkl')

    # Realizar las predicciones utilizando el modelo cargado
    predictions = model.predict(datanew)

    # Crear una lista de resultados
    results = []

    # Iterar sobre las predicciones y agregar los resultados a la lista
    for direction, prediction in zip(directions, predictions):
        if prediction == 1:
            result_text = 'Sí'
        else:
            result_text = 'No'

        results.append({'direccion': direction, 'prediccion': result_text})

    # Renderizar la plantilla de resultados y pasar los resultados como parámetro
    return render_template('results.html', results=results)



@app.route('/export', methods=['POST'])
def export():
    # Obtener los datos de la predicción del formulario
    predictions = request.form['predictions']

    # Convertir los datos de la predicción de JSON a una lista de diccionarios
    predictions = jsonify(predictions).json

    # Crear un DataFrame a partir de los datos de la predicción
    df = pd.DataFrame(predictions)

    # Guardar el DataFrame como un archivo Excel
    df.to_excel('prediccion.xlsx', index=False)

    # Redirigir a la página de resultados
    return render_template('results.html', predictions=(predictions), results=results)


if __name__ == '__main__':
    app.run(debug=True)
