from flask import Flask, request, render_template
import numpy as np
import pickle
import joblib
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
import json


load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")


# Robust model loader: try joblib (recommended), then fall back to pickle files.
def _safe_load_model(*paths):
    """Try loading a model from multiple candidate paths. Returns None on failure."""
    for p in paths:
        try:
            if os.path.exists(p):
                # Try joblib first
                try:
                    return joblib.load(p)
                except Exception:
                    # fallback to pickle
                    with open(p, 'rb') as f:
                        return pickle.load(f)
        except Exception as e:
            # continue to next candidate
            continue
    return None


# loading models (look in a `models/` directory first, then root filenames)
Jmodel = _safe_load_model('models/jmodel.joblib', 'models/jmodel.pkl', 'jmodel.joblib', 'jmodel.pkl')
Wmodel = _safe_load_model('models/wmodel.joblib', 'models/wmodel.pkl', 'wmodel.joblib', 'wmodel.pkl')
Cmodel = _safe_load_model('models/cmodel.joblib', 'models/cmodel.pkl', 'cmodel.joblib', 'cmodel.pkl')
Smodel = _safe_load_model('models/smodel.joblib', 'models/smodel.pkl', 'smodel.joblib', 'smodel.pkl')
Bmodel = _safe_load_model('models/bmodel.joblib', 'models/bmodel.pkl', 'bmodel.joblib', 'bmodel.pkl')
preprocessor = _safe_load_model('models/preprocessor.joblib', 'models/preprocessor.pkl', 'preprocessor.joblib', 'preprocessor.pkl')

#flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["MONGO_URI"] = MONGO_URL
mongo = PyMongo(app)

collection = mongo.db.crop_statistics

# Log model loading status (useful for startup checks)
_loaded = {
    'Jmodel': Jmodel is not None,
    'Wmodel': Wmodel is not None,
    'Cmodel': Cmodel is not None,
    'Smodel': Smodel is not None,
    'Bmodel': Bmodel is not None,
    'preprocessor': preprocessor is not None,
}
print('Model availability:', _loaded)


