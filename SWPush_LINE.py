#!/usr/bin/env python3
import requests
import RPi.GPIO as GPIO
import time
import sys
import cv2
import datetime
import os
import pandas as pd       #pandas icolで応答Flag動作用
import subprocess, shlex  #シェルスクリプト動作用import
#import subprocess #PythonからPythonを実行する

#HENSIN_kansi ="/home/pi/project3/CameraVoice/hensin/static"

FLAG=   '/home/pi/project3/CameraVoice/hensin/Flag'
# LED_GPIO 変数に 24をセット
SW_GPIO = 24

# GPIO.BCMを設定することで、GPIO番号で制御出来るようになります。
GPIO.setmode(GPIO.BCM)

# GPIO.INを設定することで、入力モードになります。
# pull_up_down=GPIO.PUD_DOWNにすることで、内部プルダウンになります。
GPIO.setup(SW_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

LastStatus = False
 # カレントディレクトリを、送信画像が配置されているパスに変更
#os.chdir(os.getcwd() + '/CameraVoice/jpgSAVE')
#LINE送信用関数
def LINE_message_send():
      
    dt_now = datetime.datetime.now()
    Now_time = dt_now.strftime('%Y年%m月%d日%H時%M分%S秒')
    #検出時間の取得
    print(Now_time)
    
    f = open('/home/pi/project3/CameraVoice/hensin/ngrokURL.txt','r')
    ngrokURL = f.read()
    #プロ演インターホン通知：LINE通知
    url = "https://notify-api.line.me/api/notify" 
    token = "hHajLVFv0jZxaXlyKgLeo5211Po8vEw27GAN1A1eZ8A"
    headers = {"Authorization" : "Bearer "+ token}
    
    message =  "\n",Now_time,"\nインターホンのボタンが押されました\n来客です。 \n応答URL↓\n",ngrokURL
    #files = {'imageFile': open(Now_time + '.jpg', "rb")}
    payload = {"message" :  message} 
    r = requests.post(url, headers = headers, params=payload)#files=files)
    f.close()
    


try:
    print("通知プログラム起動")
    while True:        
# ボタン押し / 離し 動作確認用コード
   
        # GPIO24の値を読み込み、その値を出力します。
        # ボタンを押すと"1"（High）、離すと"0"（Low）。
        SwitchStatus = GPIO.input(SW_GPIO)
        
        if LastStatus != SwitchStatus:            
            
            if SwitchStatus == 1:
                #フラグ用ディレクトリがあれば削除（無いとエラー(FileNotFoundError)が出るがスルーするように作成）
                try:
                    os.rmdir(FLAG)
                except FileNotFoundError as e:
                    pass
                
                print("FLAG用ディレクトリ ",os.path.exists(FLAG))
                
                print("LINE send")
                

                
       #カメラ画像を保存する
        
                """
                DIRname = '/home/pi/project3/CameraVoice/jpgSAVE'
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                cv2.imwrite(os.path.join(DIRname,(Now_time + '.jpg')), frame)
                cap.release()
                print("Camera send")
                """
            #LINEメッセージ送信 現時間&メッセージ
                LINE_message_send()
            #どちら様でしょうか？メッセージ
                args = shlex.split("/home/pi/project3/CameraVoice/OpenJTalk/OpenJTalk起動.sh どちら様でしょうか？")
                ret = subprocess.call(args)
            #返信中。少々お待ちくださいメッセージ
                time.sleep( 2 )
                if os.path.exists(FLAG) == False:                    
                    args = shlex.split("/home/pi/project3/CameraVoice/OpenJTalk/OpenJTalk起動.sh 応答を確認しています。少々お待ちください。")
                    ret = subprocess.call(args)
                
                time.sleep( 15 )
                if os.path.exists(FLAG) == False:
                    print("スマホ応答なし")
                    #返信がありませんでした。メッセージ
                    args = shlex.split("/home/pi/project3/CameraVoice/OpenJTalk/OpenJTalk起動.sh 応答がありませんでした。不在です。")
                    ret = subprocess.call(args)
                
                if os.path.exists(FLAG) == True:
                    print("スマホ応答あり！！")
                    
                print("FLAG用ディレクトリ ",os.path.exists(FLAG))            
                time.sleep(0.2)
                print("end")
        LastStatus = SwitchStatus
        

# Ctrl+Cキーを押すと処理を停止
except KeyboardInterrupt:
    # ピンの設定を初期化
    # この処理をしないと、次回 プログラムを実行した時に「ピンが使用中」のエラーになります。
    GPIO.cleanup()
    sys.exit()
    observer.stop()
    observer.join()
