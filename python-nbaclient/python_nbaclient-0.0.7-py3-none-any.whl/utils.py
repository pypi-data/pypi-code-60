import requests
import pprint


class Query:
    def __init__(self):
        self.resp = None

    def get_stats(self, url, headers, api_param):
        self.resp = requests.get(url, headers=headers, params=api_param)
        return self.resp

    def convert_to_json(self):
        return self.resp.json()


class Output:
    def __init__(self, indent=2):
        self.pretty_print = pprint.PrettyPrinter(indent=indent)

    def pretty_json(self, resp_json):
        self.pretty_print.pprint(resp_json)
