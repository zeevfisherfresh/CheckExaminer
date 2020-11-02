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

APPS_TO_ANALYSE = 1000
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
                            if item['applId'] not in analyzed:
                                analyzed += [item['applId']]
                                if (diffDays < 180):
                                    tuples += [((deadline - today).days,"%s application nears deadline %s in %s days with extension %s  for applicant %s<br/>" % (item['applId'], deadline, (deadline - today).days, extension, applicant))]
        tuples = sorted(tuples, key=lambda x: x[0])
        html = '<p style="text-align:center;color:blue;font-weight: bold;">Fresh weekly alert</p>' + \
            '<b> Hello</b>, <br> <br>'+ \
            'You have  an alert setup to track U.S. office actions for company <span style="color:orange;font-weight: bold;"> ' + row[0] + '</span>. <br/> <br/>'+ \
            'This week we\'ve identified that there are <span style="text-align:center;color:blue;font-weight: bold;">' + row[0] + ' pending office actions</span>'+ \
            '<p style="text-align:center;color:blue;font-weight: bold;"></p>'+ \
            "Click this <a href='https://checkexaminer.herokuapp.com/unsubscribe?email=" + row[1] + "&company=" + row[0] + "' > link </a> to unsubscribe." \
            "<p style='color:blue;font-weight: bold;'>Best, <br>"+ \
            'your Fresh Team</p>' 
        html += "<br/> <img src='cid:image1'></body></html>"
        send_email_with_image(row[1], html, "Weekly report of deadlines for company "+row[0])
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
    sender_email = "transcribe.upwork.test@gmail.com"
    password = "TestUser#95"

    appNumber = request.args['appNumber']
    name = request.args['name']
    email = request.args['email']

    html = "<html><body>Hi "+name + "<br><br> You've requested application insights for application number " + appNumber +". We will aim to revert to you within 48 hours to " +  email + ". <br><br> Best Regards, <br>The Fresh Team</body></html>"

    send_email(email, html, "New Office Action - Analytics")
    send_email(email, html, "New Office Action - Analytics")
    return jsonify({})

def send_email(email, html, subject):
    sender_email = "transcribe.upwork.test@gmail.com"
    password = "TestUser#95"

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
    sender_email = "transcribe.upwork.test@gmail.com"
    password = "TestUser#95"

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


@app.route('/subscribe')
def subscribe():
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
        print("INSERT INTO schedules (company, email) VALUES (%s, %s)" % (company, email))
        cur.execute("INSERT INTO schedules (company, email) VALUES ('%s', '%s')" % (company, email))
        # display the PostgreSQL database server version
       
    # close the communication with the PostgreSQL
        conn.commit()
        conn.close()

    except Error as e:
        print("Error while connecting to MySQL", e)
    html = "<html><body>Hi,<br><br> You've subscribed to being alerted of upcoming deadlines for application for " + company +". You will henceforth receive the reports every Monday. Click this <a href='https://checkexaminer.herokuapp.com/unsubscribe?email=" + email + "&company=" + company + "' > link </a> to unsubscribe. <br/> <img src='cid:image1'></body></html>"

    send_email_with_image(email, html, "Deadline subscription notice")
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
        print("delete from schedules where company=\'%s\' and email=\'%s\';" % (company, email))
        cur.execute("delete from schedules where company like \'\%%s\%\' and email=\'\%%s\%\';" % (company, email))
        # display the PostgreSQL database server version
       
    # close the communication with the PostgreSQL
        conn.commit()
        conn.close()

    except Error as e:
        print("Error while connecting to MySQL", e)
    html = "<html><body>Hi,<br><br> You've unsubscribed to being alerted of upcoming deadlines for application for " + company +". You will henceforth not receive the reports every Monday. <br/><img src='cid:image1'></body></html>"

    send_email_with_image(email, html, "Deadline unsubscription notice")
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

def get_split(patent_number, applicant):
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
                print('Fetching applications for date range:', idx.strftime("%Y%m%d")+"-"+daterange(idx, WINDOW - 1).strftime("%Y%m%d"))
                myUrl = 'http://ops.epo.org/rest-services/published-data/search/abstract,biblio,full-cycle?q=' + query + 'pd%3D'+idx.strftime("%Y%m%d")+"-"+daterange(idx, WINDOW - 1).strftime("%Y%m%d")+'&Range=1-100'
                response = requests.get(myUrl, headers=header)
                import xmltodict, json
                o = xmltodict.parse(response.text)
                #print(response.text)
                if 'fault' in o:
                    if(o['fault']['code'] == 'CLIENT.RobotDetected'):
                        print('Throttled by EPO')
                        raise "oops"
                    if(o['fault']['code'] == 'SERVER.EntityNotFound'):
                        fetched = True
                        print('No applications were filed in daterange ', idx.strftime("%Y%m%d")+"-"+daterange(idx, WINDOW - 1).strftime("%Y%m%d"))
                        break
                if 'ops:world-patent-data' in o:
                    try:
                        total_records = int(o['ops:world-patent-data']['ops:biblio-search']['@total-result-count'])
                        begin = idx.strftime("%Y%m%d")
                        end = daterange(idx, WINDOW - 1).strftime("%Y%m%d")
                        print("In this daterange", idx.strftime("%Y%m%d")+"-"+daterange(idx, WINDOW - 1).strftime("%Y%m%d"), 'we have this many records', total_records)
                        print(begin, end, begin > end)
                        if(total_records > 100 and begin > end and int(begin) - int(end) > 5):
                            print("WARNING: For interval", idx,'-', daterange(idx, WINDOW - 1), 'we have more than 100, namely',total_records, '. EPO Api only returns first 100 for a given query so we disregarded', total_records - 100, 'in calculations. Choosing smaller window.')
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
                        interval = randint(30,60)
                        import traceback
                        traceback.print_exc()
                        print("Exception: ", e, o, ' waiting',interval,' seconds to retry')
                        time.sleep(interval)
            except Exception as e:
                import time
                interval = randint(30,60)
                print("Exception: ", e, ' waiting',interval,' seconds to retry')
                time.sleep(interval)


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


