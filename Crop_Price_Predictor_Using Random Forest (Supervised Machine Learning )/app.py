from flask import Flask,request, render_template
import numpy as np
import pickle
import sklearn
import mysql.connector
print(sklearn.__version__)

#loading models
Jmodel = pickle.load(open('jmodel.pkl','rb'))
Wmodel = pickle.load(open('wmodel.pkl','rb'))
Cmodel = pickle.load(open('cmodel.pkl','rb'))
Smodel = pickle.load(open('smodel.pkl','rb'))
Bmodel = pickle.load(open('bmodel.pkl','rb'))
preprocessor = pickle.load(open('preprocessor.pkl','rb'))

#flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Data Base Connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="onkar2004",
  database="crop_sowing_data"
)

# Cursor for Data base
mycursor = mydb.cursor()


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
        sql = "INSERT INTO crop_statistics (commodity,dist) VALUES (%s,%s)"
        val = (commodity,district)
        mycursor.execute(sql,val)

        mydb.commit()
        return render_template('cropDataSubmit.html')  


@app.route('/predict')
def predict():
    return render_template('predict.html')  

@app.route('/crop_statistics',methods=['POST','GET'])
def crop_statistics():

    sql = "SELECT * FROM crop_statistics WHERE commodity= 'Jowar'"
    mycursor.execute(sql)
    data = mycursor.fetchall()

    distlist = ['Solapur','Nanded','Buldhana','Amravati','Sambhajinagar']
    jowarcount = [0,0,0,0,0]

    distcount = 0
    for district in distlist:
        for dist in data:
            if(dist[1] == district):
                jowarcount[distcount] = jowarcount[distcount] + 1
        distcount = distcount + 1


    sql = "SELECT * FROM crop_statistics"
    mycursor.execute(sql)
    data = mycursor.fetchall()

    commoditylist = ['Jowar','Bajara','Cotton','Sugarcane','Wheat']
    crop_per_dist = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    
    
    for dataele in data:
        commodityindex = commoditylist.index(dataele[0])
        distindex = distlist.index(dataele[1])
        crop_per_dist[distindex][commodityindex] = crop_per_dist[distindex][commodityindex] + 1

    crop_state = [0,0,0,0,0]
    sum =0
    i=0
    for ele in crop_per_dist:
        for ele_value in ele:
            crop_state[i] = crop_state[i] + ele_value
            i = i+1
        i =0

    print(crop_state)
    mydb.commit()
    
    return render_template("crop_statistics.html",jowarsowingdata = jowarcount,
                                            distlabel = distlist,
                                            solapur_crop=crop_per_dist[0],
                                            nanded_crop = crop_per_dist[1],
                                            buldhana_crop = crop_per_dist[2],
                                            amravati_crop = crop_per_dist[3],
                                            sambhajinagar_crop = crop_per_dist[4],
                                            crop_state_data = crop_state
                                            )
    
@app.route('/Jowar')
def jowar():



    

    sql = "SELECT * FROM crop_statistics WHERE commodity= 'Jowar'"
    mycursor.execute(sql)
    data = mycursor.fetchall()

    distlist = ['Solapur','Nanded','Buldhana','Amravati','Sambhajinagar']
    jowarcount = [0,0,0,0,0]

    distcount = 0
    for district in distlist:
        for dist in data:
            if(dist[1] == district):
                jowarcount[distcount] = jowarcount[distcount] + 1
        distcount = distcount + 1

    return render_template('commodity.html',ID="Jowar",jowardata=jowarcount)   


@app.route('/Bajara')
def bajara():

    sql = "SELECT * FROM crop_statistics WHERE commodity= 'Bajara'"
    mycursor.execute(sql)
    data = mycursor.fetchall()

    distlist = ['Solapur','Nanded','Buldhana','Amravati','Sambhajinagar']
    jowarcount = [0,0,0,0,0]

    distcount = 0
    for district in distlist:
        for dist in data:
            if(dist[1] == district):
                jowarcount[distcount] = jowarcount[distcount] + 1
        distcount = distcount + 1

    return render_template('commodity.html',ID="Bajara",jowardata=jowarcount)   


