import sys
import os
import re
import time
# from threading import Timer

from flask import Flask, render_template, request, session
import requests
from bs4 import BeautifulSoup as bs
# from wtforms import Form, TextAreaField, validators


app = Flask(__name__)
app.secret_key = b"lkjcgfhjklkjhgjklkjhgjkljhuilkjfd"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST','GET'])
def result():
    input_text = request.form["input_text"]
    input_text.strip()
    if re.search("\s", input_text):
        word_in_url = re.sub(r"\s+", "+", input_text)
    else:
        word_in_url = input_text
    url = "https://qiita.com/search?q=" + word_in_url + "&sort=created"

    html_req = requests.get(url)
    html_contents = html_req.content
    soup = bs(html_contents, 'html.parser')


    # title_list = soup.find_all(class_='tst-ArticleBody_title')



    # return render_template('index.html', title_list)
    return render_template('result.html')


@app.route('/result', methods=['POST'])
def redirect():
    session.clear()
    return render_template('index.html')


# def fn_webdriver():
#     webdriver.open("http://localhost:5000/")


if __name__ == '__main__':
    # Timer(2, fn_webdriver)
    app.debug = True
    app.run(host='localhost', port=5000)
