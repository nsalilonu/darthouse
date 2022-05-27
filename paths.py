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



# @app.route('/searchResults', methods=['GET'])
# def searchResults():
#     try:
#         # Get the fields passed from the html form.
#         dept = request.args.get('dept')
#         num = request.args.get('coursenum')
#         area = request.args.get('area')
#         title = request.args.get('title')
#
#         # Connect to the database.
#         DATABASE_NAME = 'reg.sqlite'
#         if not path.isfile(DATABASE_NAME):
#             print(argv[0] + ": Database not found", file=stderr)
#             exit(1)
#
#         connection = sqlite3.connect(DATABASE_NAME)
#         cursor = connection.cursor()
#
#         # Query them in the database.
#         parameters = [dept, num, area, title]
#         elements = create_stmt(parameters)
#         cursor.execute(elements[0], elements[1])
#         classes = print_rows(cursor)
#
#         # Output the formatted rows to the response.
#         html = ''
#         url = "./regdetails?classid="
#         for row in classes:
#             html += '<tr>' + \
#             "<td><a target='_blank' href='"+ url + str(row[0]) + "'>" + str(row[0]) + "</a></td>" + \
#             "<td>" + str(row[1]) + "</td>" + \
#             "<td>" + str(row[2]) + "</td>" + \
#             "<td>" + str(row[3]) + "</td>" + \
#             "<td>" + str(row[4]) + "</td>" + "</tr>"
#
#         cursor.close()
#         connection.close()
#         response = make_response(html)
#         return response
#
#     except Exception as e:
#         print(e, file=stderr)
#         exit(1)
#     except sqlite3.OperationalError as e:
#         print(e, file=stderr)
#         exit(1)


