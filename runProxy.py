from contextlib import closing
import requests
from flask import Flask, request, Response

app = Flask(__name__)


@app.before_request
def before_request():
    print(" request.url:", request.url, '-->File "runProxy.py", line 12')
    a = ("http://stat.ajmide.com/stat" == request.url)
    print(" request.method:", request.method, '-->File "runProxy.py", line 12')
    print(" a:", a, '-->File "runProxy.py", line 14')
    if (a):
        print(" request.get_data():", request.get_data(), '-->File "runProxy.py", line 16')
        
        return ""

    with closing(

            requests.request(
                method=request.method,
                url=request.url,
                headers=request.headers,
                data=request.get_data(),
                cookies=request.cookies,
                allow_redirects=False)
    ) as resp:
        resp_headers = []
        for name, value in resp.headers.items():

            if name.lower() == 'connection':
                resp_headers.append((name, 'close'))

            if name.lower() in ('content-length', 'connection', 'content-encoding', 'transfer-encoding'):
                continue
            resp_headers.append((name, value))

        # excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        # headers = [(name, value) for (name, value) in resp.raw.headers.items()
        #            if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, resp_headers)

        return response


app.run(host="0.0.0.0", port=5001, debug=True,threaded=True)
