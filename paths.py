#!/usr/bin/env python

from flask import Flask, render_template, request, make_response
from sys import exit, stderr
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
import urllib.parse

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder = ".")
DATABASE_NAME = "postgresql://gkxpqzrwjotsih:9b075c957964638c446f351394517675e40f7ae30ee2997a6b72bc5ec0280114@ec2-3-211-221-185.compute-1.amazonaws.com:5432/dbpk5mu96m82v"
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

@app.route('/getAddresses', methods=['GET'])
def getAddresses():
    try:
        engine = create_engine(DATABASE_NAME)
        Session = sessionmaker(bind = engine)
        session = Session()

        statement = "SELECT DISTINCT address FROM reviews"
        addresses = session.execute(statement).all()
        # addresses = session.query(Reviews.address).distinct()
        session.close()

        addressString = ""
        for address in addresses:
            addressString += address[0] + ", "
        
        addressString = addressString[0:-2]
        response = make_response(addressString)
        return response

    except Exception as e:
        print(e, file=stderr)
        exit(1)

@app.route('/createReview', methods=['GET'])
def createReview():
    try:
        requestId = str(uuid.uuid4())
        address = request.args.get('address')

        address = address.replace("\'", "''")

        startDate = request.args.get('startDate')

        endDate = request.args.get('endDate')

        cleanliness = request.args.get('cleanliness')
        cleanlinessComments = request.args.get('cleanlinessComments')
        cleanlinessComments = cleanlinessComments.replace("\'", "''")

        noise = request.args.get('noise')
        noiseComments = request.args.get('noiseComments')
        noiseComments = noiseComments.replace("\'", "''")


        responsive = request.args.get('responsive')
        responsiveComments = request.args.get('responsiveComments')
        responsiveComments = responsiveComments.replace("\'", "''")


        landlord = request.args.get('landlord')
        landlordComments = request.args.get('landlordComments')
        landlordComments = landlordComments.replace("\'", "''")

        pest = request.args.get('pest')
        pestComments = request.args.get('pestComments')
        pestComments = pestComments.replace("\'", "''")

        safety = request.args.get('safety')
        safetyComments = request.args.get('safetyComments')
        safetyComments = safetyComments.replace("\'", "''")

        appliance = request.args.get('appliance')
        applianceComments = request.args.get('applianceComments')
        applianceComments = applianceComments.replace("\'", "''")
        
        transport = request.args.get("transport")
        transportBool = ""
        if (transport == None or transport.strip() == ""):
            transportBool = "0"
        else:
            transportBool = "1"
        
        transportComments = request.args.get("transportComments")
        transportComments = transportComments.replace("\'", "''")

        furnished = request.args.get("furnished")
        furnishedBool = ""
        if (furnished == None or furnished.strip() == ""):
            furnishedBool = "0"
        else:
            furnishedBool = "1"

        furnishedComments = request.args.get("furnishedComments")
        furnishedComments = furnishedComments.replace("\'", "''")

        utility = request.args.get("utility")

        finalThoughts = request.args.get("finalThoughts")
        finalThoughts = finalThoughts.replace("\'", "''")

        engine = create_engine(DATABASE_NAME)
        Session = sessionmaker(bind = engine)
        session = Session()

        inputData = "INSERT INTO reviews VALUES (\'"+requestId+"\', \'"+address+"\', \'"+startDate+"\', \'"+endDate+"\', \'"\
        +cleanliness+"\', \'"+cleanlinessComments+"\', \'"+noise+"\', \'"+noiseComments+"\', \'"+responsive+"\', \'"\
        +responsiveComments+"\', \'"+landlord+"\', \'"+landlordComments+"\', \'"+pest+"\', \'"+pestComments+"\', \'"\
        +safety+"\', \'"+safetyComments+"\', \'"+appliance+"\', \'"+applianceComments+"\', "+transportBool+", \'"\
        +transport+"\', \'"+transportComments+"\', "+furnishedBool+", \'"+furnished+"\', \'"+furnishedComments+"\', \'"\
        +utility+"\', \'"+finalThoughts+"\')"
        
        session.execute(inputData)

        # Commit your changes in the database    
        session.commit()
        session.close()


        html = render_template("submitted.html")
        response = make_response(html)
        return response

    except Exception as e:
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
        address = address.replace("\'", "''")

        engine = create_engine(DATABASE_NAME)
        Session = sessionmaker(bind = engine)
        session = Session()

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
            
        addresses = session.execute(statement).all()
        html = ""
        color1 = "background-color: rgb(0, 105, 62);"
        color2 = "background-color: rgb(18, 49, 43);"
        color = color1

        for address in addresses:
            addressURL = urllib.parse.quote(address[0])
            addressFormatted = address[0].replace("\'", "''")
            statement = "SELECT cleanliness, noise, responsive, landlord, pest, \
                safety, appliance, transport, furnished FROM reviews WHERE address=\'"+addressFormatted+"\'\
                ORDER BY address"
            cleanliness, noise, responsive, landlord, pest, safety, appliance, transport, furnished = 0, 0, 0, 0, 0, 0, 0, 0, 0
            addressDetails = session.execute(statement).all()
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
                

            html += "<div class=\"row\" style=\""+color+"\">\
                            <div class=\"col-8\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                <a class=\"nav-link\" style=\"font-family: \'Ruda\', sans-serif; color: white;\" href=\"./findMoreDetails?address="+addressURL+"&rating="+ratingURL+"\">"+address[0]+"</a>\
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
        
        session.close()

        response = make_response(html)
        return response

    except Exception as e:
        print(e, file=stderr)
        exit(1)

