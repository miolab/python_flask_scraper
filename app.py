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

    # URL
    # // Qiita
    url_qiita = "https://qiita.com/search?q=" + word_in_url + "&sort=rel"
    # // Stack Over Flow
    url_sof = "https://stackoverflow.com/search?q=" + word_in_url
    # // Developers.IO
    url_dev = "https://dev.classmethod.jp/?s=" + word_in_url

    """ Tag Information
    - Qiita
        <h1 class="searchResult_itemTitle">
            <a href="/garakutayama/items/0768bc6135ec0683df67">article_title</a>
        </h1>

    - Stack Over Flow
        <div class="result-link">
            <h3>
                <a href="/questions/53660779/including-node-package-into-python-aws-lambda?r=SearchResults" data-searchsession="/questions/53660779/including-node-package-into-python-aws-lambda?r=SearchResults&amp;s=15|109.3204" title="Including node package into Python AWS Lambda" class="question-hyperlink">
                Q: Including node package into Python AWS Lambda        </a>
            </h3>
        </div>

    - Developers.IO
        <p class="title">
            <a href="https://dev.classmethod.jp/etc/ec2-image-builder-codepipeline/">設定ファイルPushでゴールデンイメージを自動作成する構成を考えてみた</a>
        </p>
    """

    dict_qiita = {
        "url": url_qiita,
        "tag": "h1",
        "css_class": "searchResult_itemTitle"
    }
    dict_sof = {
        "url": url_sof,
        "tag": "div",
        "css_class": "result-link"
    }
    dict_dev = {
        "url": url_dev,
        "tag": "p",
        "css_class": "title"
    }

    # print(dict_dev["url"])




    # // ON GOING //

    # def fn_(url, tag, css_class):
        
    #     html_req = requests.get(url)
    #     html_contents = html_req.content

    #     # // Set Parser
    #     soup = bs(html_contents, 'html.parser')

        # css_titles_h1_class = "searchResult_itemTitle"
        # title_list = soup.find_all("h1", class_=css_titles_h1_class)




    # for i in range(title_list):
    #     time.sleep(0.1)
    #     print(title_list[i].text)




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
