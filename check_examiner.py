from email.mime.text import MIMEText
import ssl
import smtplib
import psycopg2
import requests
import base64
import csv, json, sys
import optparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from email.mime.image import MIMEImage
import calendar
import get_split

APPS_TO_ANALYSE = 90
executor = ThreadPoolExecutor(max_workers=10)

# A very simple Flask Hello World app for you to get started with...
def get_month_text (number):

    if number==1:
        return "January"
    if number==2:
        return "February"
    if number==3:
        return "March"
    if number==4:
        return "April"
    if number==5:
        return "May"
    if number==6:
        return "June"
    if number==7:
        return "July"
    if number==8:
        return "August"
    if number==9:
        return "September"
    if number==10:
        return "October"
    if number==11:
        return "November"
    if number==12:
        return "December"

from flask import Flask
from flask import jsonify
import datetime
from datetime import date, timedelta
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pprint
from pprint import pprint
import json
import pymongo
from decimal import *
from flask import request
from flask_caching import Cache
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify

matplotlib.use('agg')
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
from flask_cors import CORS, cross_origin
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/')
@app.route('/data')
def get_examiner():
        ## Initializing the mongo connection
    examiner_name = request.args['name']
    return jsonify(hello_world(examiner_name))
@app.route('/')
def hello_world():
    return send_from_directory('static', 'index.html')
# index route, shows index.html view
@app.route('/application')
def index():
  return render_template('index.html')

@app.route('/cia')
def cia():
  response = requests.get('https://raw.githubusercontent.com/iancoleman/cia_world_factbook_api/master/data/factbook.json').json()
  mappo = {}
  for c in ['united_states', 'mexico', 'japan', 'european_union', 'china', 'brazil']:
    mappo[c] = response['countries'][c]
  return jsonify(mappo)


def hello_world(examiner_name):
        ## Initializing the mongo connection
    connection_string = 'mongodb+srv://Zeevtest:Zeevtest@freship-fu97s.mongodb.net/test?retryWrites=true&w=majority'
    from bson.decimal128 import Decimal128
    from bson.codec_options import TypeCodec
    class DecimalCodec(TypeCodec):
        python_type = Decimal    # the Python type acted upon by this type codec
        bson_type = Decimal128   # the BSON type acted upon by this type codec
        def transform_python(self, value):
            """Function that transforms a custom type value into a type
            that BSON can encode."""
            return Decimal128(value)
        def transform_bson(self, value):
            """Function that transforms a vanilla BSON type value into our
            custom type."""
            return value.to_decimal()
    decimal_codec = DecimalCodec()

    today = date.today()
    cutoff_date = today - timedelta(days=70)

    from bson.codec_options import TypeRegistry
    type_registry = TypeRegistry([decimal_codec])
    from bson.codec_options import CodecOptions
    codec_options = CodecOptions(type_registry=type_registry)

    mongo_client = pymongo.MongoClient(connection_string)
    mydb = mongo_client["patents"]
    db = mongo_client["patents"]
    examiners_collection = mydb.get_collection("examiners_new" , codec_options=codec_options)

    print(examiner_name)
    examiner_record = examiners_collection.find_one({'examiner':examiner_name})

    if examiner_record is None:
        print ("no examiner record")

    else:
        if "total_refused" in examiner_record:
            examiner_apps_refused = examiner_record.get("total_refused")
        else:
            examiner_apps_refused = 0
        if "total_refused_with_interview" in examiner_record:
            examiner_apps_refused_with_interview = examiner_record.get("total_refused_with_interview")
        else:
            examiner_apps_refused_with_interview = 0
        if "total_refused_without_interview" in examiner_record:
            examiner_apps_refused_without_interview = examiner_record.get("total_refused_without_interview")
        else:
            examiner_apps_refused_without_interview = 0

        if "total_granted" in examiner_record:
            examiner_apps_granted = examiner_record.get("total_granted")
        else:
            examiner_apps_granted = 0
        if "total_granted_with_interview" in examiner_record:
            examiner_apps_granted_with_interview = examiner_record.get("total_granted_with_interview")
        else:
            examiner_apps_granted_with_interview = 0
        if "total_granted_without_interview" in examiner_record:
            examiner_apps_granted_without_interview = examiner_record.get("total_granted_without_interview")
        else:
            examiner_apps_granted_without_interview = 0

        examiner_apps_we_have = examiner_apps_granted + examiner_apps_refused
        examiner_grant_rate = "%.0f%%" % (100 * examiner_apps_granted / examiner_apps_we_have)
        examiner_grant_rate_with_interview = "%.0f%%" % (100 * examiner_apps_granted_with_interview / (examiner_apps_granted_with_interview + examiner_apps_refused_with_interview))
        examiner_grant_rate_without_interview = "%.0f%%" % (100 * examiner_apps_granted_without_interview / (examiner_apps_granted_without_interview + examiner_apps_refused_without_interview))
        interview_improvement_rate = "%.0f%%" % (100 * (examiner_apps_granted_with_interview / (examiner_apps_granted_with_interview + examiner_apps_refused_with_interview)) / (examiner_apps_granted_without_interview / (examiner_apps_granted_without_interview + examiner_apps_refused_without_interview))-100)

        # Here comes the monthly data:
        successful_month_retrieved = examiner_record.get("successful_month")
        failed_month_retrieved = examiner_record.get("failed_month")
        successful_month = []
        failed_month = []
        month_stat = []
        #possible_response_month = []
        total_successful_responses = 0
        total_failed_responses = 0

        for i in range (1,14):
                successful_month.append(0)
                failed_month.append(0)
                month_stat.append(0)
                #possible_response_month.append(0)

        try:
            for key,value in successful_month_retrieved.items():
                key = int(key)
                successful_month[key] = value
                total_successful_responses = total_successful_responses + value
        except AttributeError:
            print ("no successful month data")
            total_successful_responses = 0.00000000000000000000000001
        try:
            for key,value in failed_month_retrieved.items():
                key = int(key)
                failed_month[key] = value
                total_failed_responses = total_failed_responses + value
        except AttributeError:
            print ("no failed month data")

        #print ("monthly statistics, month by month")
        for i in range (0,13):
            if (failed_month[i] !=0):
                month_stat[i] = successful_month[i] / (successful_month[i] + failed_month [i])
                #month_stat[i] = "%.0f%%" % (100 * month_stat[i])
                #if (i !=0):
                    #print ("Month",str(i),": ",month_stat[i], " ")

        response_success_rate = total_successful_responses / ( total_successful_responses + total_failed_responses)

        # Run through the 6 months including and after the one where the office action was issued:
        recommended_month_stat = 0

        recommended_month_stat = "%.0f%%" % (100 * recommended_month_stat)
        response_success_rate = "%.0f%%" % (100 * response_success_rate)

        # Here ends the monthly data.

        reporting_text = "<br><br>Hi there! The examiner's name is: "
        reporting_text = reporting_text + examiner_name
        reporting_text = reporting_text + "<br><br>We crunched through "
        reporting_text = reporting_text + str(examiner_apps_we_have)
        reporting_text = reporting_text + " applications for this examiner and here is what we can tell you:<br><br>"
        reporting_text = reporting_text + "Grant rate (chances to eventually reach a grant): "
        reporting_text = reporting_text + str(examiner_grant_rate) + "with interview: " + str(examiner_grant_rate_with_interview) + " / without interview: " + str(examiner_grant_rate_without_interview) + " improvement rate: " + str(interview_improvement_rate)
        reporting_text = reporting_text + "<br>Response success rate (chances to overcome one office action): "
        reporting_text = reporting_text + str(response_success_rate)
        reporting_text = reporting_text + "<br><br>Full monthly stats: "
        months = {}
        for i in range (0,13):
            if (failed_month[i] !=0):
                month_stat[i] = successful_month[i] / (successful_month[i] + failed_month [i])
                month_stat[i] = "%.0f%%" % (100 * month_stat[i])
                if (i !=0):
                    reporting_text = reporting_text + str(get_month_text(i)) + ": " + month_stat[i] + " | "
                    months[get_month_text(i)] = month_stat[i]

        #print (reporting_text)

        # Now is the time to check if the office action matches any of our pre-tracked queries
        # and if yes, to fire it up.

        # starting from checking if the applicant is in our tracked applicant's list.

        sender_email = "freshipinsights@gmail.com"
        receiver_email = "zeev@freship.com"
        password = "freship#14insights"

        # Create the plain-text and HTML version of your message
        text = reporting_text
        html = "<html><body>"+reporting_text+"</body></html>"
        result = {}
        result['examiner_name'] = examiner_name
        result['examiner_apps_we_have'] = examiner_apps_we_have
        result['examiner_grant_rate'] = examiner_grant_rate
        result['examiner_grant_rate_with_interview'] = examiner_grant_rate_with_interview
        result['examiner_grant_rate_without_interview'] = examiner_grant_rate_without_interview
        result['response_success_rate'] = response_success_rate
        result['interview_improvement_rate'] = interview_improvement_rate
        result['months'] = months
        return (result)