@app.route('/Cotton')
def cotton():

    sql = "SELECT * FROM crop_statistics WHERE commodity= 'Cotton'"
    mycursor.execute(sql)
    data = mycursor.fetchall()

    distlist = ['Solapur','Nanded','Buldhana','Amravati','Sambhajinagar']
    jowarcount = [0,0,0,0,0]

    distcount = 0
    for district in distlist:
        for dist in data:
            if(dist[1] == district):
                jowarcount[distcount] = jowarcount[distcount] + 1
        distcount = distcount + 1

    return render_template('commodity.html',ID="Cotton",jowardata=jowarcount)   


@app.route('/Sugarcane')
def sugarcane():

    sql = "SELECT * FROM crop_statistics WHERE commodity= 'Sugarcane'"
    mycursor.execute(sql)
    data = mycursor.fetchall()

    distlist = ['Solapur','Nanded','Buldhana','Amravati','Sambhajinagar']
    jowarcount = [0,0,0,0,0]

    distcount = 0
    for district in distlist:
        for dist in data:
            if(dist[1] == district):
                jowarcount[distcount] = jowarcount[distcount] + 1
        distcount = distcount + 1

    return render_template('commodity.html',ID="SugarCane",jowardata=jowarcount)   


@app.route('/Wheat')
def wheat():

    sql = "SELECT * FROM crop_statistics WHERE commodity= 'Wheat'"
    mycursor.execute(sql)
    data = mycursor.fetchall()

    distlist = ['Solapur','Nanded','Buldhana','Amravati','Sambhajinagar']
    jowarcount = [0,0,0,0,0]

    distcount = 0
    for district in distlist:
        for dist in data:
            if(dist[1] == district):
                jowarcount[distcount] = jowarcount[distcount] + 1
        distcount = distcount + 1

    return render_template('commodity.html',ID="Wheat",jowardata=jowarcount)   




@app.route('/Solapur')
def solapur():
     
    sql = "SELECT * FROM crop_statistics WHERE dist= 'Solapur'"
    mycursor.execute(sql)
    data = mycursor.fetchall()

    commoditylist = ['Jowar','Bajara','Cotton','Sugarcane','Wheat']
    crop_frequency = [0,0,0,0,0]
    
    
    for dataele in data:
        commodityindex = commoditylist.index(dataele[0])
        crop_frequency[commodityindex] = crop_frequency[commodityindex] + 1

    return render_template('district.html',ID="Solapur",crop_frequency=crop_frequency)  

@app.route('/Nanded')
def nanded():
     
    sql = "SELECT * FROM crop_statistics WHERE dist= 'Nanded'"
    mycursor.execute(sql)
    data = mycursor.fetchall()

    commoditylist = ['Jowar','Bajara','Cotton','Sugarcane','Wheat']
    crop_frequency = [0,0,0,0,0]
    
    
    for dataele in data:
        commodityindex = commoditylist.index(dataele[0])
        crop_frequency[commodityindex] = crop_frequency[commodityindex] + 1

    return render_template('district.html',ID="Nanded",crop_frequency=crop_frequency)  


@app.route('/Buldhana')
def buldhana():
     
    sql = "SELECT * FROM crop_statistics WHERE dist= 'Buldhana'"
    mycursor.execute(sql)
    data = mycursor.fetchall()

    commoditylist = ['Jowar','Bajara','Cotton','Sugarcane','Wheat']
    crop_frequency = [0,0,0,0,0]
    
    
    for dataele in data:
        commodityindex = commoditylist.index(dataele[0])
        crop_frequency[commodityindex] = crop_frequency[commodityindex] + 1

    return render_template('district.html',ID="Buldhana",crop_frequency=crop_frequency)  

@app.route('/Amaravati')
def amaravati():
     
    sql = "SELECT * FROM crop_statistics WHERE dist= 'Amravati'"
    mycursor.execute(sql)
    data = mycursor.fetchall()

    commoditylist = ['Jowar','Bajara','Cotton','Sugarcane','Wheat']
    crop_frequency = [0,0,0,0,0]
    
    
    for dataele in data:
        commodityindex = commoditylist.index(dataele[0])
        crop_frequency[commodityindex] = crop_frequency[commodityindex] + 1

    return render_template('district.html',ID="Amaravati",crop_frequency=crop_frequency)  

