""" Doc

Status : On Going (alpha)
Version: 0.0

"""
# import sys
import os
import re
import time
import concurrent.futures as cf
# from threading import Timer

from flask import Flask, render_template, request, session
import requests
from bs4 import BeautifulSoup as bs
# from wtforms import Form, TextAreaField, validators

import pprint
import pytest


url_origin_qiita = "https://qiita.com/"
url_origin_sof = "https://stackoverflow.com/"
url_origin_dev = "https://dev.classmethod.jp/"


app = Flask(__name__)
app.secret_key = b"lkjcgfhjklkjhgjklkjhgjkljhuilkjfd"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST','GET'])
def result():
    time.sleep(0.1)
    input_text = request.form["input_text"]
    input_text.strip()

    if re.search("\s", input_text):
        word_in_url = re.sub(r"\s+", "+", input_text)
    else:
        word_in_url = input_text

    class Url:
        def __init__(self, url, tag, css_class):
            self.url = url
            self.tag = tag
            self.css_class = css_class

        def fn_prepare_title_list(self):
            html_req = requests.get(self.url)
            html_contents = html_req.content
            soup = bs(html_contents, 'html.parser')
            self.title_list = soup.find_all(self.tag, class_=self.css_class)
            return self.title_list


    # // Qiita
    url_qiita = Url(
        url = url_origin_qiita + "search?q=" + word_in_url + "&sort=rel",
        tag = "h1",
        css_class = "searchResult_itemTitle",
    )
    # // Stack Over Flow
    url_sof = Url(
        url = url_origin_sof + "search?q=" + word_in_url,
        tag = "a",
        css_class = "question-hyperlink"
    )
    # // Developers.IO
    url_dev = Url(
        url = url_origin_dev + "?s=" + word_in_url,
        tag = "p",
        css_class = "title"
    )


    worker_cores = os.cpu_count()

    with cf.ThreadPoolExecutor(max_workers=worker_cores) as executor:
        """ Parallel task execution
        """
        executor.submit(url_qiita.fn_prepare_title_list())
        executor.submit(url_sof.fn_prepare_title_list())
        executor.submit(url_dev.fn_prepare_title_list())

    # // Sequential processing instead of Parallel task processing //
    # url_qiita.fn_prepare_title_list()
    # url_sof.fn_prepare_title_list()
    # url_dev.fn_prepare_title_list()


    # pprint.pprint(url_qiita.title_list[0].text)
    # pprint.pprint(url_sof.title_list[0].text)
    # pprint.pprint(url_dev.title_list[0].text)


    def fn_replace_tag(new_array, bs4_array, tag_hd_pre, tag_hd_post, tag_tl_pre, tag_tl_post, a_prefix):
        for i in range(len(bs4_array)):
            _ = re.sub(tag_hd_pre, tag_hd_post, str(bs4_array[i]))
            _ = re.sub(tag_tl_pre, tag_tl_post, _)

            if a_prefix == "":
                pass
            else:
                _ = re.sub('a href="', 'a href="'+a_prefix, _)

            new_array.append(_)
        return new_array


    array_qiita = []
    array_sof = []
    array_dev = []

    with cf.ThreadPoolExecutor(max_workers=worker_cores) as executor:
        executor.submit(fn_replace_tag(array_qiita, url_qiita.title_list, r"<h\d", "<p", r"</h\d", "</p", url_origin_qiita))
        executor.submit(fn_replace_tag(array_sof, url_sof.title_list, "<a", "<p><a", r"</a>", "</a></p>", url_origin_sof))
        executor.submit(fn_replace_tag(array_dev, url_dev.title_list, "\n", "", "", "", ""))


    return render_template('result.html',
        array_qiita=array_qiita,
        array_sof=array_sof,
        array_dev=array_dev,
    )


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




""" DEv memo

# todo

- 検索結果数をフロント側で可変する（resultのヘッド部分で）


---

# Tag Information

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
