from os import name
from flask import Flask, render_template,request

import sqlite3, random

# （1）必要なパッケージをインポート
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError
 
# （2）LINE APIへ接続するための定数を定義。
LINE_ACCESS_TOKEN= "OhgpU9irRwJ9DvlG6MN0BY1GTo1CF5BpT2BdIGo1AESItseNRmiiXtzMfPivgjVxQlnKGzS1t02rzdt1cy3hyFMU3fl2ToywdOS4iQZz8yke3NlROCLqmYs1KUsOVaMd4K9I7VYD33C+QuHsWD8uSQdB04t89/1O/w1cDnyilFU=" # ラインアクセストークン
LINE_USER_ID= "U1a74ce0d3ceb2f8d80d6f6ff2f8bf257" # ライン
 
# LINE APIを定義。引数にアクセストークンを与える。
line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)


app = Flask(__name__)
app.secret_key="sunabacokoza"


# トップページを表示するpython(flask)
@app.route("/", methods=["GET"])
def top():
    return render_template("top.html")

@app.route("/index",methods=["GET"])
def index():
    return render_template("index.html")

# カテゴリーを選択した時に動くpython(flask)
@app.route("/category", methods=["POST"])
def category():
    # カテゴリーを選択するとHTMLで埋め込まれているvalueをとってくる
    number = request.form.get("category")
    # print(type(number))
    # とってきたvalueの形を調べるとstr(文字列)型だったから、↓でint(数値)型に変換する
    category_id = int(number)
    # print(type(category_id))
    conn = sqlite3.connect("sotugyou.db")
    c = conn.cursor()
    c.execute("SELECT * FROM main WHERE category_id=?",(category_id,) )
    list = c.fetchall()
    list = random.choice(list)
    # print(list)
    list = dict(id=list[0],name=list[1],word=list[2],task=list[3],category_id=list[4])
    print(list)
    
    c.close()
    return render_template("result.html", html_list=list )

@app.route("/result",methods=["GET"])
def result():
    return render_template("result.html",html_list=list)

@app.route("/line",methods=["post"])
def line_message():

    if request.method == 'POST':
        data = request.json
        print(data)
        task = data["task"]
        
    text_message ="あなたの今日のタスクは" + "\n" + "\n" + "『" + task + "』" + "\n" + "\n" + "です。"
    try:
        # ラインユーザIDは配列で指定する。
        line_bot_api.broadcast(
         TextSendMessage(text=text_message)
    )
    except LineBotApiError as e:
        # エラーが起こり送信できなかった場合
        print(e)

    return render_template("result.html", html_list=list)

@app.errorhandler(404)
def notfound(code):
    return "404エラーだよ！ページ見つからないよ！"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')