@app.route('/list_examiners')
@cache.cached(timeout=3600)
def get_names():
        ## Initializing the mongo connection
    connection_string = 'mongodb+srv://Zeevtest:Zeevtest@freship-fu97s.mongodb.net/test?retryWrites=true&w=majority'
    from bson.decimal128 import Decimal128
    from bson.codec_options import TypeCodec
    class DecimalCodec(TypeCodec):
        python_type = Decimal    # the Python type acted upon by this type codec
        bson_type = Decimal128   # the BSON type acted upon by this type codec
        def transform_python(self, value):
            """Function that transforms a custom type value into a type
            that BSON can encode."""
            return Decimal128(value)
        def transform_bson(self, value):
            """Function that transforms a vanilla BSON type value into our
            custom type."""
            return value.to_decimal()
    decimal_codec = DecimalCodec()

    today = date.today()
    cutoff_date = today - timedelta(days=70)

    from bson.codec_options import TypeRegistry
    type_registry = TypeRegistry([decimal_codec])
    from bson.codec_options import CodecOptions
    codec_options = CodecOptions(type_registry=type_registry)

    mongo_client = pymongo.MongoClient(connection_string)
    mydb = mongo_client["patents"]
    db = mongo_client["patents"]
    examiners_collection = mydb.get_collection("examiners_new" , codec_options=codec_options)
    return jsonify([(i['examiner']) for i in examiners_collection.find()])

@app.route('/search_app')
def search_app_endpoint():
    ## Initializing the mongo connection
    import requests

    headers = {
        'Content-type': 'application/json',
    }
    name = request.args['name']

    return jsonify(search_app(name))



