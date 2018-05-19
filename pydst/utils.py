from pandas import DataFrame

def assign_lang(lang):
    """Returns lang if the language is valid
    Args:
        lang (str):
            lang can take the values `da` or `en` for Danish, English respectively
    """
    if not lang in ['en', 'da']:
        raise ValueError('language can only take the values `en` or `da`. See documentation')
    return lang

def desc_to_df(list_):
    def json_to_df_dict(list_):
        res = []
        for i in list_:
            if not i['subjects']:
                res.append({'id': i['id'], 'desc': i['description'], 'active': i['active'], 'hasSubjects': i['hasSubjects']})
            else:
                res.extend(json_to_df_dict(i['subjects']))

        return res
    return DataFrame(json_to_df_dict(list_))


class Error(object):
    def __init__(self, request):
        if not request.ok:
            raise ValueError(request.json()['message'])
