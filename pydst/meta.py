from pydst.utils import assign_lang
from requests import get
from pandas import DataFrame
from collections import OrderedDict

class DstMeta(object):
    def __init__(self, lang='en'):
        self.lang = assign_lang(lang)

    def get_meta(self, tableID=None):
        base_url = 'https://api.statbank.dk/v1/tableinfo/{}?lang={}&format=JSON'.format(tableID, self.lang)
        r = get(base_url)
        #values = [{j['id']: j['text'] for j in i['values']} for i in r.json()['variables']]
        values = [OrderedDict([tuple(j[a] for a in ['id','text']) for j in i['values']]) for i in r.json()['variables']]
        res = DataFrame(r.json()['variables'])
        res['values'] = values
        return res
