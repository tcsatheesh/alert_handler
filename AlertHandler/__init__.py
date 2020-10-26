import json
import logging

import azure.functions as func

from azure_monitor import AzureMonitorSpanExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import urllib

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

instrumentation_key = os.environ["APPINSIGHTS_INSTRUMENTATIONKEY"]

# SpanExporter receives the spans and send them to the target location
exporter = AzureMonitorSpanExporter(connection_string='InstrumentationKey=' +
                                    instrumentation_key, )

span_processor = BatchExportSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# connection_string = os.environ["SQL_CONNECTION_STRING"]

# params = urllib.parse.quote_plus(
#     connection_string)  # urllib.parse.quote_plus for python 3

# conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
# engine = create_engine(conn_str, echo=True)

# SQLAlchemyInstrumentor().instrument(
#     engine=engine,
#     service="GenerateTimeSeriesData",
# )


def main(req: func.HttpRequest,
         outputblob: func.Out[func.InputStream]) -> func.HttpResponse:
    logging.info(
        'Version 1.9: Python HTTP trigger function processed a request.')    
    for key,value in req.headers.items():
        logging.info("Request headers: %s=%s", key, value)    
    req_json = req.get_json()
    outputblob.set(json.dumps(req_json))
    return func.HttpResponse(
        "This HTTP triggered function executed successfully.", status_code=200)
