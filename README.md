# Python (Flask) & Vue.js 開発用テンプレート

### 💻 下記実装コードのチートシート。（兼、後述アプリ開発）
- Flask & Vue.js によるMVC開発
- スクレイピング
- ほかPython, Vue.jsの機能いろいろ

### 💻 開発環境
- pipenv
- Python 3.8
- Flask 1.1.1
- Vue.js 2.6.11
- VSCode


# アプリの説明

## __🔎 Tech Article Finder__

しらべたい技術トピックについて、複数のナレッジコミュニティサイトで横断的に記事検索し  
キーワード検索結果を集約し一覧化するWebアプリです。

![tool_image](https://user-images.githubusercontent.com/33124627/74113258-665aa800-4be6-11ea-9250-e2e3905ec655.png)


### 🔎 使い方

1. ブラウザでアクセス  
  http://localhost:5000
1. 検索窓に、しらべたいキーワードを1個もしくは2個以上タイプし、  
  検索ボタンをクリック。
  - 現バージョンでは、下記サイトの検索結果記事を一覧表示します
    - [Qiita](https://qiita.com/)
    - [Stack Over Flow](https://stackoverflow.com/)
    - [Developes.IO](https://dev.classmethod.jp/)

### 🔎 アプリ制作の背景

下記問題の解決をはかるため。

- それぞれ技術系サイトでは、各々のサイト内での検索結果記事しか確認できない。  
  →　1回の検索操作で、他の技術系サイトの検索結果もまとめて表示したい。

- GoogleやYahooなどの一般検索サイトでは、技術系サイト以外の検索結果がノイズとして表示されてしまう。  
  →　検索対象をあらかじめ技術系サイトにしぼることができれば、  
  必要ない検索結果をあらかた除外した状態から、自分の見たいトピックを吟味できる。

- 技術系サイトであっても、
  プログラミングスクールの申込みに誘導される・広告が多い・・・  
  などの、ストレスを感じさせる記事が検索結果に返ることが往々にしてある。  
  →　自分の志向に合わないサイトは前もって除外しておきたい。


__※ 冒頭説明の通り、本アプリは「Flask開発チートシート」の役割色がつよく、ソースコード中  
実装手順の手引き的に冗長なコードを書いていたり、コメントを残している箇所があったりします。__


### 🔎 今後の機能追加予定

  CRUDによる下記カスタマイズ機能
  1. 希望サイトを選択登録
  1. 表示記事数増減
  1. お気に入り記事ストック  
  etc.

