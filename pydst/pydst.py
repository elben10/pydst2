# -*- coding: utf-8 -*-

"""This module powers the DstSubjects class that is the workhorse to obtain subjects and subjects from
Statistics Denmark."""

from pydst.utils import assign_lang, desc_to_df, Error
from requests import get
from pandas import DataFrame, to_datetime, read_csv
from collections import OrderedDict
from io import BytesIO

class DST(object):
    """Returns a phasor plot of the given eigenvalues and eigenvectors.

    Attributes
    ----------
    lang : The eigenvalues.

    Returns
    -------
    figs : list
        A list of matplotlib figures.

    Notes
    -----
    Plots are not produced for zero eigenvalues.

    TODO
    -----
    Plots are not produced for zero eigenvalues.

    .. todo:: blabla

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

    def get_tables(self, subjects=None, active_tables=True):
        inactive = not active_tables
        if not isinstance(active_tables, bool):
            raise ValueError('`active_tables` can only take the values True or False')

        if isinstance(subjects, (list, str, type(None))):
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
        df['updated'] = to_datetime(df['updated'])
        return df

    def get_meta(self, tableID=None):
        base_url = 'https://api.statbank.dk/v1/tableinfo/{}?lang={}&format=JSON'.format(tableID, self.lang)
        r = get(base_url)
        #values = [{j['id']: j['text'] for j in i['values']} for i in r.json()['variables']]
        values = [OrderedDict([tuple(j[a] for a in ['id','text']) for j in i['values']]) for i in r.json()['variables']]
        res = DataFrame(r.json()['variables'])
        res['values'] = values
        return res

    def get_data(self, tableID=None, params=None):
        metadata = self.get_meta(tableID=tableID)
        if isinstance(tableID, type(None)):
            raise ValueError('tableID must be provided')
        elif not isinstance(tableID, str):
            raise ValueError('tableID must be a string')

        if not isinstance(params, (dict, type(None))):
            raise ValueError('params must be None or dict')
        elif isinstance(params, dict):
            if not all([x.upper() in [x.upper() for x in metadata['id'].tolist()] for x in params.keys()]):
                bad_vars = [x for x in params.keys() if (x.upper() not in metadata['id'].tolist())]
                raise ValueError('The following variables does not exists within the specified table: {}'.format(','.join(bad_vars)))
            if not all(isinstance(x, (str, list)) for x in params.values()):
                raise ValueError('variable values must be either a string or a list')
            if not all(isinstance(x, str) for j in params.values() for x in j if isinstance(j, list)):
                raise ValueError('variable values within a list must only be strings')
            params = {x:(y if isinstance(y, str) else ','.join(y)) for x,y in params.items()}


        if isinstance(params, dict):
            base_param = {x:list(y)[0] for x,y in zip(metadata['id'].tolist(), metadata['values']) if not x in params.keys()}
            params = {**base_param, **{x.upper():y for x,y in params.items()}}
        else:
            params = {x:list(y)[0] for x,y in zip(metadata['id'].tolist(), metadata['values'])}

        params_string = '&'.join([x + '=' + y for x, y in params.items()])

        base_url = 'https://api.statbank.dk/v1/data/{}/BULK?lang={}&valuePresentation=Default&delimiter=Semicolon&{}'.format(tableID, self.lang, params_string)
        r = get(base_url)

        return read_csv(BytesIO(r.content), delimiter=';')
