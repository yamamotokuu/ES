#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import sys
import record
import requests
import datetime

# LED_GPIO 変数に 25をセット
SW_GPIO = 25

# GPIO.BCMを設定することで、GPIO番号で制御出来るようになります。
GPIO.setmode(GPIO.BCM)

# GPIO.INを設定することで、入力モードになります。
# pull_up_down=GPIO.PUD_DOWNにすることで、内部プルダウンになります。
GPIO.setup(SW_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#応答した時の録音ファイルが更新されればLINEに送る関数
def LINE_message_HENSIN_kansi(Now_time):
    f = open('/home/pi/project3/CameraVoice/hensin/ngrokURL.txt','r')
    ngrokURL = f.read()
    #プロ演インターホン通知：LINE通知
    url = "https://notify-api.line.me/api/notify" 
    token = "hHajLVFv0jZxaXlyKgLeo5211Po8vEw27GAN1A1eZ8A"
    headers = {"Authorization" : "Bearer "+ token}
    
    message =  "\n",Now_time,"\n訪問者からから応答がありました。\nwebブラウザの更新をして下さい。\n応答URL↓\n",ngrokURL
    #files = {'imageFile': open(Now_time + '.jpg', "rb")}
    payload = {"message" :  message} 
    r = requests.post(url, headers = headers, params=payload)
    f.close()
    
if __name__ == '__main__':
    # Audioインスタンスの作成
    audio = record.Audio()
    while True:
        try:
            # ボタン押し
            if GPIO.input(SW_GPIO) == 1:
                # マイクに喋った内容を音声ファイルに保存
                print('start record')
                audio.start_record()
                while GPIO.input(SW_GPIO) == 1:
                    time.sleep(1)  # 1秒間待つ
                audio.stop_record()
                print('stop record')
                
                ##----------------------
                #検出時間の取得
                dt_now = datetime.datetime.now()
                Now_time = dt_now.strftime('%Y年%m月%d日%H時%M分%S秒')
                print(Now_time)
                #LINEへブラウザを更新してくれという通知を送る
                LINE_message_HENSIN_kansi(Now_time)
        
                time.sleep(1)   # 1秒間待つ

        # Ctrl+Cキーを押すと処理を停止
        except KeyboardInterrupt:
            audio.stop_record()
            # ピンの設定を初期化
            # この処理をしないと、次回 プログラムを実行した時に「ピンが使用中」のエラーになります。
            GPIO.cleanup()
            sys.exit()