def search_app(name):
    ## Initializing the mongo connection
    import requests

    headers = {
        'Content-type': 'application/json',
    }

    data = '{"searchText":"firstNamedApplicant:(' + name + ')","fl":"applId patentTitle firstNamedApplicant appExamName ","mm":"100%","df":"patentTitle","qf":"firstNamedApplicant ","facet":"false","sort":"applId asc","start":"0"}'
    print(data)
    while True:
        try:
            response = requests.post('https://ped.uspto.gov/api/queries', headers=headers, data=data)
            print(response.content)
            return (list(set([i['firstNamedApplicant'][0] for i in response.json()['queryResults']['searchResponse']['response']['docs']])))
        except:
            import traceback
            traceback.print_exc()


@app.route('/get_apps')
def get_apps_endpoint():
    ## Initializing the mongo connection
    import requests

    headers = {
        'Content-type': 'application/json',
    }
    name = request.args['name']
    page = int(request.args.get('page', 0))

    return jsonify(get_apps(name, page))

def get_apps(name, page):
    ## Initializing the mongo connection
    import requests

    headers = {
        'Content-type': 'application/json',
    }

    data = '{"searchText":"firstNamedApplicant:(' + name + ')","fl":"*","mm":"100%","df":"patentTitle","qf":"firstNamedApplicant ","facet":"false","sort":"appStatusDate desc","start":"' + str(page * 20) + '"}'
    return (requests.post('https://ped.uspto.gov/api/queries', headers=headers, data=data).json())

@app.route('/get_deadline')
def get_deadlines():
    ## Initializing the mongo connection
    import requests

    for row in get_rows():
        tuples = []
        headers = {
            'Content-type': 'application/json',
        }

        applicants = (search_app(row[0]))
        analyzed = []
        print(applicants)
        for applicant in applicants:
            applicant = applicant.strip()
            for i in range(0, 4):
                applications = get_apps(applicant, i)['queryResults']['searchResponse']['response']['docs']
                print(applicant, len(applications))
                for item in applications:
                    print('-----')
                    if 'transactions' in item:
                        transactions = item['transactions']
                        description = ''
                        lastEvent = ''
                        for i in reversed(range(len(transactions))):
                            transaction = (transactions[i]);
                            if (transaction['code'] == 'MCTFR' or transaction['code'] == 'MCTNF'):
                                lastEvent = transaction['recordDate'][:11]
                                description = transaction['description']
                                if(transaction['code'] == 'MCTFR'):
                                    description = 'Final Rejection'
                                else:
                                    description = 'Non-Final Rejection' 
                            if (transaction['code'] == 'A.NE' or transaction['code'] == 'SA..' or transaction['code'] == 'A.QU'):
                                lastEvent = ''
                                description = ''
                        if lastEvent:
                            deadline = datetime.datetime(int(lastEvent.split('-')[0]), int(lastEvent.split('-')[1]), int(lastEvent.split('-')[2]))
                            today = datetime.datetime.now()
                            diffDays = (today - deadline).days
                            print(item['applId'], lastEvent, diffDays)
                            if (diffDays < 0):
                                extension = "Deadline in the past!";
                                deadline = datetime.datetime(int(lastEvent.split('-')[0]), int(lastEvent.split('-')[1]), int(lastEvent.split('-')[2])); 

                            if (diffDays > 0 and diffDays <90):
                                extension = "No extension period";
                                deadline = datetime.datetime(int(lastEvent.split('-')[0]), int(lastEvent.split('-')[1]), int(lastEvent.split('-')[2])) + relativedelta(months=3)
                            if (diffDays >= 90 and diffDays <120):

                                extension = "1st extension";
                                deadline = datetime.datetime(int(lastEvent.split('-')[0]), int(lastEvent.split('-')[1]), int(lastEvent.split('-')[2])) + relativedelta(months=4)

                            if (diffDays >= 120 and diffDays <150):

                                extension = "2nd extension";
                                deadline = datetime.datetime(int(lastEvent.split('-')[0]), int(lastEvent.split('-')[1]), int(lastEvent.split('-')[2])) + relativedelta(months=5)

                            if (diffDays >= 150 and diffDays <180):

                                extension = "3rd extension";
                                deadline = datetime.datetime(int(lastEvent.split('-')[0]), int(lastEvent.split('-')[1]), int(lastEvent.split('-')[2])) + relativedelta(months=6)


                            if (diffDays >= 180) :

                                extension = "";
                            if item['patentTitle'] not in analyzed:
                                analyzed += [item['patentTitle']]
                                if (diffDays < 180):
                                    tuples += [((deadline - today).days,"%s application nears deadline %s in %s days with extension %s  for applicant %s<br/>" % (item['applId'], deadline, (deadline - today).days, extension, applicant))]
        tuples = sorted(tuples, key=lambda x: x[0])
        html = """\n\n<!DOCTYPE html\n    PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n\n<head>\n    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\n    <title>Demystifying Email Design</title>\n    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">\n</head>\n\n<body style="margin: 0; padding: 0; font-family: 'Roboto', sans-serif;">\n    <table border="0" cellpadding="0" cellspacing="0" width="100%" bgcolor="#FAFAFA">\n        <tr>\n            <td style="padding: 10px 0 30px 0; background-color: #FAFAFA;">\n                <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" bgcolor="#FAFAFA" style="border-collapse: collapse; background-color: #FAFAFA;">\n                    <tr>\n                        <td align="center"\n                            style="padding: 40px 0 30px 0; color: #306183; font-size: 22px; font-weight: bold;">\n                            <div>FRESH Weekly Alert</div>\n                        </td>\n                    </tr>\n                    <tr>\n                        <td style="padding: 40px 15px 0px 15px;">\n                            <table border="0" cellpadding="0" cellspacing="0" width="100%">\n                                <tr>\n                                    <td style="color: #000; font-size: 18px;">\n                                        <b>Dear """ + row[2] + """,</b>\n                                    </td>\n                                </tr>\n                                <tr>\n                                    <td style="color: #191A1C; font-size: 18px;">\n                                       <p>You have an alert set up to track U.S. office actions for "<span style="color: #FF5B3D; font-weight: bold;">""" + row[0] +"""</span>".</p> \n                                    </td>\n                                </tr>\n                                <tr>\n                                    <td style="color: #191A1C; font-size: 18px;">\n                                        <p style="margin: 0;">This week, we identified that there are <span style="color: #144160; font-weight: bold;">""" + str(len(tuples)) + """ pending office actions</span>.</p>\n                                    </td>\n                                </tr>\n                                <tr>\n                                    <td style="color: #FFFFFF; font-size: 18px; text-align: center; padding-top: 40px;">\n                                        <a href="insights.freship.io/index.html?company=""" + row[0] + """" style="display: inline-block; padding: 15px 20px; background-color: #FF5B3D; color: #FFFFFF; text-decoration: unset; border-radius: 10px; box-shadow: 0px 3.79861px 3.79861px rgba(0, 0, 0, 0.16);"><span style="color: #FFFFFF;">See pending office actions</span></a>\n                                    </td>\n                                </tr>\n                            </table>\n                        </td>\n                    </tr>\n                    <tr>\n                        <td>\n                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="padding: 40px 15px 40px 15px;">\n                                <tr>\n                                    <td style="color: #000; font-size: 14px; padding-top: 15px;">\n                                        <p>You can stop tracking Cambridge Enterprise at any time <a href=\"""" + "https://checkexaminer.herokuapp.com/unsubscribe?email=" + row[1] + "&company=" + row[0] + """\"target="_blank" style="color: #306183; text-decoration: underline; font-weight: bold;">here</a></p>                                     \n                                    </td>\n                                </tr>\n                                <tr>\n                                    <td style="color: #000; font-size: 14px; padding-top: 10px;">\n                                        <p style="color:#306183;">\n                                            <b>Best,</b> <br />\n                                            <b>Your Fresh team</b>\n                                        </p>\n                                    </td>\n                                </tr>\n                                <tr>\n                                    <td style="padding-top: 15px;">\n                                        <img src="http://fresh.fox-m.com/img/icons/second-logo.png" alt="logo">\n                                    </td>\n                                </tr>\n                            </table>\n                        </td>\n                    </tr>\n                </table>\n            </td>\n        </tr>\n    </table>\n</body>\n\n</html>\n"""
        send_email(row[1], html, "Weekly report of deadlines for company "+row[0])
    return jsonify({})

            

    

