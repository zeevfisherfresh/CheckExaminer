from email.mime.text import MIMEText
import ssl
import smtplib
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
        password = "freship14insights"

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
def search_app():
    ## Initializing the mongo connection
    import requests

    headers = {
        'Content-type': 'application/json',
    }
    name = request.args['name']

    data = '{"searchText":"firstNamedApplicant:(' + name + ')","fl":"applId patentTitle firstNamedApplicant appExamName ","mm":"100%","df":"patentTitle","qf":"firstNamedApplicant ","facet":"false","sort":"applId asc","start":"0"}'
    print(data)
    while True:
        try:
            response = requests.post('https://ped.uspto.gov/api/queries', headers=headers, data=data)
            print(response.content)
            return jsonify(list(set([i['firstNamedApplicant'][0] for i in response.json()['queryResults']['searchResponse']['response']['docs']])))
        except:
            import traceback
            traceback.print_exc()


@app.route('/get_apps')
def get_apps():
    ## Initializing the mongo connection
    import requests

    headers = {
        'Content-type': 'application/json',
    }
    name = request.args['name']

    page = int(request.args.get('page', 0))

    data = '{"searchText":"firstNamedApplicant:(' + name + ')","fl":"*", "fq" : ["appStatus:\\\"Final Rejection Mailed\\\",\\\"Non Final Action Mailed\\\""],"mm":"100%","df":"patentTitle","qf":"firstNamedApplicant ","facet":"false","sort":"appStatusDate desc","start":"' + str(page * 20) + '"}'
    print(data)
    print(requests.post('https://ped.uspto.gov/api/queries', headers=headers, data=data).json())
    return jsonify(requests.post('https://ped.uspto.gov/api/queries', headers=headers, data=data).json())

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
    sender_email = "transcribe.upwork.test@gmail.com"
    password = "TestUser#95"

    appNumber = request.args['appNumber']
    name = request.args['name']
    email = request.args['email']

    message = MIMEMultipart("alternative")
    message["Subject"] = "New Office Action - Analytics"
    message["From"] = "Fresh Insights"
    message["Reply-to"] = email #"zeev@freship.com"
    #receiver_email = "zeev@freship.com"
    message["To"] = email                                                    
    # Create the plain-text and HTML version of your message
    reporting_text = 'arek'
    notification_recipient_name = name
    text = reporting_text
    html = "<html><body>Hi "+name + "<br><br> You've requested application insights for application number " + appNumber +". We will aim to revert to you within 48 hours to " +  email + ". <br><br> Best Regards, <br>The Fresh Team</body></html>"
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, [email], message.as_string())

        server.sendmail(sender_email, ["zeev@freship.com" ], message.as_string())
    return jsonify({})
