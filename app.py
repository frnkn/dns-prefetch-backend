from chalice import Chalice
from bs4 import BeautifulSoup

import subprocess

app = Chalice(app_name='dns-prefetch-backend')

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/dns-prefetch/{url}', cors=True)
def dns_prefetch(url):
    #r = requests.get(url)
    # subprocess.check_call(['curl', url])
    html_doc = subprocess.check_output(['curl', url])
    urls = _find_dns_prefetch_links(html_doc)

    domains = ["http://www.soliver.de", "http://www.example.org"]
    return {'dns-prefetch-domains': domains, 'content': urls}


def _find_dns_prefetch_links(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    css_urls = [link["href"] for link in soup.findAll("link") if "stylesheet" in link.get("rel", [])]
    js_urls = [i.get('src') for i in soup.findAll('script') if i.get('src')]
    img_urls =  []

    for image in soup.findAll('img'):
        img_urls.append(image.get('src'))

    all_urls = {"css_urls": css_urls, "js_urls": js_urls, "img_urls": img_urls}
    return all_urls




# The view function above will return {"hello": "world"}
# whenver you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.json_body
#     # Suppose we had some 'db' object that we used to
#     # read/write from our database.
#     # user_id = db.create_user(user_as_json)
#     return {'user_id': user_id}
#
# See the README documentation for more examples.
#
