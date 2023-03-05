#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request,redirect,url_for
import subprocess
import talk
import os



app = Flask(__name__, static_folder='./static')
FLAG_mkdir = '/home/pi/project3/CameraVoice/hensin/Flag'


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)



# ブラウザに画面を表示
@app.route('/', methods=['GET'])
def get():
    return render_template('index.html')

# ブラウザからのデータ取得
@app.route('/', methods=['POST'])
def post():
    
    speaker_action = request.form.get('speaker_action')
    if speaker_action == '送信':
        #FLAG用のディレクトリを無ければ作成するコード（exits_okを指定するとエラーで終わらないように出来た）
        os.makedirs(FLAG_mkdir, exist_ok=True)
        
        speaker_text = request.form.get('speaker_text')
        talk.talk(speaker_text)
          
        print (speaker_text)
        return redirect(url_for('get'))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)