@app.route('/get_apps_by_id')
def get_apps_by_id():
    ## Initializing the mongo connection
    import requests

    headers = {
        'Content-type': 'application/json',
    }
    name = request.args['name']

    page = int(request.args.get('page', 0))

    data = '{"searchText":"applId:(' + name + ')","fl":"*","mm":"100%","df":"patentTitle","qf":"applId","facet":"false","sort":"appStatusDate desc","start":"' + str(page * 20) + '"}'
    print(data)
    while True:
        try:
            return jsonify(requests.post('https://ped.uspto.gov/api/queries', headers=headers, data=data).json())
        except:
            pass

@app.route('/email')
def email():
    sender_email = "freshipinsights@gmail.com"
    password = "freship#14insights"

    appNumber = request.args['appNumber']
    name = request.args['name']
    email = request.args['email']

    html = "<html><body>Hi "+name + "<br><br> You've requested application insights for application number " + appNumber +". We will aim to revert to you within 48 hours to " +  email + ". <br><br> Best Regards, <br>The Fresh Team</body></html>"

    send_email(email, html, "New Office Action - Analytics")
    send_email(email, html, "New Office Action - Analytics")
    return jsonify({})

def send_email(email, html, subject):
    sender_email = "freshipinsights@gmail.com"
    password = "freship#14insights"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = "Fresh Insights"
    message["Reply-to"] = email #"zeev@freship.com"
    #receiver_email = "zeev@freship.com"
    message["To"] = email          
    # Turn these into plain/html MIMEText objects
    part2 = MIMEText(html, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, [email], message.as_string())
    return jsonify({})

