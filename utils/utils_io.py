# standard
# import random
import pathlib
import sys
# external
# import requests
# import boto3


def get_file(filename, folders=None):
    # folders = list of subdirectory names
    #           in tree from cwd
    # print(f'''Retrieving {filename} in {folder}''')
    if folders:
        if not isinstance(folders, list):
            print("Folders paramaeter MUST be a list!")
            sys.exit()
        p = pathlib.Path.cwd().joinpath(*folders)
    else:
        p = pathlib.Path.cwd()
    path = p.joinpath(filename)
    return path.read_text()


def put_file(data, filename, folders=None):
    # WARNING: THIS OVERWRITES DATA
    # print(f'''Writing {filename} in {folder}''')
    if folders:
        if not isinstance(folders, list):
            print("Folders paramaeter MUST be a list!")
            sys.exit()
        p = pathlib.Path.cwd().joinpath(*folders)
    else:
        p = pathlib.Path.cwd()
    path = p.joinpath(filename)
    path.write_text(data)
    return


""" def put_S3(file_name):
    # should have variable for cach controle
    # should have variable for file path
    print("++++++++++++\nNow in Put S3 module ...")
    s3 = boto3.resource('s3')
    js_file_name = f"{file_name}.js"
    data = open(f'./build/{js_file_name}', 'rb')
    s3.Bucket('picabot').put_object(Key=f'pagejs/{js_file_name}', Body=data, CacheControl="max-age=1800")
    return


def get_data(s_url, b_json=True, l_filter=None):
    print("+++++++++++++\nNow in fetch_data module ...")
    # string s_url
    # boolean b_json whether to return json or text
    # list of strings that are really keys to drill down the dict
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/70.0.3538.75 Mobile/15E148 Safari/605.1',
        'Mozilla/5.0 (Linux; Android 7.0; SM-G570M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.80 Mobile Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
    ]
    headers = {'user-agent': random.choice(user_agents)}
    # print(f"Fetch headers: {headers}")
    r = requests.get(s_url, headers=headers)
    if b_json:
        d = r.json()
        if l_filter:
            temp = d
            for item in l_filter:
                # print(item)
                temp = temp[item]
            return temp
        else:
            return d
    else:
        return r.text


def minify_css(file_name):
    print("++++++++++\nNow in fetch_css module ...")
    # get CSS from file, minify said css
    # file path needs to be in form './static/abc.css/'
    css_file = {'input': open(f'''./static/{file_name}''', 'rb').read()}
    response = requests.post('https://cssminifier.com/raw', data=css_file)
    css = response.text
    return css """
