import joblib

new_model = joblib.load('new_model.pkl')
newdata=0
predictions = new_model.predict(new_data)