def send_email_with_image(email, html, subject):
    sender_email = "freshipinsights@gmail.com"
    password = "freship#14insights"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = "Fresh Insights"
    message["Reply-to"] = email #"zeev@freship.com"
    #receiver_email = "zeev@freship.com"
    message["To"] = email          
    # Turn these into plain/html MIMEText objects
    part2 = MIMEText(html, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2)

    fp = open('logo.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, [email], message.as_string())
    return jsonify({})

def get_cache_no(element):
    try:
        return json.load(open(element.replace('/','') + ".txt", "r"))
    except:
        return {}

@app.route('/temp')
def tempo():
    try:
        patent = request.args['patent']

        return jsonify([[i['term'], i['count']] for i in get_split.temp(patent)['widgets']['publications.cc']['terms']] + [[patent, patent]])
    except Exception as e:
        print(e)
        return {}

@app.route('/split_per_class')
def temp():
    try:
        classi = request.args['classi']

        return jsonify([[i['term'], i['count']] for i in get_split.ipc(classi)['widgets']['publications.cc']['terms']] + [[classi, classi]])
    except Exception as e:
        print(e)
        return {}

def get_cache(element):
    try:
        return json.load(open(element.replace('/','') + ".txt", "r"))
    except:
        result = {}
        result['timestamp'] = datetime.datetime.now().timestamp()
        write_cache(element, result)
        return {}

def write_cache(key, result):
    with open(key.replace('/','')  + '.txt', 'w') as outfile:
        result['timestamp'] = datetime.datetime.now().timestamp()
        json.dump(result, outfile)

def fetch_patent(patent):
    classes = []
    #print('Fetching patent', patent)
    fetched = False
    creds = base64.b64encode("VkIikoJMeoJKLPGGgAUWMl324QD81x8O:3TzRhnYc6ezNptjA".encode())
    headers = {'Authorization': 'Basic ' + creds.decode('UTF-8'), 'Content-Type': 'application/x-www-form-urlencoded'}
    url = 'https://ops.epo.org/3.2/auth/accesstoken'
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)

    myToken = response.json()["access_token"]

    header = {'Authorization': "Bearer " + myToken}
    from random import randint
    from time import sleep
    while not fetched:
        try:
            import urllib.parse

            myUrl = 'http://ops.epo.org/rest-services/published-data/search/abstract,biblio,full-cycle?q=num%3D' + patent + '&Range=1-100'
            response = requests.get(myUrl, headers=header)
            #print('resp', response.text)
            fetched = True
            import xmltodict, json
            o = xmltodict.parse(response.text)
            #print(response.text)
            biblio_data = o['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents'][0]['exchange-document']['bibliographic-data']
            pub_data = biblio_data['publication-reference']
            try:
                for ex_doc in o['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']:
                    try:
                        print('Fetching claims for ', ex_doc['exchange-document']['@country'], ex_doc['exchange-document']['@doc-number'])
                        myUrl = 'http://ops.epo.org/3.2/rest-services/published-data/publication/epodoc/'+ex_doc['exchange-document']['@country']+ ex_doc['exchange-document']['@doc-number']+'/claims'
                        response = requests.get(myUrl, headers=header)
                        fetched = True
                        import xmltodict, json
                        claims = xmltodict.parse(response.text)
                        #print('Claims:')
                        #for i in claims['ops:world-patent-data']['ftxt:fulltext-documents']['ftxt:fulltext-document']['claims']['claim']['claim-text']:
                        #    print(i)
                    except:
                        pass
            except Exception as e:
                print(e)
                pass
            #try:
            #    print('Patent title', o['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents'][0]['exchange-document']['bibliographic-data']['invention-title']['#text'])
            #except:
            #    print('Patent title:', o['ops:world-patent-data']['exchange-documents']['exchange-document']['bibliographic-data']['invention-title']['#text'])
            try:
                for cl in (biblio_data['classifications-ipcr']['classification-ipcr']):
                    x = ((cl['text']))
                    x = "".join(x.split('   ')[:3])
                    classes = classes + [x.replace(' ', '')]
            except:
                x = ((biblio_data['classifications-ipcr']['classification-ipcr']['text']))
                x = "".join(x.split('   ')[:3])
                classes = classes + [x.replace(' ', '')]
            return classes
        except Exception as e:
            import traceback
            traceback.print_exc()
            print('Exception when fetching patent ',e)
            pass

@app.route('/split')
def split():
    patent_number = request.args['patent_number']
    applicant = request.args['applicant']
    classes = fetch_patent(patent_number)
    executor.submit(get_split, patent_number, applicant)
    res = {}
    for cl in classes + [applicant]:
        res[cl] = get_cache_no(cl)
    print(res)
    import json
    return res

@app.route('/get_epo_records')
def get_epo_records():
    pa = request.args['pa']
    page_no = int(request.args['page_no'])
    return jsonify(get_split.get_epo_records(pa, page_no))


@app.route('/subscribe')
def subscribe():
    email = request.args['email']
    company = request.args['company']
    text = request.args['text']

    try:
        conn = psycopg2.connect(host='ec2-34-231-56-78.compute-1.amazonaws.com',
                                             database='d4g1rkpppj5adf',
                                             user='igsgvulkrsftdl',
                                             port=5432,
                                             password='a25b712e2b4fadaa145685d089fead23e8e3d53fa45425312e98cf1c8a1dcbe9')
        # create a cursor
        cur = conn.cursor()
        
    # execute a statement
        print("INSERT INTO schedules (company, email, name) VALUES ('%s', '%s', '%s')" % (company, email, text))
        cur.execute("INSERT INTO schedules (company, email, name) VALUES ('%s', '%s', '%s')" % (company, email, text))
        # display the PostgreSQL database server version
       
    # close the communication with the PostgreSQL
        conn.commit()
        conn.close()

    except Error as e:
        print("Error while connecting to MySQL", e)
    html = "<html><body>Hi,<br><br> You've subscribed to being alerted of upcoming deadlines for application for " + company +". You will henceforth receive the reports every Monday. Click this <a href='https://checkexaminer.herokuapp.com/unsubscribe?email=" + email + "&company=" + company + "' > link </a> to unsubscribe. <br/> <img src='http://fresh.fox-m.com/img/icons/second-logo.png' alt='logo'></body></html>"

    send_email(email, html, "Deadline subscription notice")
    return jsonify({})


