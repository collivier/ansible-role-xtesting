#!/usr/bin/env python

# pylint: disable=missing-docstring

import json
import os
import sys
import time

import requests

from xtesting.core import testcase


class Weather(testcase.TestCase):

    url = "https://samples.openweathermap.org/data/2.5/weather"
    city_name = "London,uk"
    app_key = "439d4b804bc8187953eb36d2a8c26a02"

    def run(self, **kwargs):
        try:
            self.start_time = time.time()
            req = requests.get("{}?q={}&&appid={}".format(
                self.url, self.city_name, self.app_key))
            req.raise_for_status()
            data = req.json()
            os.makedirs(self.res_dir, exist_ok=True)
            with open('{}/dump.txt'.format(self.res_dir), 'w+') as report:
                json.dump(data, report, indent=4, sort_keys=True)
            for key in kwargs:
                if data["main"][key] > kwargs[key]:
                    self.result = self.result + 100/len(kwargs)
            self.stop_time = time.time()
        except Exception:  # pylint: disable=broad-except
            print("Unexpected error:", sys.exc_info()[0])
            self.result = 0
            self.stop_time = time.time()
