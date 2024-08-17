from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.predict_pipeline import FormData, PredictPipeline

application=Flask(__name__)

app=application

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictdata',methods=['GET','POST'])
def prediction_endpoint():
    if request.method=='GET':
        return render_template('index.html')
    else:
        data=FormData(
            Administrative=request.form.get('Administrative'),
            Administrative_Duration=float(request.form.get('Administrative_Duration')),
            Informational=request.form.get('Informational'),
            Informational_Duration=float(request.form.get('Informational_Duration')),
            ProductRelated=request.form.get('ProductRelated'),
            ProductRelated_Duration=float(request.form.get('ProductRelated_Duration')),
            BounceRates=float(request.form.get('BounceRates')),
            ExitRates=float(request.form.get('ExitRates')),
            PageValues=float(request.form.get('PageValues')),
            SpecialDay=float(request.form.get('SpecialDay')),
            Month=request.form.get('Month'),
            OperatingSystems=request.form.get('OperatingSystems'),
            Browser=request.form.get('Browser'),
            Region=request.form.get('Region'),
            TrafficType=request.form.get('TrafficType'),
            VisitorType=request.form.get('VisitorType'),
            Weekend=bool(request.form.get('Weekend'))
        )
        pred_df=data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline=PredictPipeline()
        results=predict_pipeline.predict(pred_df)
        return render_template('index.html',results=results[0])
    

if __name__=="__main__":
    app.run(host="0.0.0.0")        