"""This module powers the DstSubjects class that is the workhorse to obtain subjects and subjects from
Statistics Denmark."""

from pydst.utils import assign_lang, desc_to_df, Error
from requests import get

class DstSubjects(object):
    """subject class for obtaining classes and subclasses of Statistics Denmarks

    Attributes:
        lang (str):
            the language of the subjects. Can be either `da` for danish or `en` for english
    """
    def __init__(self, lang='en'):
        """Initiation of DstSubjects

        Args:
            lang (str):
                the language of the subjects. Can be either `da` for danish or `en` for english
        """
        self.lang = assign_lang(lang)

    def get_subjects(self, subjects=None):
        """DataFrame containing base subjects and specified subjectsself.

        Args:
            subjects (str, list):
                subjects parameter is used to obtain subsubjects from Statistics Denmarkself.
                If subjects=None then the top level subjects will be returned.
        """
        base_url = "https://api.statbank.dk/v1/subjects?lang={}&format=JSON".format(self.lang)
        base_r = get(base_url)
        base_r_json = base_r.json()
        subjects_r_json = []

        Error(base_r)

        if isinstance(subjects, (list, str)):
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
