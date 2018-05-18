from requests import get
from pandas import DataFrame
from utils import *

class DstTables(object):
    def __init__(self, lang='en'):
        self.lang = assign_lang(lang)

    def get_tables(self, subjects=None, active_tables=True):
        inactive = not active_tables
        if not isinstance(active_tables, bool):
            raise ValueError('`active_tables` can only take the values True or False')

        if isinstance(subjects, list) or isinstance(subjects, str) or subjects is None:
            if isinstance(subjects, list):
                subjects_url = "https://api.statbank.dk/v1/tables?lang={lang_}&subjects={subject_}&includeInactive={inactive_}&format=JSON".format(subject_=",".join(subjects), lang_=self.lang, inactive_=inactive)
            elif isinstance(subjects, str):
                subjects_url = "https://api.statbank.dk/v1/tables?lang={lang_}&subjects={subject_}&includeInactive={inactive_}&format=JSON".format(subject_=subjects, lang_=self.lang, inactive_=inactive)
            else:
                subjects_url = "https://api.statbank.dk/v1/tables?lang={lang_}&includeInactive={inactive_}&format=JSON".format(lang_=self.lang, inactive_=inactive)

            subjects_r = get(subjects_url)
            Error(subjects_r)

        else:
            raise ValueError('subjects must be a list or a string of subject ids')

        df = DataFrame(subjects_r.json())
        df['updated'] = pd.to_datetime(df['updated'])
        return df
