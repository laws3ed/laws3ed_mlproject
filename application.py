import sys
from flask import Flask, request, render_template
from src.prediction_pipeline import FormData, PredictionPipeline
from src.logger import logging
from src.exception import CustomException

application=Flask(__name__)
app=application

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/predictiondata',methods=['GET', 'POST'])
def prediction_endpoint():
    try:
        if request.method=='GET':
            return render_template('index.html')
        else:
            data=FormData(
                Administrative = request.form.get('Administrative'),
                Administrative_Duration = request.form.get('Administrative_Duration', type=float),
                Informational = request.form.get('Informational'),
                Informational_Duration = request.form.get('Informational_Duration', type=float),
                ProductRelated = request.form.get('ProductRelated'),
                ProductRelated_Duration = request.form.get('ProductRelated_Duration', type=float),
                BounceRates = request.form.get('BounceRates', type=float),
                ExitRates = request.form.get('ExitRates', type=float),
                PageValues = request.form.get('PageValues', type=float),
                SpecialDay = request.form.get('SpecialDay', type=float),
                Month = request.form.get('Month'),
                OperatingSystems = request.form.get('OperatingSystems'),
                Browser = request.form.get('Browser'),
                Region = request.form.get('Region'),
                TrafficType = request.form.get('TrafficType'),
                VisitorType = request.form.get('VisitorType'),
                Weekend = request.form.get('Weekend', type=bool)
            )
            input_data_df=data.get_form_data()
            logging.info("Input data values:")
            logging.info(input_data_df)

            prediction_pipeline=PredictionPipeline()
            results=prediction_pipeline.predict(input_data_df)
            return render_template('index.html', results=results[0])
    except Exception as e:
            logging.error(str(e))
            raise CustomException(e, sys)

if __name__=="__main__":
    app.run(host="127.0.0.1")        