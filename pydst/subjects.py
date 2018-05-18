from pydst.utils import *
from requests import get
import sys

class DstSubjects(object):
    def __init__(self, lang='en'):
        self.lang = assign_lang(lang)

    def get_subjects(self, subjects=None):
        base_url = "https://api.statbank.dk/v1/subjects?lang={}&format=JSON".format(self.lang)
        base_r = get(base_url)
        base_r_json = base_r.json()
        subjects_r_json = []

        Error(base_r)

        if isinstance(subjects, list) or isinstance(subjects, str):
            if isinstance(subjects, list):
                subjects_url = "https://api.statbank.dk/v1/subjects/{}?lang={}&format=JSON".format(",".join(subjects), self.lang)
            else:
                subjects_url = "https://api.statbank.dk/v1/subjects/{}?lang={}&format=JSON".format(subjects, self.lang)
            subjects_r = get(subjects_url)
            subjects_r_json = subjects_r.json()
            Error(subjects_r)

        elif not subjects is None:
            raise ValueError('subjects must be a list or a string of subject ids')

        return desc_to_df([*base_r_json, *subjects_r_json])