# Rachel made changes here
# @app.route('/regdetails', methods=['GET'])
# def details():
#     try:
#         # connect to the database I guess?
#         DATABASE_NAME = 'reg.sqlite'
#         if not path.isfile(DATABASE_NAME):
#             print(argv[0] + ": Database not found", file=stderr)
#             exit(1)
#
#
#         connection = sqlite3.connect(DATABASE_NAME)
#         cursor = connection.cursor()
#         classid = request.args.get('classid')
#
#         # if classid == '':
#         #     html = render_template("regdetails.html", classid = classid)
#         #     response = make_response(html)
#         #     return response
#         # elif classid.isdigit() == False:
#         #     classid = True
#         #     html = render_template("regdetails.html", classid = classid)
#         #     response = make_response(html)
#         #     return response
#
#         # get the class info from the database. shamelessly taken from asgt 2
#         query = create_stmt1()
#         cursor.execute(query, [classid])
#         details1 = print_stmt1(cursor) # includes classes.courseid, days, starttime, endtime, bldg, roomnum
#
#         # THIS IS CAUSING CLASSID DOES NOT EXIST WHEN CLASSID IS MISSING DO SOMETHING
#         # handle classid not existing
#         # if len(details1) < 1:
#         #     classid = False
#         #     html = render_template("regdetails.html", classid = classid)
#         #     response = make_response(html)
#         #     return response
#
#         query = create_dept_num_stmt()
#         cursor.execute(query, [classid])
#         details2 = print_dept_num(cursor) # includes dept, coursenum
#
#         query = create_stmt2()
#         cursor.execute(query, [classid])
#         details3 = print_stmt2(cursor) # area, title, descrip, prereqs
#
#         query = create_prof_stmt()
#         cursor.execute(query, [classid])
#         details4 = print_prof_rows(cursor) # just all the profs
#
#
#         html = render_template("regdetails.html", classid = classid, courseid = details1[0], details1 = details1, details2 = details2,
#         details3 = details3, details4 = details4)
#         response = make_response(html)
#         return response
#     except sqlite3.OperationalError as e:
#         print(e, file=stderr)
#         exit(1)
#
# def insert_escapes(text):
#     # find the index of the first % character or -1 if it doesn't exist
#     latest_wildcard_1 = text.find('%')
#     # stores the index of the first _ character or -1 if it doesn't exist
#     latest_wildcard_2 = text.find('_')
#     altered_text = text
#     while latest_wildcard_1 != -1 or latest_wildcard_2 != -1:
#         if latest_wildcard_1 != -1:
#             altered_text = altered_text[:latest_wildcard_1] + "\\" + altered_text[latest_wildcard_1:]
#         if latest_wildcard_2 != -1:
#             altered_text = altered_text[:latest_wildcard_2] + "\\" + altered_text[latest_wildcard_2:]
#         latest_wildcard_1 = altered_text.find('%', latest_wildcard_1 + 2)
#         latest_wildcard_2 = altered_text.find('_', latest_wildcard_2 + 2)
#     return altered_text
#
# def create_stmt1():
#     return 'SELECT classes.courseid, days, starttime, endtime, bldg, roomnum FROM classes \
#     WHERE classes.classid = ?'
#
# def create_dept_num_stmt():
#     return 'SELECT dept, coursenum FROM crosslistings, classes, courses WHERE classes.classid = ?\
#         AND classes.courseid = courses.courseid AND crosslistings.courseid = classes.courseid ORDER BY dept, coursenum ASC'
#
# def create_stmt2():
#     return 'SELECT area, title, descrip, prereqs FROM classes, courses WHERE classid = ? AND classes.courseid = courses.courseid'
#
# def create_prof_stmt():
#     return 'SELECT DISTINCT profname FROM classes, courses, crosslistings, coursesprofs, profs WHERE classes.classid = ?\
#          AND classes.courseid = courses.courseid AND profs.profid = coursesprofs.profid AND coursesprofs.courseid = crosslistings.courseid \
#          AND crosslistings.courseid = classes.courseid ORDER BY profname ASC'
#
# def create_stmt(parameters):
#     found = []
#     # create the first part of the select statement
#     full_stmt = 'SELECT classid, dept, coursenum, area, title FROM courses, classes, crosslistings WHERE '
#     selection_stmt = ' AND crosslistings.courseid = courses.courseid AND classes.courseid = courses.courseid'
#     condition = False
#
#     if parameters[0] is not None:
#         dept = parameters[0].upper()
#         dept = insert_escapes(dept)
#         full_stmt+= "AND dept LIKE ? ESCAPE '\\\'"
#         condition = True
#         found.append('%' + dept + '%')
#     if parameters[1] is not None:
#         num = parameters[1].upper()
#         num = insert_escapes(num)
#         full_stmt += "AND coursenum LIKE ? ESCAPE '\\\'"
#         condition = True
#         found.append('%' + num + '%')
#     if parameters[2] is not None:
#         area = parameters[2].upper()
#         area = insert_escapes(area)
#         full_stmt+= "AND area LIKE ? ESCAPE '\\\'"
#         condition= True
#         found.append('%' + area + '%')
#     if parameters[3] is not None:
#         title = parameters[3]
#         title = insert_escapes(title)
#         full_stmt += "AND title LIKE ? ESCAPE '\\\'"
#         condition = True
#         found.append('%' + title + '%')
#
#     if condition:
#         first_part = full_stmt[:88]
#         second_part = full_stmt[92:]
#         full_stmt = first_part + second_part + selection_stmt
#     else:
#         full_stmt = full_stmt[:88] + selection_stmt[5:]
#
#     full_stmt = full_stmt + " ORDER BY dept, coursenum, classid"
#
#     return [full_stmt, found]
#
# # Rachel made edits here
# def print_stmt1(cursor):
#     row = cursor.fetchone()
#     stmt1Rows = []
#     # if row is None:
#     #    raise ValueError(
#     #         argv[0] + ': classid does not exist')
#     while row is not None:
#         stmt1Rows.append(str(row[0]))
#         stmt1Rows.append(str(row[1]))
#         stmt1Rows.append(str(row[2]))
#         stmt1Rows.append(str(row[3]))
#         stmt1Rows.append(str(row[4]))
#         stmt1Rows.append(str(row[5]))
#         row = cursor.fetchone()
#     return stmt1Rows
#
# # Rachel made edits here
# def print_dept_num(cursor):
#     row = cursor.fetchone()
#     dept_numRows = []
#     while row is not None:
#         dept_numRows.append(str(row[0]) + " " + str(row[1]))
#         row = cursor.fetchone()
#     return dept_numRows
#
# # Rachel made edits here
# def print_stmt2(cursor):
#     row = cursor.fetchone()
#     stmt2Rows = []
#
#     while row is not None:
#         stmt2Rows.append(str(row[0])) # Area
#         stmt2Rows.append(str(row[1])) # Title
#         stmt2Rows.append(str(row[2])) # Description
#         stmt2Rows.append(str(row[3])) # Prerequisites
#         row = cursor.fetchone()
#     return stmt2Rows
#
# # Rachel made edits here
# def print_prof_rows(cursor):
#     row = cursor.fetchone()
#     profRows = []
#
#     while row is not None:
#         profRows.append(str(row[0]))
#         row = cursor.fetchone()
#     return profRows
#
# def print_rows(cursor):
#     row = cursor.fetchone()
#     regRows = []
#
#     while row is not None:
#         regRows.append(row)
#         row = cursor.fetchone()
#     return regRows

