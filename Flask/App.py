from flask import Flask, render_template, request
import joblib

# Ruta del archivo del modelo
model_path = 'D:\Bootcamp\MLproyecto\Model\my_model.pkl'

# Cargar el modelo
model = joblib.load(model_path)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Obtén los valores de las calles
    calle_1 = request.form.get('calle_1')
    calle_2 = request.form.get('calle_2')
    calle_3 = request.form.get('calle_3')

    # Obtén los valores de los otros campos para cada calle
    mes = request.form.get('mes')
    tipodeobra= request.form.get('tipodeobra')
    canal= request.form.get('canal')
    teleop_num= request.form.get('teleop_num')
    comercial_num= request.form.get('comercial_num')

    mes= request.form.get('mes')
    tipodeobra= request.form.get('tipodeobra')
    canal= request.form.get('canal')
    teleop_num = request.form.get('teleop_num')
    comercial_num= request.form.get('comercial_num')

    mes = request.form.get('mes')
    tipodeobra = request.form.get('tipodeobra')
    canal = request.form.get('canal')
    teleop_num = request.form.get('teleop_num')
    comercial_num = request.form.get('comercial_num')

    # Realiza la predicción para cada calle
    predictions = []

    # Predicción para calle 1
    prediction_1 = predict(mes_1, tipodeobra, canal, teleop_num, comercial_num)
    predictions.append(prediction_1)

    # Predicción para calle 2
    prediction_2 = predict(mes, tipodeobra, canal, teleop_num, comercial_num)
    predictions.append(prediction_2)

    # Predicción para calle 3
    prediction_3 = predict(mes, tipodeobra, canal, teleop_num, comercial_num)
    predictions.append(prediction_3)

    return render_template('result.html', predictions=predictions)

def predict(mes, tipodeobra, canal, teleop_num, comercial_num):
    # Mapea los valores seleccionados a los números correspondientes
    tipodeobra_dict = {'GENERAL': 1, 'BAÑO Y COCINA': 2, 'BAÑO': 3, 'COCINA': 4, 'OTROS': 5}
    canal_dict = {'FORMULARIO': 1, 'CHAT': 2, 'TELEFONO': 3, 'REFERENCIADO': 4}
    teleop_num_dict = {'MA CARMEN': 1, 'MONICA CHAT': 2, 'AMPARO': 3, 'TERESA': 4}
    comercial_num_dict = {'MOISES': 1, 'REBOLLEDO': 2, 'JOSE PASCUAL': 3, 'NICOLAS': 4}

    tipodeobra_num = tipodeobra_dict[tipodeobra]
    canal_num = canal_dict[canal]
    teleop_num_num = teleop_num_dict[teleop_num]
    comercial_num_num = comercial_num_dict[comercial_num]

    # Hacer la predicción utilizando el modelo cargado
    prediction = model.predict([[mes, tipodeobra_num, canal_num, teleop_num_num, comercial_num_num]])
    if prediction == 1:
        prediction_text = "Se firma"
    else:
        prediction_text = "No se firma"

    return prediction_text

if __name__ == '__main__':
    app.run(debug=True)

