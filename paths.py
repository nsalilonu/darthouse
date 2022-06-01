#!/usr/bin/env python

from os import path, remove
from flask import Flask, render_template, request, make_response, redirect, url_for
from sys import argv, exit, stderr
import sqlite3
import uuid
import urllib.parse

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
        address = request.args.get('address')
        DATABASE_NAME = "darthouseSQLite.db"
            
        if not path.isfile(DATABASE_NAME):
            print(argv[0] + ": Database not found", file=stderr)
            exit(1)


        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()
        statement = ""
        if (address == "" or address == None):
            # statement = "SELECT address, start_date, end_date, cleanliness, noise, responsive, landlord, pest, \
            #     safety, appliance, transport, furnished, utility FROM reviews  ORDER BY address"
            statement = "SELECT DISTINCT address FROM reviews ORDER BY address"
        else:
            # statement = "SELECT address, start_date, end_date, cleanliness, noise, responsive, landlord, pest, \
            #     safety, appliance, transport, furnished FROM reviews WHERE address LIKE \'"+address+"%\'\
            #     ORDER BY address"
            statement = "SELECT DISTINCT address FROM reviews WHERE address LIKE \'"+address+"%\' ORDER BY address"
            
        addresses = cursor.execute(statement).fetchall()
        html = ""
        color1 = "background-color: rgb(0, 105, 62);"
        color2 = "background-color: rgb(18, 49, 43);"
        color = color1

        for address in addresses:
            addressURL = urllib.parse.quote(address[0])
            statement = "SELECT cleanliness, noise, responsive, landlord, pest, \
                safety, appliance, transport, furnished FROM reviews WHERE address=\'"+address[0]+"\'\
                ORDER BY address"
            cleanliness, noise, responsive, landlord, pest, safety, appliance, transport, furnished = 0, 0, 0, 0, 0, 0, 0, 0, 0
            addressDetails = cursor.execute(statement).fetchall()
            rating = 0
            total = 0

            for details in addressDetails:
                if (details[0] != ""):
                    cleanliness += int(details[0])
                    total += 1
                if (details[1] != ""):
                    noise += int(details[1])
                    total += 1
                if (details[2] != ""):
                    responsive += int(details[2])
                    total += 1
                if (details[3] != ""):    
                    landlord += int(details[3])
                    total += 1
                if (details[4] != ""):
                    pest += int(details[4])
                    total += 1
                if (details[5] != ""):
                    safety += int(details[5])
                    total += 1
                if (details[6] != ""):
                    appliance += int(details[6])
                    total += 1
                if (details[7] != ""):
                    transport += int(details[7])
                    total += 1
                if (details[8] != ""):
                    furnished += int(details[8])
                    total += 1

            sum = cleanliness + noise + responsive + landlord + pest + safety + appliance + transport + furnished
            if (sum == 0):
                rating = 0
                continue
            else:
                rating = sum/total
                rating = round(rating, 1)
                rating = str(rating)
                ratingURL = urllib.parse.quote(rating)
                

            html += "   <div class=\"row\" style=\""+color+"\">\
                            <div class=\"col-8\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                <a href=\"./findMoreDetails?address="+addressURL+"&rating="+ratingURL+"\">"+address[0]+"</a>\
                            </div>\
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

@app.route('/findMoreDetails', methods=['GET'])
def findMoreDetails():
    try:
        address = request.args.get('address')
        totalRating = request.args.get('rating')
        DATABASE_NAME = "darthouseSQLite.db"
            
        if not path.isfile(DATABASE_NAME):
            print(argv[0] + ": Database not found", file=stderr)
            exit(1)


        connection = sqlite3.connect(DATABASE_NAME)
        cursor = connection.cursor()
        statement = "SELECT * FROM reviews WHERE address=\'"+address+"\' "
        reviews = cursor.execute(statement).fetchall()
        color1 = "background-color: rgb(0, 105, 62);"
        color2 = "background-color: rgb(18, 49, 43);"
        color = color1
        html = ""
        rating = 0
        sum = 0
        total = 0

        for review in reviews:
            rating = 0
            sum = 0
            total = 0
            cleanliness, noise, responsive, landlord, pest, safety, appliance, transport, furnished = 0, 0, 0, 0, 0, 0, 0, 0, 0
            if (review[4] != ""):
                cleanliness += int(review[4])
                total += 1
            if (review[6] != ""):
                noise += int(review[6])
                total += 1
            if (review[8] != ""):
                responsive += int(review[8])
                total += 1
            if (review[10] != ""):    
                landlord += int(review[10])
                total += 1
            if (review[12] != ""):
                pest += int(review[12])
                total += 1
            if (review[14] != ""):
                safety += int(review[14])
                total += 1
            if (review[16] != ""):
                appliance += int(review[16])
                total += 1
            if (review[19] != ""):
                transport += int(review[19])
                total += 1
            if (review[22] != ""):
                furnished += int(review[22])
                total += 1

            sum = cleanliness + noise + responsive + landlord + pest + safety + appliance + transport + furnished
            if (sum == 0):
                rating = 0
                continue
            else:
                rating = sum/total
                rating = round(rating, 1)
                rating = str(rating)
                


            html += "<div class=\"row\" style=\""+color+" padding: 10px; color: white; font-size: 40px; font-family: \'Lexend Deca\', sans-serif;\">\
                        <div class=\"col\">\
                    <div class=\"row\" style=\""+color+" padding: 10px;\">\
                            <div class=\"col-8\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Leasing Period: "+review[2]+" - "+review[3]+"\
                            </div>\
                            <div class=\"col-4\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Overall Rating: "+rating+"\
                            <img src=\"static/Images/star-24-gold.png\" style=\"height: 15px; width: 15px; padding-bottom: 4px; padding-left: 2px;\">"\
                            "</div>\
                    </div>\
                    <div class=\"row\" style=\""+color+" padding: 10px;\">\
                        <div class=\"col\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Cleanliness rating: "+str(cleanliness)+"\
                                    <img src=\"static/Images/star-24-gold.png\" style=\"height: 15px; width: 15px; padding-bottom: 4px; padding-left: 2px;\">\
                                    <br><br>\
                                Comments: <br>"+review[5]+"\
                        </div>\
                    </div>"

            if (color == color1):
                color = color2
            else:
                color = color1


    except Exception as e:
        print(e, file=stderr)
        exit(1)

    except sqlite3.OperationalError as e:
        print(e, file=stderr)
        exit(1)

