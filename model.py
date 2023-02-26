from flask import Flask,render_template,request
import pandas as pd
import numpy as np
import pickle
from flask_sqlalchemy import SQLAlchemy
import psycopg2
DATABASE_URL = 'postgresql://car_price_prediction_user:niK7vOLKpK9zsWgFz5LbmonjjGnPJLZS@dpg-cfsb0tpgp3jt6tjli3lg-a.oregon-postgres.render.com/car_price_prediction'

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
db = SQLAlchemy(app)
class symptoms(db.Model):
    SerialNo = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    Symptom_1 = db.Column(db.String(100),nullable=False)
    Symptom_2 = db.Column(db.String(100),nullable=False)
    Symptom_3 = db.Column(db.String(100),nullable=False)
    Symptom_4 = db.Column(db.String(100),nullable=False)
    Symptom_5 = db.Column(db.String(100),nullable=False)
    Symptom_6 = db.Column(db.String(100),nullable=False)

class disease_prediction(db.Model):
    Symptom_1 = db.Column(db.String(100),nullable=False)
    Symptom_2 = db.Column(db.String(100),nullable=False)
    Symptom_3 = db.Column(db.String(100),nullable=False)
    Symptom_4 = db.Column(db.String(100),nullable=False)
    Symptom_5 = db.Column(db.String(100),nullable=False)
    Symptom_6 = db.Column(db.String(100),nullable=False)
    Result = db.Column(db.String(100),nullable=False)
    serialno = db.Column(db.Integer(), primary_key=True,autoincrement=True)

with open('C:/Users/Rakibul islam/OneDrive/Desktop/Disease Prediction/Disease_prediction.pickle', 'rb') as file:
    model = pickle.load(file)
data=pd.read_csv('C:/Users/Rakibul islam/OneDrive/Desktop/Disease Prediction/cleaned_data.csv')

@app.route('/',methods=['GET','POST'])

def Home():
    Symptom_1 = data['Symptom_1']
    Symptom_2 = data['Symptom_2']
    Symptom_3 = data['Symptom_3']
    Symptom_4 = data['Symptom_4']
    Symptom_5 = data['Symptom_5']
    Symptom_6 = data['Symptom_6']
    return render_template('Home.html',Symptom_1=Symptom_1,Symptom_2=Symptom_2,Symptom_3=Symptom_3,Symptom_4=Symptom_4,Symptom_5=Symptom_5,Symptom_6=Symptom_6)


@app.route('/predict',methods=['POST'])
def predict():
    Symptom_1 = request.form.get('Symptom_1')
    Symptom_2 = request.form.get('Symptom_2')
    Symptom_3 = request.form.get('Symptom_3')
    Symptom_4 = request.form.get('Symptom_4')
    Symptom_5 = request.form.get('Symptom_5')
    Symptom_6 = request.form.get('Symptom_6')

    entry = symptoms(Symptom_1=Symptom_1, Symptom_2=Symptom_2, Symptom_3=Symptom_3, Symptom_4=Symptom_4,
                               Symptom_5=Symptom_5, Symptom_6=Symptom_6)
    db.session.add(entry)
    db.session.commit()
    datab = symptoms.query.order_by(symptoms.SerialNo.desc()).first()

    prediction= model.predict(pd.DataFrame(columns= ['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4','Symptom_5', 'Symptom_6'],
                                           data=np.array([datab.Symptom_1,datab.Symptom_2,datab.Symptom_3,datab.Symptom_4,datab.Symptom_5,datab.Symptom_6]).reshape(1,6)))

    entry1 = disease_prediction(Symptom_1=Symptom_1, Symptom_2=Symptom_2, Symptom_3=Symptom_3, Symptom_4=Symptom_4,
                               Symptom_5=Symptom_5, Symptom_6=Symptom_6,Result=prediction[0])
    db.session.add(entry1)
    db.session.commit()

    datab1 = disease_prediction.query.order_by(disease_prediction.serialno.desc()).first()

    return str(datab1.Result)
if __name__=='__main__':
    app.run(debug=False,host='0.0.0.0')