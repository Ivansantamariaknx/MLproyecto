import pandas as pd

# Cargar el archivo CSV
datanew = pd.read_csv('D:\Bootcamp\MLproyecto\Data\Raw\Datosjulioraw.csv', sep=";", encoding="utf-8")

# Realizar la limpieza de datos
# Eliminar columnas
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

# Aplicar la función a la columna 'observaciones' y crear una nueva columna 'tipodeobra'
datanew['tipodeobra'] = datanew['OBSERVACIONES'].apply(asignar_tipo_obra)

datanew["MES"] = datanew["MES"].str.replace(",00", "").astype(int)

# Continúa con el código para realizar la predicción con los datos limpios

datanew["tipodeobra"] = datanew["tipodeobra"].astype(int)


dataresult = datanew[["MES", "COMERCIAL_NUM", "TELEOP_NUM", "CANAL_NUM", "tipodeobra"]]

dataresult.info()