@app.route('/unsubscribe')
def unsubscribe():
    email = request.args['email']
    company = request.args['company']

    try:
        conn = psycopg2.connect(host='ec2-34-231-56-78.compute-1.amazonaws.com',
                                             database='d4g1rkpppj5adf',
                                             user='igsgvulkrsftdl',
                                             port=5432,
                                             password='a25b712e2b4fadaa145685d089fead23e8e3d53fa45425312e98cf1c8a1dcbe9')
        # create a cursor
        cur = conn.cursor()
        
    # execute a statement
        print("delete from schedules where company like '%" + company+"%' and email='" + email+"%';" )
        cur.execute("delete from schedules where company like '%" + company+"%' and email like'%" + email+ "%';" )
        # display the PostgreSQL database server version
       
    # close the communication with the PostgreSQL
        conn.commit()
        conn.close()

    except Error as e:
        print("Error while connecting to MySQL", e)
    html = "<html><body>Hi,<br><br> You've unsubscribed to being alerted of upcoming deadlines for application for " + company +". You will henceforth not receive the reports every Monday. <br/><img src='http://fresh.fox-m.com/img/icons/second-logo.png' alt='logo'></body></html>"

    send_email(email, html, "Deadline unsubscription notice")
    return jsonify("Successfuly unscubscribed!")


def get_rows():

    try:
        conn = psycopg2.connect(host='ec2-34-231-56-78.compute-1.amazonaws.com',
                                             database='d4g1rkpppj5adf',
                                             user='igsgvulkrsftdl',
                                             port=5432,
                                             password='a25b712e2b4fadaa145685d089fead23e8e3d53fa45425312e98cf1c8a1dcbe9')
        # create a cursor
        cur = conn.cursor()
        
    # execute a statement
        print("select * from schedules;")
        cur.execute("select * from schedules;")
        # display the PostgreSQL database server version
        rows = cur.fetchall() 
       
    # close the communication with the PostgreSQL
        conn.commit()
        conn.close()
        return rows

    except Error as e:
        print("Error while connecting to MySQL", e)

    return jsonify({})

import requests
from lxml.html import fromstring
def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

