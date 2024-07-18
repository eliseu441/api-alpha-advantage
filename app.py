#substituir os.getenv('API_KEY') por 'KG769NM8V32KAQ20' para usar key de testes
import os 
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from alpha_vantage.fundamentaldata import FundamentalData

load_dotenv()
getData = (
"SELECT id, build, country, year, file_name, description FROM public.tbf_buildings;"
)
app = Flask(__name__)
#url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(database="HERMES", user="hermesUsers", password="123", host="db-projects.cjukum6eu94v.us-east-2.rds.amazonaws.com", port=5432)


@app.get('/')
def getAll():
    with connection.cursor() as cursor:
        cursor.execute(getData)
        query_result = cursor.fetchall()
        for x in query_result:
            print(x)
        return query_result

@app.get('/incomeStatement')
def incomeStatement():
    fd = FundamentalData(key = os.getenv('API_KEY'))
    # Get Company Overview
    # ticker example 'AAPL'
    ticker = request.args.get('ticker')
    result = fd.get_income_statement_annual(symbol=ticker)
    company_overview = result[0] if result else pd.DataFrame()
    company_overview_json = company_overview.to_dict(orient='records')
    return jsonify(company_overview_json)

@app.get('/cashFlow')
def cashFlow():
    fd = FundamentalData(key = os.getenv('API_KEY'))
    # Get Company Overview
    # ticker example 'AAPL'
    ticker = request.args.get('ticker')
    result = fd.get_cash_flow_annual(symbol=ticker)
    company_overview = result[0] if result else pd.DataFrame()
    company_overview_json = company_overview.to_dict(orient='records')
    return jsonify(company_overview_json)