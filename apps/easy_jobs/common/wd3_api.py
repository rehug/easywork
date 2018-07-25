# -*- coding: utf-8 -*-

import json
import requests


class ReqApi(object):
    """
    Call API
    """

    def __init__(self, _url, _method, _headers, _data=None):
        self._url = _url
        self._method = _method
        self._headers = _headers
        self._data = _data

    def get_req(self):
        get_response_info = requests.get(self._url, self._headers)
        return get_response_info

    def post_req(self):
        post_response_info = requests.post(
            self._url, headers=self._headers, data=self._data
        )
        return post_response_info

    def exc_req(self):
        req_info = ''
        if self._method.upper() == 'GET':  # 兼容大小写
            req_info = self.get_req()
        elif self._method.upper() == 'POST':  # 兼容大小写
            req_info = self.post_req()
        else:
            pass
        return req_info


# def get_csv_data(_filename):
#     """
#     Read csv file and return a list with element of dict.
#     :param _filename: source csv filename
#     :return: list(dict)
#     """
#     csv_data = pd.read_csv(_filename, header=0)
#     csv_data = csv_data.fillna('-')  # 填补缺失值

#     _headers = csv_data.columns
#     headers = list()
#     for head in _headers:
#         headers.append(head)

#     contents = csv_data.values
#     _data_list = list()
#     for content in contents:
#         temp_data = dict(zip(headers, content))
#         _data_list.append(temp_data)

#     return _data_list


def transfer_data(origin_data, col_map):
    _result = list()
    for tmp in origin_data:
        result_dict = dict()
        for group in col_map:
            target_col = group["target"]
            origin_col = group["origin"]
            default_value = group["default"]
            if default_value is not None:
                value = tmp.get(origin_col, default_value)
            else:
                value = tmp.get(origin_col)
            result_dict[target_col] = value
        _result.append(result_dict)
    return _result


def get_token():
    """
    获取token
    :return: string
    """
    token_api = "https://www.example.com/api/v2/login"
    params_1 = {
        'username': 'user',
        'password': 'password',
        'Content-Type': 'application/json'
    }
    req_1 = requests.post(token_api, params_1, timeout=100).json()  # dict
    _token = req_1.get('data', '-')  # token
    return _token


def request(data, profile_id, command, table):
    if command == "update" and table == "order":
        url_pattern = "https://www.example.com/{profile_id}/datadock/upload/json"
    elif command == "update" and table == "product":
        url_pattern = "https://www.example.com/{profile_id}/productinfo"
    else:
        raise Exception("{command} {table} is not supported!".format(
            command=command, table=table))
    json_data = json.dumps(data)
    url = url_pattern.format(
        profile_id=profile_id)
    token = get_token()
    header = {
        'Content-Type': 'application/json',
        'Token': token
    }
    api_info = ReqApi(url, 'post', header, json_data).exc_req()
    return api_info


def main(origin_data, col_map, profile_id, command, table):
    data = transfer_data(origin_data, col_map)
    api_info = request(data, profile_id, command, table)
    return api_info