@app.route('/health')
def health():
    """Health endpoint reporting model availability and basic DB connectivity."""
    try:
        # quick DB ping
        count = collection.count_documents({})
    except Exception:
        count = None
    return {
        'models': _loaded,
        'db_records': count
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('homepage.html')    

@app.route('/submitCropData')
def submitcropdata():
    return render_template('submitCropDetails.html')  

@app.route('/cropDetailsSubmited',methods=['POST'])
def cropdatasubmited():
    if request.method == 'POST':
        commodity = request.form['commodityname']
        district = request.form['district']
        crop_data = {
        "commodity": commodity,
        "district": district
        }
        collection.insert_one(crop_data)
        return render_template('cropDataSubmit.html')


@app.route('/predict')
def predict():
    return render_template('predict.html')  

@app.route('/crop_statistics',methods=['POST','GET'])
def crop_statistics():
    
    distlist = ['Solapur','Nanded','Buldhana','Amravati','Sambhajinagar']
    commoditylist = ['Jowar','Bajara','Cotton','Sugarcane','Wheat']

    cursor  = collection.find({})
    data = list(cursor)
  
    crop_per_dist = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    
    for dataele in data:
        commodityindex = commoditylist.index(dataele.get('commodity'))
        distindex = distlist.index(dataele.get('district'))
        crop_per_dist[distindex][commodityindex] = crop_per_dist[distindex][commodityindex] + 1

    crop_state = [0,0,0,0,0]
    i=0
    for ele in crop_per_dist:
        for ele_value in ele:
            crop_state[i] = crop_state[i] + ele_value
            i = i+1
        i =0
   
    return render_template("crop_statistics.html",crop_state_data = json.dumps(crop_state))
    
@app.route('/Jowar')
def jowar():
    cursor  = collection.find({'commodity':"Jowar"})
    data = list(cursor)
   
    distlist = ['Solapur','Nanded','Buldhana','Amravati','Sambhajinagar']
    frequency_count = [0,0,0,0,0]

    distcount = 0
    for district in distlist:
        for dist in data:
            if(dist.get('district') == district):
                frequency_count[distcount] = frequency_count[distcount] + 1
        distcount = distcount + 1

    return render_template('commodity.html',ID="Jowar",commodity_data=json.dumps(frequency_count))   


@app.route('/Bajara')
def bajara():
    cursor  = collection.find({'commodity':"Bajara"})
    data = list(cursor)

    distlist = ['Solapur','Nanded','Buldhana','Amravati','Sambhajinagar']
    frequency_count = [0,0,0,0,0]

    distcount = 0
    for district in distlist:
        for dist in data:
            if(dist.get('district') == district):
                frequency_count[distcount] = frequency_count[distcount] + 1
        distcount = distcount + 1

    return render_template('commodity.html',ID="Bajara",commodity_data=json.dumps(frequency_count))   


@app.route('/Cotton')
def cotton():

    cursor  = collection.find({'commodity':"Cotton"})
    data = list(cursor)

    distlist = ['Solapur','Nanded','Buldhana','Amravati','Sambhajinagar']
    frequency_count = [0,0,0,0,0]

    distcount = 0
    for district in distlist:
        for dist in data:
            if(dist.get('district') == district):
                frequency_count[distcount] = frequency_count[distcount] + 1
        distcount = distcount + 1

    return render_template('commodity.html',ID="Cotton",commodity_data=json.dumps(frequency_count))   


@app.route('/Sugarcane')
def sugarcane():

    cursor  = collection.find({'commodity':"Sugarcane"})
    data = list(cursor)

    distlist = ['Solapur','Nanded','Buldhana','Amravati','Sambhajinagar']
    frequency_count = [0,0,0,0,0]

    distcount = 0
    for district in distlist:
        for dist in data:
            if(dist.get('district') == district):
                frequency_count[distcount] = frequency_count[distcount] + 1
        distcount = distcount + 1

    return render_template('commodity.html',ID="Sugarcane",commodity_data=json.dumps(frequency_count))   


@app.route('/Wheat')
def wheat():

    cursor  = collection.find({'commodity':"Wheat"})
    data = list(cursor)

    distlist = ['Solapur','Nanded','Buldhana','Amravati','Sambhajinagar']
    frequency_count = [0,0,0,0,0]

    distcount = 0
    for district in distlist:
        for dist in data:
            if(dist.get('district') == district):
                frequency_count[distcount] = frequency_count[distcount] + 1
        distcount = distcount + 1

    return render_template('commodity.html',ID="Wheat",commodity_data=json.dumps(frequency_count))   




@app.route('/Solapur')
def solapur():
     
    cursor  = collection.find({'district':"Solapur"})
    data = list(cursor)

    commoditylist = ['Jowar','Bajara','Cotton','Sugarcane','Wheat']
    crop_frequency = [0,0,0,0,0]
    
    
    for dataele in data:
        commodityindex = commoditylist.index(dataele.get('commodity'))
        crop_frequency[commodityindex] = crop_frequency[commodityindex] + 1

    return render_template('district.html',ID="Solapur",crop_frequency=json.dumps(crop_frequency))  

@app.route('/Nanded')
def nanded():
     
    cursor  = collection.find({'district':"Nanded"})
    data = list(cursor)

    commoditylist = ['Jowar','Bajara','Cotton','Sugarcane','Wheat']
    crop_frequency = [0,0,0,0,0]
    
    
    for dataele in data:
        commodityindex = commoditylist.index(dataele.get('commodity'))
        crop_frequency[commodityindex] = crop_frequency[commodityindex] + 1

    return render_template('district.html',ID="Nanded",crop_frequency=json.dumps(crop_frequency))  


@app.route('/Buldhana')
def buldhana():
     
    cursor  = collection.find({'district':"Buldhana"})
    data = list(cursor)

    commoditylist = ['Jowar','Bajara','Cotton','Sugarcane','Wheat']
    crop_frequency = [0,0,0,0,0]
    
    
    for dataele in data:
        commodityindex = commoditylist.index(dataele.get('commodity'))
        crop_frequency[commodityindex] = crop_frequency[commodityindex] + 1

    return render_template('district.html',ID="Buldhana",crop_frequency=json.dumps(crop_frequency))  

@app.route('/Amaravati')
def amaravati():
     
    cursor  = collection.find({'district':"Amravati"})
    data = list(cursor)

    commoditylist = ['Jowar','Bajara','Cotton','Sugarcane','Wheat']
    crop_frequency = [0,0,0,0,0]
    
    
    for dataele in data:
        commodityindex = commoditylist.index(dataele.get('commodity'))
        crop_frequency[commodityindex] = crop_frequency[commodityindex] + 1

    return render_template('district.html',ID="Amaravati",crop_frequency=json.dumps(crop_frequency))  

@app.route('/Sambhajinagar')
def sambhajinagar():
     
    cursor  = collection.find({'district':"Sambhajinagar"})
    data = list(cursor)

    commoditylist = ['Jowar','Bajara','Cotton','Sugarcane','Wheat']
    crop_frequency = [0,0,0,0,0]
    
    
    for dataele in data:
        commodityindex = commoditylist.index(dataele.get('commodity'))
        crop_frequency[commodityindex] = crop_frequency[commodityindex] + 1

    return render_template('district.html',ID="Sambhajinagar",crop_frequency=json.dumps(crop_frequency))  


@app.route('/result',methods=['POST'])
def result():
    if request.method == 'POST':
        # basic server-side validation and parsing
        allowed_commodities = ['Jowar','Wheat','Cotton','Sugarcane','Bajara']
        commoditytype = request.form.get('commodityname', '').strip()
        month_raw = request.form.get('month', '')
        Year_raw = request.form.get('year', '')
        average_rain_fall_raw = request.form.get('average_rain_fall', '')
        confirm = request.form.get('confirm')

        if not confirm:
            return render_template('predict.html', error='Please confirm before submitting.')

        if commoditytype not in allowed_commodities:
            return render_template('predict.html', error='Please select a valid commodity.')

        try:
            month = int(month_raw)
            if month < 1 or month > 12:
                raise ValueError()
        except Exception:
            return render_template('predict.html', error='Month must be an integer between 1 and 12.')

        try:
            Year = int(Year_raw)
        except Exception:
            return render_template('predict.html', error='Year must be a valid integer.')

        NextYear = int(Year) + 1

        try:
            average_rain_fall = float(average_rain_fall_raw)
        except Exception:
            return render_template('predict.html', error='Average rainfall must be a number (mm).')

        # ensure preprocessor and models are available
        if preprocessor is None:
            return render_template('predict.html', error='Preprocessor not available on server. Contact admin.')

        avgPriceyear = []
        mspyear = []
        mspnextyear = []
        avgPriceNextyear = []
        months_labels = ["jan","Feb","March","April","May","June","July","Aug","Sept","Oct","Nov","Dec"]
        monthcount = 1
        yearcount = 2021

        rainfall2024 = [1,2,3,1,8,673,1318,779,408,106,44,8]
        rainfall2023 = [90,7.2,29.9,41.4,67.6,148.6,315.9,162.7,190.3,50.8,9.3,8]
        x_count =0 

        cropimges = ['/static/images/jowarlogo.webp',
                     '/static/images/wheatlogo.avif',
                     '/static/images/cottonlogo.jpg',
                     '/static/images/sugarcanelogo.jpg',
                     '/static/images/bajralogo.jpg'
                    ]
        

        features = np.array([[int(month), int(Year), float(average_rain_fall)]], dtype=object)
        try:
            transformed_features = preprocessor.transform(features)
        except Exception as e:
            return render_template('predict.html', error='Failed to transform input features: {}'.format(str(e)))

        if(commoditytype == "Jowar"):
            cropface = cropimges[0]
            if Jmodel is None:
                return render_template('predict.html', error='Jowar model is not available on the server.')
            prediction = Jmodel.predict(transformed_features).reshape(1,-1)
            predicted_value = round(prediction[0][0] , 3)
            min_value = round((predicted_value*1550)/100,2)
            max_value = round((predicted_value*2970)/100,2)
            avg_value = round((min_value + max_value) / 2,2)

            for x in rainfall2023:
                features = np.array([[monthcount,yearcount,x]],dtype=object)
                transformed_features = preprocessor.transform(features)
                prediction = Jmodel.predict(transformed_features).reshape(1,-1)
                predicted_value = round(prediction[0][0] , 3)
                predictionMsp = round((predicted_value*2970)/100,2)
                mspyear.append(predictionMsp)
                predictionAvg = round((predicted_value*1550)/100,2)
                avgPriceyear.append(predictionAvg)
                monthcount = monthcount + 1
                x_count = x_count + 1

            for x in rainfall2024:
                features = np.array([[monthcount,yearcount,x]],dtype=object)
                transformed_features = preprocessor.transform(features)
                prediction = Jmodel.predict(transformed_features).reshape(1,-1)
                predicted_value = round(prediction[0][0] , 3)
                predictionMsp = round((predicted_value*2970)/100,2)
                mspnextyear.append(predictionMsp)
                predictionAvg = round((predicted_value*1550)/100,2)
                avgPriceNextyear.append(predictionAvg)
                x_count = x_count + 1

        elif(commoditytype == "Wheat"):
            cropface = cropimges[1]
            if Wmodel is None:
                return render_template('predict.html', error='Wheat model is not available on the server.')
            prediction = Wmodel.predict(transformed_features).reshape(1,-1)
            predicted_value = round(prediction[0][0] , 3)
            min_value = round((predicted_value*1350)/100,2)
            max_value = round((predicted_value*2125)/100,2)
            avg_value = round((min_value + max_value) / 2 ,2)

            for x in rainfall2023:
                features = np.array([[monthcount,yearcount,x]],dtype=object)
                transformed_features = preprocessor.transform(features)
                prediction = Wmodel.predict(transformed_features).reshape(1,-1)
                predicted_value = round(prediction[0][0] , 3)
                predictionMsp = round((predicted_value*2125)/100,2)
                mspyear.append(predictionMsp)
                predictionAvg = round((predicted_value*1350)/100,2)
                avgPriceyear.append(predictionAvg)
                monthcount = monthcount + 1
                x_count = x_count + 1

            for x in rainfall2024:
                features = np.array([[monthcount,yearcount,x]],dtype=object)
                transformed_features = preprocessor.transform(features)
                prediction = Wmodel.predict(transformed_features).reshape(1,-1)
                predicted_value = round(prediction[0][0] , 3)
                predictionMsp = round((predicted_value*2970)/100,2)
                mspnextyear.append(predictionMsp)
                predictionAvg = round((predicted_value*2125)/100,2)
                avgPriceNextyear.append(predictionAvg)
                x_count = x_count + 1
        
        elif(commoditytype == "Cotton"):
            cropface = cropimges[2]
            if Cmodel is None:
                return render_template('predict.html', error='Cotton model is not available on the server.')
            prediction = Cmodel.predict(transformed_features).reshape(1,-1)
            predicted_value = round(prediction[0][0] , 3)
            min_value = round((predicted_value*3600)/100,2)
            max_value = round((predicted_value*6080)/100,2)
            avg_value = round((min_value + max_value) / 2 ,2)

            for x in rainfall2023:
                features = np.array([[monthcount,yearcount,x]],dtype=object)
                transformed_features = preprocessor.transform(features)
                prediction = Cmodel.predict(transformed_features).reshape(1,-1)
                predicted_value = round(prediction[0][0] , 3)
                predictionMsp = round((predicted_value*6080)/100,2)
                mspyear.append(predictionMsp)
                predictionAvg = round((predicted_value*3600)/100,2)
                avgPriceyear.append(predictionAvg)
                monthcount = monthcount + 1
                x_count = x_count + 1

            for x in rainfall2024:
                features = np.array([[monthcount,yearcount,x]],dtype=object)
                transformed_features = preprocessor.transform(features)
                prediction = Cmodel.predict(transformed_features).reshape(1,-1)
                predicted_value = round(prediction[0][0] , 3)
                predictionMsp = round((predicted_value*6080)/100,2)
                mspnextyear.append(predictionMsp)
                predictionAvg = round((predicted_value*3600)/100,2)
                avgPriceNextyear.append(predictionAvg)
                x_count = x_count + 1
        
        elif(commoditytype == "Sugarcane"):
            cropface = cropimges[3]
            if Smodel is None:
                return render_template('predict.html', error='Sugarcane model is not available on the server.')
            prediction = Smodel.predict(transformed_features).reshape(1,-1)
            predicted_value = round(prediction[0][0] , 3)
            min_value = round((predicted_value*2250)/100,2)
            max_value = round((predicted_value*2775)/100,2)
            avg_value = round((min_value + max_value) / 2 ,2)

            for x in rainfall2023:
                features = np.array([[monthcount,yearcount,x]],dtype=object)
                transformed_features = preprocessor.transform(features)
                prediction = Smodel.predict(transformed_features).reshape(1,-1)
                predicted_value = round(prediction[0][0] , 3)
                predictionMsp = round((predicted_value*2775)/100,2)
                mspyear.append(predictionMsp)
                predictionAvg = round((predicted_value*2250)/100,2)
                avgPriceyear.append(predictionAvg)
                monthcount = monthcount + 1
                x_count = x_count + 1

            for x in rainfall2024:
                features = np.array([[monthcount,yearcount,x]],dtype=object)
                transformed_features = preprocessor.transform(features)
                prediction = Smodel.predict(transformed_features).reshape(1,-1)
                predicted_value = round(prediction[0][0] , 3)
                predictionMsp = round((predicted_value*2970)/100,2)
                mspnextyear.append(predictionMsp)
                predictionAvg = round((predicted_value*2775)/100,2)
                avgPriceNextyear.append(predictionAvg)
                x_count = x_count + 1
        
        elif(commoditytype == "Bajara"):
            cropface = cropimges[4]
            if Bmodel is None:
                return render_template('predict.html', error='Bajara model is not available on the server.')
            prediction = Bmodel.predict(transformed_features).reshape(1,-1)
            predicted_value = round(prediction[0][0] , 3)
            min_value = round((predicted_value*1175)/100,2)
            max_value = round((predicted_value*2350)/100,2)
            avg_value = round((min_value + max_value) / 2 ,2)

            for x in rainfall2023:
                features = np.array([[monthcount,yearcount,x]],dtype=object)
                transformed_features = preprocessor.transform(features)
                prediction = Bmodel.predict(transformed_features).reshape(1,-1)
                predicted_value = round(prediction[0][0] , 3)
                predictionMsp = round((predicted_value*2350)/100,2)
                mspyear.append(predictionMsp)
                predictionAvg = round((predicted_value*1175)/100,2)
                avgPriceyear.append(predictionAvg)
                monthcount = monthcount + 1
                x_count = x_count + 1

            for x in rainfall2024:
                features = np.array([[monthcount,yearcount,x]],dtype=object)
                transformed_features = preprocessor.transform(features)
                prediction = Bmodel.predict(transformed_features).reshape(1,-1)
                predicted_value = round(prediction[0][0] , 3)
                predictionMsp = round((predicted_value*2970)/100,2)
                mspnextyear.append(predictionMsp)
                predictionAvg = round((predicted_value*2350)/100,2)
                avgPriceNextyear.append(predictionAvg)
                x_count = x_count + 1



        maxmspyear = max(mspyear)
        maxavgPriceyear = max(avgPriceyear)

        goldmonthindex = mspyear.index(maxmspyear) + 1

        minmspyear = min(mspyear)
        minavgPriceyear = min(avgPriceyear)

        silvermonthindex = mspyear.index(minmspyear) + 1
        


        # Pass native Python lists to templates and let Jinja's tojson handle serialization
        return render_template('result.html', prediction=predicted_value,
                             cropface=cropface,
                             min_value=min_value,
                             max_value=max_value,
                             avg_value=avg_value,
                             year=Year,
                             NextYear=NextYear,
                             month=month,
                             maxhigh=maxmspyear,
                             maxlow=maxavgPriceyear,
                             minhigh=minmspyear,
                             minlow=minavgPriceyear,
                             goldmonth=goldmonthindex,
                             silvermonth=silvermonthindex,
                             months_labels=months_labels,
                             mspyear=mspyear,
                             minPriceYear=avgPriceyear,
                             mspnextyear=mspnextyear,
                             minPriceNextYear=avgPriceNextyear
                             )

if __name__=="__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)