@app.route('/Sambhajinagar')
def sambhajinagar():
     
    sql = "SELECT * FROM crop_statistics WHERE dist= 'Sambhajinagar'"
    mycursor.execute(sql)
    data = mycursor.fetchall()

    commoditylist = ['Jowar','Bajara','Cotton','Sugarcane','Wheat']
    crop_frequency = [0,0,0,0,0]
    
    
    for dataele in data:
        commodityindex = commoditylist.index(dataele[0])
        crop_frequency[commodityindex] = crop_frequency[commodityindex] + 1

    return render_template('district.html',ID="Sambhajinar",crop_frequency=crop_frequency)  


@app.route('/result',methods=['POST'])
def result():
    if request.method == 'POST':
        commoditytype = request.form['commodityname']
        month  = request.form['month']
        Year = request.form['year']
        NextYear = int(Year) + 1
        average_rain_fall = request.form['average_rain_fall'] 

        avgPriceyear = []
        mspyear = []
        mspnextyear = []
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
        

        features = np.array([[month,Year,average_rain_fall]],dtype=object)
        transformed_features = preprocessor.transform(features)

        if(commoditytype == "Jowar"):
            cropface = cropimges[0]
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
                x_count = x_count + 1

        elif(commoditytype == "Wheat"):
            cropface = cropimges[1]
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
                predictionMsp = round((predicted_value*1350)/100,2)
                mspyear.append(predictionMsp)
                predictionAvg = round((predicted_value*2125)/100,2)
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
                x_count = x_count + 1
        
        elif(commoditytype == "Cotton"):
            cropface = cropimges[2]
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
                predictionMsp = round((predicted_value*3600)/100,2)
                mspyear.append(predictionMsp)
                predictionAvg = round((predicted_value*6080)/100,2)
                avgPriceyear.append(predictionAvg)
                monthcount = monthcount + 1
                x_count = x_count + 1

            for x in rainfall2024:
                features = np.array([[monthcount,yearcount,x]],dtype=object)
                transformed_features = preprocessor.transform(features)
                prediction = Cmodel.predict(transformed_features).reshape(1,-1)
                predicted_value = round(prediction[0][0] , 3)
                predictionMsp = round((predicted_value*2970)/100,2)
                mspnextyear.append(predictionMsp)
                x_count = x_count + 1
        
        elif(commoditytype == "Sugarcane"):
            cropface = cropimges[3]
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
                predictionMsp = round((predicted_value*2250)/100,2)
                mspyear.append(predictionMsp)
                predictionAvg = round((predicted_value*2775)/100,2)
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
                x_count = x_count + 1
        
        elif(commoditytype == "Bajara"):
            cropface = cropimges[4]
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
                predictionMsp = round((predicted_value*1175)/100,2)
                mspyear.append(predictionMsp)
                predictionAvg = round((predicted_value*2350)/100,2)
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
                x_count = x_count + 1



        maxmspyear = max(mspyear)
        maxavgPriceyear = max(avgPriceyear)

        goldmonthindex = mspyear.index(maxmspyear) + 1

        minmspyear = min(mspyear)
        minavgPriceyear = min(avgPriceyear)

        silvermonthindex = mspyear.index(minmspyear) + 1
        


        return render_template('result.html',prediction = predicted_value,
                                             min_value = min_value,
                                             max_value = max_value,
                                             avg_value= avg_value,
                                             year = Year,
                                             NextYear = NextYear,
                                             month = month,
                                             maxhigh = maxmspyear,
                                             maxlow = maxavgPriceyear,
                                             minhigh = minmspyear,
                                             minlow = minavgPriceyear,
                                             goldmonth = goldmonthindex,
                                             silvermonth = silvermonthindex,
                                             months_labels = months_labels,
                                             mspyear = mspyear,
                                             mspnextyear = mspnextyear,
                                             cropface = cropface
                                             )

if __name__=="__main__":
    app.run(debug=True)