import pandas as pd
import numpy as np
from flask import Flask,render_template,request
import pickle

app=Flask(__name__)
pipe=pickle.load(open('model.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST','GET'])
def predict():
    brand=request.form.get('brand')
    typ= request.form.get('type')
    ram=int(request.form.get('ram'))
    gpu= request.form.get('gpu')
    os= request.form.get('os')
    weight=float(request.form.get('weight'))
    touch = request.form.get('touch')
    ips= request.form.get('ips')
    size= float(request.form.get('size'))
    processor= request.form.get('processor')
    clock=float(request.form.get('clock'))
    screen_res = request.form.get('screen')
    mem_type= request.form.get('mem_type')
    mem= int(request.form.get('mem'))

    if touch=='Yes':
        touch=1
    else:
        touch=0
    if ips=='Yes':
        ips=1
    else:
        ips=0

    x_res=int(screen_res.split('x')[0])
    y_res =int(screen_res.split('x')[1])
    ppi=(((x_res**2)+(y_res**2))**0.5)/int(size)

    query = pd.DataFrame([[brand,typ,ram,gpu,os,weight,touch,ips,ppi,processor,clock,mem,mem_type]],columns=['Company', 'TypeName', 'Ram', 'Gpu', 'OpSys', 'Weight', 'TouchScreen', 'IPS', 'PPI', 'Processor','clockspeed', 'Memory_amount', 'Memory_type'])
    res=pipe.predict(query)
    price=str(np.round(np.exp(res[0]),2))
    return render_template('index.html', prediction_text='The predicted price is Rs.{}/-'.format(price))

if __name__=='__main__':
    app.run(debug=True)


