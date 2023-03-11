import urllib.request
import urllib.parse
from urllib.error import HTTPError
import json
from datetime import datetime
import os
import pprint as pp


class Daily_sales_report_api():
    def __init__(
            self,
            api_host,
            auth):
        self.api_host = api_host
        self.auth = auth
        self.api_end_point = 'wp-json/gp-daily-report/v1/sales_report/'

        self.url = f'https://{self.api_host}/{self.api_end_point}'
        self.date_format = '%Y-%m-%d'

    def _get_params(self):
        return {
            'date': self.report_date_str
        }

    def _get_request_url(self):
        params = urllib.parse.urlencode(
            self._get_params(),
            quote_via=urllib.parse.quote)
        return self.url + '?' + params


    def fetch_data(self, report_date_str):
        self.report_date_str = report_date_str
        data = []
        url = self._get_request_url()
        request = urllib.request.Request(url)
        request.add_header('Authorization', self.auth)
        try:
            with urllib.request.urlopen(request) as request_url:
                data = json.loads(request_url.read().decode())
        except HTTPError as e:
            if e.code != 200:
                pp.pprint ( e.readline() )
        return data
