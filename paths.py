#!/usr/bin/env python

from os import path, remove
from flask import Flask, render_template, request, make_response, redirect, url_for
from sys import argv, exit, stderr
import sqlite3
import uuid

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder = ".")

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html = render_template("index.html")
    response = make_response(html)
    return response

@app.route('/writeDetails', methods=['GET'])
def writeDetails():
    html = render_template("writeDetails.html")
    response = make_response(html)
    return response

@app.route('/about', methods=['GET'])
def about():
    html = render_template("about.html")
    response = make_response(html)
    return response



@app.route('/createReview', methods=['GET'])
def createReview():
    try:
        requestId = str(uuid.uuid4())
        address = request.args.get('address')
        startDate = request.args.get('startDate')

        endDate = request.args.get('endDate')

        cleanliness = request.args.get('cleanliness')
        cleanlinessComments = request.args.get('cleanlinessComments')
        noise = request.args.get('noise')
        noiseComments = request.args.get('noiseComments')
        responsive = request.args.get('responsive')
        responsiveComments = request.args.get('responsiveComments')
        landlord = request.args.get('landlord')
        landlordComments = request.args.get('landlordComments')
        pest = request.args.get('pest')
        pestComments = request.args.get('pestComments')
        safety = request.args.get('safety')
        safetyComments = request.args.get('safetyComments')
        appliance = request.args.get('appliance')
        applianceComments = request.args.get('applianceComments')
        transportBool = request.args.get('transportBool')
        if (transportBool == "on"):
            transportBool = "1"
        else:
            transportBool = "0"
        transport = request.args.get("transport")
        transportComments = request.args.get("transportComments")
        furnishedBool = request.args.get("furnishedBool")
        if (furnishedBool == "on"):
            furnishedBool = "1"
        else:
            furnishedBool = "0"
        furnished = request.args.get("furnished")
        furnishedComments = request.args.get("furnishedComments")
        utility = request.args.get("utility")
        finalThoughts = request.args.get("finalThoughts")

        DATABASE_NAME = "darthouseSQLite.db"
        
        if not path.isfile(DATABASE_NAME):
            print(argv[0] + ": Database not found", file=stderr)
            exit(1)


        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()
        inputData = "INSERT INTO reviews VALUES (\""+requestId+"\", \""+address+"\", \""+startDate+"\", \""+endDate+"\", \""\
        +cleanliness+"\", \""+cleanlinessComments+"\", \""+noise+"\", \""+noiseComments+"\", \""+responsive+"\", \""\
        +responsiveComments+"\", \""+landlord+"\", \""+landlordComments+"\", \""+pest+"\", \""+pestComments+"\", \""\
        +safety+"\", \""+safetyComments+"\", \""+appliance+"\", \""+applianceComments+"\", \""+transportBool+"\", \""\
        +transport+"\", \""+transportComments+"\", \""+furnishedBool+"\", \""+furnished+"\", \""+furnishedComments+"\", \""\
        +utility+"\", \""+finalThoughts+"\")"
        print(inputData)

        cursor.execute(inputData)

        print("Data inserted in the table: ")
        data=cursor.execute('''SELECT * FROM reviews''')
        for row in data:
            print(row)
        # Commit your changes in the database    
        connection.commit()
        print("Committed data!")
          
        # Closing the connection
        connection.close()

        html = render_template("submitted.html")
        response = make_response(html)
        return response

    except Exception as e:
        print(e, file=stderr)
        exit(1)
    except sqlite3.OperationalError as e:
        print(e, file=stderr)
        exit(1)
  
@app.route('/findDetails', methods=['GET'])
def findDetails():
    html = render_template("findDetails.html")
    response = make_response(html)
    return response

@app.route('/getContent', methods=['GET'])
def getContent():
    try:
        print("Getting content")
        address = request.args.get('address')
        DATABASE_NAME = "darthouseSQLite.db"
            
        if not path.isfile(DATABASE_NAME):
            print(argv[0] + ": Database not found", file=stderr)
            exit(1)


        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()
        statement = ""
        if (address == "" or address == None):
            print("No data, sending everything...")
            statement = "SELECT address, start_date, end_date, cleanliness, noise, responsive, landlord, pest, \
                safety, appliance, transport, furnished, utility FROM reviews  ORDER BY address"
        else:
            print("Specific address, sending address")
            statement = "SELECT address, start_date, end_date, cleanliness, noise, responsive, landlord, pest, \
                safety, appliance, transport, furnished FROM reviews WHERE address LIKE \'"+address+"%\'\
                ORDER BY address"
            
        print("Statement to be executed: "+statement)
        data = cursor.execute(statement).fetchall()
        html = ""
        color1="background-color: rgb(0, 105, 62);"
        color2="background-color: rgb(18, 49, 43);"
        color = color1
        
        for row in data:
            rating = 0
            total = 0
            cleanliness, noise, responsive, landlord, pest, safety, appliance, transport, furnished = 0, 0, 0, 0, 0, 0, 0, 0, 0
            if (row[3] != ""):
                cleanliness = int(row[3])
                total += 1
            if (row[4] != ""):
                noise = int(row[4])
                total += 1
            if (row[5] != ""):
                responsive = int(row[5])
                total += 1
            if (row[6] != ""):    
                landlord = int(row[6])
                total += 1
            if (row[7] != ""):
                pest = int(row[7])
                total += 1
            if (row[8] != ""):
                safety = int(row[8])
                total += 1
            if (row[9] != ""):
                appliance = int(row[9])
                total += 1
            if (row[10] != ""):
                transport = int(row[10])
                total += 1
            if (row[11] != ""):
                furnished = int(row[11])
                total += 1
            sum = cleanliness + noise + responsive + landlord + pest + safety + appliance + transport + furnished
            if (sum == 0):
                rating = 0
                continue
            else:
                rating = sum/total
                rating = round(rating, 1)
            rating = str(rating)
            

            html += "   <div class=\"row\" style=\""+color+"\">\
                            <div class=\"col-8\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">"+\
                                row[0]+\
                            "</div>\
                            <div class=\"col-4\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">"\
                                +rating+\
                            "<img src=\"static/Images/star-24-gold.png\" style=\"height: 15px; width: 15px; padding-bottom: 4px; padding-left: 2px;\">"\
                            "</div>\
                        </div>"
            if (color == color1):
                color = color2
            else:
                color = color1
            
        cursor.close()
        connection.close()

        response = make_response(html)
        return response

    except Exception as e:
        print(e, file=stderr)
        exit(1)

    except sqlite3.OperationalError as e:
        print(e, file=stderr)
        exit(1)

