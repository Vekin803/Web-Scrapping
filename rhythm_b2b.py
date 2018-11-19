import psycopg2
from requests_html import HTMLSession
import requests_html
import os
import urllib




session = HTMLSession()
url = 'http://b2b.generaldepilas.com/login.aspx'
url2 = 'http://b2b.generaldepilas.com/mainpanel.aspx'
data = {
    'txNombre': 'invitado',
    'txPassword': 'invitado'
}





r = session.get(url2)
cookies = r.html

# for cookie in cookies:
#     print(cookie['name'])
#     print(cookie['value'])

print(cookies)

# def rhythm(item):
#     # Entrando en la plataforma B2B
#     session = HTMLSession()