def get_splito(patent_number, applicant):
    print(patent_number, applicant)
    classes = []

    from datetime import timedelta, date, datetime

    url = 'https://ops.epo.org/3.2/auth/accesstoken'
    data = {"grant_type": "client_credentials"}

    creds = base64.b64encode("VkIikoJMeoJKLPGGgAUWMl324QD81x8O:3TzRhnYc6ezNptjA".encode())
    headers = {'Authorization': 'Basic ' + creds.decode('UTF-8'), 'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(url, headers=headers, data=data)

    myToken = response.json()["access_token"]

    header = {'Authorization': "Bearer " + myToken}

    WINDOW = 1000

    def daterange(start_date, n):
        print(start_date, n, start_date- timedelta(days=(n)))
        return start_date - timedelta(days=(n))

    def fetch_apps(idx, WINDOW):
        if(idx.strftime("%Y%m%d") < '19800101'):
            return
        fetched = False
        from random import randint
        from time import sleep
        sleep(randint(0,5))
        print(query)
        while not fetched:
            try:
                print('Fetching applications for date range:', idx.strftime("%Y%m%d")+"-"+daterange(idx, WINDOW - 1).strftime("%Y%m%d"), query)
                myUrl = 'http://ops.epo.org/rest-services/published-data/search/abstract,biblio,full-cycle?q=' + query + 'pd%3D'+idx.strftime("%Y%m%d")+"-"+daterange(idx, WINDOW - 1).strftime("%Y%m%d")+'&Range=1-100'
                import time
                proxies = get_proxies()
                response = requests.get(myUrl, headers=header)
                print(response.text)
                import xmltodict, json
                o = xmltodict.parse(response.text)
                #print(response.text)
                if 'fault' in o:
                    if(o['fault']['code'] == 'CLIENT.RobotDetected'):
                        print('Throttled by EPO', query)
                        raise "oops"
                    if(o['fault']['code'] == 'SERVER.EntityNotFound'):
                        fetched = True
                        print('No applications were filed in daterange ', idx.strftime("%Y%m%d")+"-"+daterange(idx, WINDOW - 1).strftime("%Y%m%d"), query)
                        break
                if 'ops:world-patent-data' in o:
                    try:
                        total_records = int(o['ops:world-patent-data']['ops:biblio-search']['@total-result-count'])
                        begin = idx.strftime("%Y%m%d")
                        end = daterange(idx, WINDOW - 1).strftime("%Y%m%d")
                        print("In this daterange", idx.strftime("%Y%m%d")+"-"+daterange(idx, WINDOW - 1).strftime("%Y%m%d"), 'we have this many records', total_records, query)
                        print(begin, end, begin > end, query)
                        if(#total_records > 100 and and int(begin) - int(end) > 5
                            begin > end ):
                            print("WARNING: For interval", idx,'-', daterange(idx, WINDOW - 1), 'we have more than 100, namely',total_records, '. EPO Api only returns first 100 for a given query so we disregarded', total_records - 100, 'in calculations. Choosing smaller window.', query)
                            fetch_apps(idx, WINDOW/2)
                            if len(all_apps) < APPS_TO_ANALYSE:
                                fetch_apps(daterange(idx, WINDOW/2), WINDOW/2)
                            fetched = True
                        else:
                            reg_doc = o['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']
                            try:
                                if(reg_doc.keys()):
                                    all_apps.append(reg_doc)
                            except:
                                try:
                                    for datum in (o['ops:world-patent-data']['ops:biblio-search']['ops:search-result']['exchange-documents']):
                                        all_apps.append(datum)
                                except:
                                    pass
                            fetched = True

                    except Exception as e:
                        import time
                        interval = randint(0,10)
                        import traceback
                        traceback.print_exc()
                        print("Exception: ", e, o, ' waiting',interval,' seconds to retry', query)
                        time.sleep(interval)
            except Exception as e:
                import time
                interval = randint(10,20)
                print("Exception: ", e, ' waiting',interval,' seconds to retry', query)
                time.sleep(randint(10,20))


    start_date = date(2013, 1, 1)
    end_date = date(2015, 6, 2)
    i = 0
    date = datetime.now()
    all_apps = []
    results = []
    def to_infinity():
        index = 0
        while len(all_apps) < APPS_TO_ANALYSE:
            yield index
            index += 1
        raise "Ooops"
    NUM_OF_THREADS = 10
    delta = NUM_OF_THREADS
    classes = fetch_patent(patent_number)
    classes = [applicant] + classes
    for cl in classes:
        res = get_cache(cl)
        if 'timestamp' in res and datetime.now().timestamp() - float(res['timestamp']) < 3600:
            continue
        all_apps = []
        print('Fetching split for classification',cl)
        cl.replace(' ', '')
        print()
        if '/' in str(cl):
            try:
                query = 'ic%3D' + cl[:cl.find('/')]+","
            except:
                query = 'ic%3D' + cl['text'][:cl['text'].find('/')]+","
        else:
            query = 'pa%3D' + cl + ','
        print(query)
        while len(all_apps) < APPS_TO_ANALYSE and date.strftime("%Y%m%d") > '19800101':
            try:
                fetch_apps(date, delta * WINDOW)
                delta += NUM_OF_THREADS
                date = daterange(date, WINDOW)
                print('Fetched up to day ', date, len(all_apps), ' records analysed so far')
            except KeyboardInterrupt:
                break
        families = []
        count = {}
        count_all = 0
        all_apps = all_apps[:APPS_TO_ANALYSE]
        for app in all_apps:
            family = app['exchange-document']
            if family not in families:
                for idx in 'exchange-document.bibliographic-data.publication-reference.document-id.country'.split('.'):
                    try:
                        app = app[idx]
                    except:
                        app = app[0][idx]
                if app not in count:
                    count[app] = 0
                count[app] = count[app] + 1
                count_all += 1
                families += [family]
            else:
                pass

        print('SPLIT PER COUNTRY for classification', cl, ':')
        try:
            for key in count:
                res[key] = count[key]*100.0/count_all
            write_cache(cl, res)
        except:
            import traceback
            traceback.print_exc()

def add_months(sourcedate, months):
     month = sourcedate.month - 1 + months
     year = sourcedate.year + month // 12
     month = month % 12 + 1
     day = min(sourcedate.day, calendar.monthrange(year,month)[1])
     return datetime.date(year, month, day)

@app.route('/fp')
def fp():
#from datetime import timedelta, date, datetime
    patent = request.args['patent']

    url = 'https://ops.epo.org/3.2/auth/accesstoken'
    data = {"grant_type": "client_credentials"}

    creds = base64.b64encode("VkIikoJMeoJKLPGGgAUWMl324QD81x8O:3TzRhnYc6ezNptjA".encode())
    headers = {'Authorization': 'Basic ' + creds.decode('UTF-8'), 'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(url, headers=headers, data=data)

    myToken = response.json()["access_token"]

    header = {'Authorization': "Bearer " + myToken}
    classes = []
    print('Fetching patent', patent)
    fetched = False
    from random import randint
    from time import sleep

    title = "Undetected"
    applicant = "Undetected"
    first_inventor = "Undetected"
    first_deadline_30 = "Undetected"
    application_reference = "Undetected"
    while not fetched:
        try:
            myUrl = 'http://ops.epo.org/rest-services/published-data/publication/epodoc/' + patent
            response = requests.get(myUrl, headers=header)
            print(response.text)
            fetched = True
            import xmltodict, json

            application = xmltodict.parse(response.text).get("ops:world-patent-data").get("exchange-documents").get("exchange-document")
            try:
                bibliographic_data = application.get("bibliographic-data")
            except:
                bibliographic_data = application[0].get("bibliographic-data")


            application_reference = str(bibliographic_data.get("application-reference").get("document-id")[1].get("doc-number"))
            application_reference = "PCT/" + application_reference[6:8] + application_reference[2:6] + "/" + "0" + application_reference[8:]
            priority_claims = bibliographic_data.get("priority-claims").get("priority-claim")
            try: 
               for k in range (0,len(priority_claims)):
            # #        print (priority_claims)
            # #        priority_claim=priority_claims[0].get("document-id")
                if "document-id" in priority_claims:
                   priority_claim=priority_claims.get("document-id")
                else:    
                   priority_claim=priority_claims[0].get("document-id")
      
                for l in range (0,len(priority_claim)):
                   priority_claim_type = priority_claim[l]
                   if "date" in priority_claim_type:
                     earliest_priority = priority_claim_type.get("date")
                     earliest_priority_year = int(earliest_priority[0:4])
                     earliest_priority_month = int(earliest_priority[4:6])
                     earliest_priority_day = int(earliest_priority[6:8])
                     earliest_priority = datetime.date(earliest_priority_year,earliest_priority_month,earliest_priority_day)                     
                     first_deadline_30 = add_months(earliest_priority,30)

            except KeyError:
                print ("error")

            
            applicant = bibliographic_data.get("parties").get("applicants").get("applicant")[0].get("applicant-name").get("name")

            first_inventor = bibliographic_data.get("parties").get("inventors").get("inventor")[0].get("inventor-name").get("name")
            title = bibliographic_data.get("invention-title")[1].get("#text")

            print (application_reference + "," + applicant + "," + str(earliest_priority) + "," + str(first_deadline_30) + "," + title)

            try:
                for classifications in bibliographic_data.get("classifications-ipcr").get("classification-ipcr"):
                    class_text = ((classifications['text']))
                    class_text = "".join(class_text.split('   ')[:3])
                    classes = classes + [class_text.replace(' ', '')]
            except:
                class_text = bibliographic_data.get("classifications-ipcr").get("classification-ipcr").get("text")
                class_text = "".join(class_text.split('   ')[:3])
                classes = classes + [class_text.replace(' ', '')]

            print (classes)
            # CPC translation to words is somewhere here: https://publication.epo.org/raw-data/product?productId=71

        except Exception as e:
            import traceback
            traceback.print_exc()
            print('Exception when fetching patent ',e)
            pass

    print('now fetching claims', patent)
    fetched = False
    claims_num = "Undetected"
    independent_claims = "Undetected"
    total_words = "Undetected"
    num_of_words_in_claims = "Undetected"
    while not fetched:
        try:
            myUrl = 'http://ops.epo.org/rest-services/published-data/publication/epodoc/' + patent + "/claims"
            response = requests.get(myUrl, headers=header)
            fetched = True
            claims = xmltodict.parse(response.text).get("ops:world-patent-data").get("ftxt:fulltext-documents").get("ftxt:fulltext-document").get("claims").get("claim").get("claim-text")
            
            num_of_words_in_claims = len(claims.split())
            claims = claims.split('\n')
            claims_num=0
            independent_claims = 0
            for i in range (0,len(claims)):
                if (claims[i][0] == "1" or claims[i][0]=="2" or claims[i][0]=="3" or claims[i][0]=="4" or claims[i][0]=="5" or claims[i][0]=="6" or claims[i][0]=="7" or claims[i][0]=="8" or claims[i][0]=="9"):  #if the paragraph doesn't start with a number, it is not a claim and shouldn't be counted.
                    claims_num=claims_num+1
                    if "claim" not in claims[i]:
                        independent_claims = independent_claims + 1

        except Exception as e:
            import traceback
            traceback.print_exc()
            print('Exception when fetching patent ',e)
            pass

    print (claims_num)
    print (independent_claims)

    print('now fetching description', patent)
    fetched = False
    while not fetched:
        try:
            myUrl = 'http://ops.epo.org/rest-services/published-data/publication/epodoc/' + patent + "/description"
            response = requests.get(myUrl, headers=header)
            fetched = True
            description = xmltodict.parse(response.text).get("ops:world-patent-data").get("ftxt:fulltext-documents").get("ftxt:fulltext-document").get("description").get("p")
            description = str(description)
            num_of_words_in_description = len(description.split())
        except Exception as e:
            import traceback
            traceback.print_exc()
            print('Exception when fetching patent ',e)
            pass

    print('now fetching pages and images', patent)
    fetched = False
    total_p = "Undetected"
    claims_p = "Undetected"
    drawings_p = "Undetected"
    description_p = "Undetected"
    description_start_page = "Undetected"
    description_end_page = "Undetected"
    drawings_start_page = "Undetected"
    drawings_end_page = "Undetected"
    claims_start_page = "Undetected"
    claims_end_page = "Undetected"
    search_start_page = "Undetected"
    while not fetched:
        try:
            myUrl = 'http://ops.epo.org/rest-services/published-data/publication/epodoc/' + patent + ".A1/images"
            response = requests.get(myUrl, headers=header)
            print(response.text)
            fetched = True
            images_data = xmltodict.parse(response.text).get("ops:world-patent-data").get("ops:document-inquiry").get("ops:inquiry-result").get("ops:document-instance")

            for id in range (0,len(images_data)):
                image_data = images_data[id]
                if image_data.get("@desc")=="FullDocument":
                    total_p = image_data.get("@number-of-pages")
                                        
                    image_data_doc_sections = image_data.get("ops:document-section")
                    for dc in range (0,len(image_data_doc_sections)):
                      doc_section = image_data_doc_sections[dc] 
                      doc_section_name = doc_section.get("@name")
                      if doc_section_name == "ABSTRACT":
                         abstract_page = int(doc_section.get("@start-page"))  
                      if doc_section_name == "CLAIMS":
                          claims_start_page = int(doc_section.get("@start-page"))
                          description_end_page = claims_start_page - 1     
                      if doc_section_name == "DESCRIPTION":
                          description_start_page = int(doc_section.get("@start-page"))
                      if doc_section_name == "DRAWINGS":
                          drawings_start_page = int(doc_section.get("@start-page"))
                          claims_end_page = drawings_start_page - 1            
                      if doc_section_name == "SEARCH_REPORT":
                          search_start_page = int(doc_section.get("@start-page")) 
                          drawings_end_page = search_start_page - 1 
                
            if search_start_page == 0:
                    search_start_page = total_p
                    drawings_end_page = search_start_page - 1
            claims_p = claims_end_page - claims_start_page +1
            description_p = description_end_page - description_start_page +1
            drawings_p = drawings_end_page - drawings_start_page +1
            total_words = num_of_words_in_description+num_of_words_in_claims

        except Exception as e:
            import traceback
            traceback.print_exc()
            print('Exception when fetching patent ',e)
            pass


    return jsonify([total_words,num_of_words_in_claims,claims_num,independent_claims,title,applicant,first_inventor,str(first_deadline_30),classes,total_p, claims_p,drawings_p,description_p,application_reference, [get_split.get_class_text(cl) for cl in classes]])

