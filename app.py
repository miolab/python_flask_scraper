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

    # // "関連順"
    url = "https://qiita.com/search?q=" + word_in_url + "&sort=rel"
    # // "新着順"
    # url = "https://qiita.com/search?q=" + word_in_url + "&sort=created"
    print(url)

    html_req = requests.get(url)
    html_contents = html_req.content


    # // Set Parser
    soup = bs(html_contents, 'html.parser')

    # // Tag Information
    # <h1 class="searchResult_itemTitle"><a href="/garakutayama/items/0768bc6135ec0683df67">【<em>AWS</em>勉強】<em>AWS</em> SDK　概要</a></h1>

    css_titles_h1_class = "searchResult_itemTitle"
    title_list = soup.find_all("h1", class_=css_titles_h1_class)

    print(title_list[0].text)


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