@app.route('/findMoreDetails', methods=['GET'])
def findMoreDetails():
    try:
        address = request.args.get('address')
        rating = request.args.get('rating')
        
        html = render_template("findMoreDetails.html", address=address, rating=rating)
        response = make_response(html)
        return response

    except Exception as e:
        print(e, file=stderr)
        exit(1)


@app.route('/getMoreContent', methods=['GET'])
def getMoreContent():
    def dateFormat(date):
        dateArray = date.split("-")
        year = dateArray[0]
        month = dateArray[1]
        day = dateArray[2]
        months = {
            "01": "Jan.",
            "02": "Feb.",
            "03": "Mar.",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "Aug.",
            "09": "Sept.",
            "10": "Oct.",
            "11": "Nov.",
            "12": "Dec."
        }
        newDate = months.get(month, "undefined")+" "+day+", "+year
        return newDate 
    
    try:
        address = request.args.get('address')
        addressFormatted = address.replace("\'", "''")
        totalRating = request.args.get('rating')

        engine = create_engine(DATABASE_NAME)
        Session = sessionmaker(bind = engine)
        session = Session()

        statement = "SELECT * FROM reviews WHERE address=\'"+addressFormatted+"\' ORDER BY start_date DESC"
        reviews = session.execute(statement).all()
        color1 = "background-color: rgb(0, 105, 62);"
        color2 = "background-color: rgb(18, 49, 43);"
        color = color2
        reviewNumber = 1
        details = "<div class=\"container-fluid\">\
                    <div class=\"row\" style=\"background-color: rgb(0, 105, 62); padding: 10px; color: white; font-size: 60px; font-variant: small-caps;\
                    font-stretch: ultra-expanded;\
                    font-weight: bold; font-family: 'Ruda', sans-serif;\">\
                        <div class=\"col-8\">\
                            "+address+"\
                        </div>\
                        <div class=\"col-4\">\
                            "+totalRating+"\
                            <img src=\"static/Images/star-24-gold.png\" style=\"height: 35px; width: 35px; padding-bottom: 4px; padding-left: 2px;\">\
                        </div>\
                    </div>"
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

            # Format date:
            startDate = dateFormat(review[2])
            endDate = dateFormat(review[3])


            reviewNumber = str(reviewNumber)
            details += "<div class=\"row\" style=\""+color+" padding: 10px;\">\
                            <div class=\"col-2\" style=\"color: white; font-family: \'Lexend Deca\', sans-serif;\">\
                                <img src=\"static/Images/tenant.png\" style=\"height: auto; width: 100px; padding-bottom: 4px; padding-left: 2px;\"><br>\
                                Review #"+reviewNumber+"\
                            </div>\
                            <div class=\"col-6\" style=\"color: white; font-size: 30px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Leasing Period: "+startDate+" - "+endDate+"\
                            </div>\
                            <div class=\"col-4\" style=\"color: white; font-size: 30px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Overall Rating: "+rating+"\
                            <img src=\"static/Images/star-24-gold.png\" style=\"height: 20px; width: 20px; padding-bottom: 4px; padding-left: 2apx;\">"\
                            "</div>\
                    </div>\
                    <div class=\"row\" style=\""+color+" padding: 10px; text-align: left;\">\
                        <div class=\"col\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Cleanliness: "
            for i in range(cleanliness):
                details +=  "<img src=\"static/Images/star-24-gold.png\" style=\"height: 30px; width: 30px; padding-bottom: 4px; padding-left: 2px;\">"
            
            details += "    <br>\
                            Comments: <br>"+review[5]+"<br><br>\
                        </div>\
                    </div>\
                    <div class=\"row\" style=\""+color+" padding: 10px; text-align: left;\">\
                        <div class=\"col\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Noise rating (Lower ratings mean more noisy): "
            for i in range(noise):
                details +=  "<img src=\"static/Images/star-24-gold.png\" style=\"height: 30px; width: 30px; padding-bottom: 4px; padding-left: 2px;\">"
            details += "<br>\
                                Comments: <br>"+review[7]+"<br><br>\
                        </div>\
                    </div>\
                    <div class=\"row\" style=\""+color+" padding: 10px; text-align: left;\">\
                        <div class=\"col\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Landlord Responsiveness: "
            for i in range(responsive):
                details +=  "<img src=\"static/Images/star-24-gold.png\" style=\"height: 30px; width: 30px; padding-bottom: 4px; padding-left: 2px;\">"
            details +=  "<br>\
                                Comments: <br>"+review[9]+"<br><br>\
                        </div>\
                    </div>\
                        <div class=\"row\" style=\""+color+" padding: 10px; text-align: left;\">\
                        <div class=\"col\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Overall Landlord Quality - (Friendliness, Flexibility, Reliability, Fairness): "
            for i in range(landlord):
                details +=  "<img src=\"static/Images/star-24-gold.png\" style=\"height: 30px; width: 30px; padding-bottom: 4px; padding-left: 2px;\">"
            details += "<br>\
                                Comments: <br>"+review[11]+"<br><br>\
                        </div>\
                    </div>\
                        <div class=\"row\" style=\""+color+" padding: 10px; text-align: left;\">\
                        <div class=\"col\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Pest Control: "
            for i in range(pest):
                details +=  "<img src=\"static/Images/star-24-gold.png\" style=\"height: 30px; width: 30px; padding-bottom: 4px; padding-left: 2px;\">"
            details += "<br>\
                                Comments: <br>"+review[13]+"<br><br>\
                        </div>\
                    </div>\
                        <div class=\"row\" style=\""+color+" padding: 10px; text-align: left;\">\
                        <div class=\"col\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Safety of the Neighborhood: "
            for i in range(safety):
                details +=  "<img src=\"static/Images/star-24-gold.png\" style=\"height: 30px; width: 30px; padding-bottom: 4px; padding-left: 2px;\">"
            details += "<br>\
                                Comments: <br>"+review[15]+"<br><br>\
                        </div>\
                    </div>\
                    <div class=\"row\" style=\""+color+" padding: 10px; text-align: left;\">\
                        <div class=\"col\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Appliance Quality: "
            for i in range(appliance):
                details +=  "<img src=\"static/Images/star-24-gold.png\" style=\"height: 30px; width: 30px; padding-bottom: 4px; padding-left: 2px;\">"
            details += "<br>\
                                Comments: <br>"+review[17]+"<br><br>\
                        </div>\
                    </div>\
                    <div class=\"row\" style=\""+color+" padding: 10px; text-align: left;\">\
                        <div class=\"col\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Did you take public transportation or a shuttle service to/from your home?: "

            if (review[18] == 0):
                details += "No <br><br><br></div></div>"
            elif (review[18] == 1):
                details += "Yes\
                        </div>\
                    </div>\
                     <div class=\"row\" style=\""+color+" padding: 10px; text-align: left;\">\
                        <div class=\"col\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Availability of Transportation: "
                for i in range(transport):
                    details +=  "<img src=\"static/Images/star-24-gold.png\" style=\"height: 30px; width: 30px; padding-bottom: 4px; padding-left: 2px;\">"
                details += "<br>\
                                Comments: <br>"+review[20]+"<br><br>\
                        </div>\
                    </div>"
            
            details += "<div class=\"row\" style=\""+color+" padding: 10px; text-align: left;\">\
                        <div class=\"col\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Furnished?: "
            if (review[21] == 0):
                details += "No <br><br><br></div></div>"
            elif (review[21] == 1):
                details += "Yes\
                        </div>\
                    </div>\
                     <div class=\"row\" style=\""+color+" padding: 10px; text-align: left;\">\
                        <div class=\"col\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                Furniture Quality: "
                for i in range(furnished):
                    details +=  "<img src=\"static/Images/star-24-gold.png\" style=\"height: 30px; width: 30px; padding-bottom: 4px; padding-left: 2px;\">"
                details += "<br>\
                                Comments: <br>"+review[23]+"<br><br>\
                        </div>\
                    </div>"
            
            details += "<div class=\"row\" style=\""+color+" padding: 10px; text-align: left;\">\
                            <div class=\"col\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                    Average Monthly Utility Bill (Total): $"+str(review[24])+"<br><br><br>\
                            </div>\
                        </div>\
                        <div class=\"row\" style=\""+color+" padding: 10px; text-align: left;\">\
                            <div class=\"col\" style=\"color: white; font-size: 20px; font-family: \'Lexend Deca\', sans-serif;\">\
                                    Is there anything else a future tenant should know about this property?:<br>\
                                        "+str(review[25])+"<br><br><br>\
                            </div>\
                        </div><br><br><br>"


            if (color == color1):
                color = color2
            else:
                color = color1

            reviewNumber = int(reviewNumber)
            reviewNumber += 1
        
        session.close()

        details += "</div>"
        response = make_response(details)
        return response

    except Exception as e:
        print("First exception")
        print(e, file=stderr)
        exit(1)


