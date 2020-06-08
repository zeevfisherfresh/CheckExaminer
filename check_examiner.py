
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
import datetime
from datetime import date, timedelta
import pprint
from pprint import pprint
import json
import pymongo
from decimal import *
from flask import request
app = Flask(__name__)
from flask_cors import CORS, cross_origin
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/')
@app.route('/data')
def hello_world():
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

    examiner_name = request.args['name']
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

        for i in range (0,13):
            if (failed_month[i] !=0):
                month_stat[i] = successful_month[i] / (successful_month[i] + failed_month [i])
                month_stat[i] = "%.0f%%" % (100 * month_stat[i])
                if (i !=0):
                    reporting_text = reporting_text + str(get_month_text(i)) + ": " + month_stat[i] + " | "

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
        return (html)

@app.route('/list_examiners')
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
    from flask import jsonify
    return jsonify([(i['examiner']) for i in examiners_collection.find()])
