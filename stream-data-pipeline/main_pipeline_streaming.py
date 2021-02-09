from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import pubsub_v1
from google.cloud import bigquery
import apache_beam as beam
import logging
import argparse
import sys
import re

PROJECT = "user-logs-237110"
schema = 'fullname:STRING, time_local:STRING, user_name:STRING, email:STRING, iban:STRING, ipv6:STRING, mac_address:STRING, address:STRING'
TOPIC = "projects/user-logs-237110/topics/userlogs"


def regex_clean(data):
    PATTERNS = [r'(^\S+\.[\S+\.]+\S+)\s', r'(?<=\[).+?(?=\])',
                r'\"(\S+)\s(\S+)\s*(\S*)\"', r'\s(\d+)\s', r"(?<=\[).\d+(?=\])",
                r'\"[A-Z][a-z]+', r'\"(http|https)://[a-z]+.[a-z]+.[a-z]+']
    result = []
    for match in PATTERNS:
        try:
            reg_match = re.search(match, data).group()
            if reg_match:
                result.append(reg_match)
            else:
                result.append(" ")
        except:
            print("There was an error with the regex search")
    result = [x.strip() for x in result]
    result = [x.replace('"', "") for x in result]
    res = ','.join(result)
    return res


class Split(beam.DoFn):

    def process(self, element):
        from datetime import datetime
        element = element.split(",")
        d = datetime.strptime(element[1], "%d/%b/%Y:%H:%M:%S")
        date_string = d.strftime("%Y-%m-%d %H:%M:%S")

        return [{
            'fullname': element[0],
            'time_local': date_string,
            'user_name': element[2],
            'email': element[3],
            'iban': element[4],
            'ipv6': element[5],
            'mac_address': element[6],
            'address': element[7]

        }]


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_topic")
    parser.add_argument("--output")
    known_args = parser.parse_known_args(argv)

    p = beam.Pipeline(options=PipelineOptions())

    (p
     | 'ReadData' >> beam.io.ReadFromPubSub(topic=TOPIC).with_output_types(bytes)
     | "Decode" >> beam.Map(lambda x: x.decode('utf-8'))
     | "Clean Data" >> beam.Map(regex_clean)
     | 'ParseCSV' >> beam.ParDo(Split())
     | 'WriteToBigQuery' >> beam.io.WriteToBigQuery('{0}:userlogs.logdata'.format(PROJECT), schema=schema,
                                                    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
     )
    result = p.run()
    result.wait_until_finish()


if __name__ == '__main__':
    logger = logging.getLogger().setLevel(logging.INFO)
    main()