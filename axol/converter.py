import json

import urllib3

http = urllib3.PoolManager()

query = "https://cash.rbc.ru/cash/json/converter_currency_rate/?"
delimiter = "&"


def convert(from_value, to_value, sum_value):
    from_string = "currency_from=" + from_value
    to_string = "currency_to=" + to_value
    sum_string = "sum=" + str(sum_value)
    date_string = "date=&"  # only today, hardcoded
    rate_string = "source=cash"  # only obmennik, hardcoded

    full_query = query \
                 + from_string + delimiter \
                 + to_string + delimiter \
                 + sum_string + delimiter \
                 + date_string + delimiter \
                 + rate_string

    json_result = http.request('GET', full_query)
    result = json.loads(json_result.data.decode("utf-8"))

    return result["data"]["sum_result"]
