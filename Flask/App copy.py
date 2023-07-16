from flask import Flask, render_template, request

import joblib

# Ruta del archivo del modelo
model_path = 'Model\my_model.pkl'

# Cargar el modelo
model = joblib.load(model_path)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    mes = request.form['mes']
    tipodeobra = request.form['tipodeobra']
    canal = request.form['canal']
    teleop_num = request.form['teleop_num']
    comercial_num = request.form['comercial_num']

    # Mapea los valores seleccionados a los números correspondientes
    tipodeobra_dict = {'GENERAL': 1, 'BAÑO Y COCINA': 2, 'BAÑO': 3, 'COCINA': 4, 'OTROS': 5}
    canal_dict = {'FORMULARIO': 1, 'CHAT': 2, 'TELEFONO': 3, 'REFERENCIADO': 4}
    teleop_num_dict = {'MA CARMEN': 1, 'MONICA CHAT': 2, 'AMPARO': 3, 'TERESA': 4}
    comercial_num_dict = {'MOISES': 1, 'REBOLLEDO': 2, 'JOSE PASCUAL': 3, 'NICOLAS': 4}
    mes_dict = {'ENERO': 1, 'FEBRERO': 2, 'MARZO': 3, 'ABRIL': 4, 'MAYO': 5, 'JUNIO': 6, 'JULIO': 7, 'AGOSTO': 8, 'SEPTIEMBRE': 9, 'OCTUBRE': 10, 'NOVIEMBRE': 11, 'DICIEMBRE': 12}

    tipodeobra_num = tipodeobra_dict[tipodeobra]
    canal_num = canal_dict[canal]
    teleop_num = teleop_num_dict[teleop_num]
    comercial_num = comercial_num_dict[comercial_num]
    mes = mes_dict[mes]
    
    # Llama a la función predict() para obtener la predicción
    prediction = predict(mes, tipodeobra_num, canal_num, teleop_num, comercial_num)
    
    return render_template('result.html', prediction=prediction)

def predict(mes, tipodeobra_num, canal_num, teleop_num, comercial_num):
    # Hacer la predicción utilizando el modelo cargado
    prediction = model.predict([[mes, tipodeobra_num, canal_num, teleop_num, comercial_num]])
    if prediction == 1:
        prediction_text = "Se firma"
    else:
        prediction_text = "No se firma"
    
    return prediction_text

if __name__ == '__main__':
    app.run(debug=True)
