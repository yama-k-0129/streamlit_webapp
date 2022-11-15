from http import client
import numpy as np
import calendar
from operator import index
import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime, timezone, timedelta
import time
from streamlit_option_menu import option_menu #pip install streamlit-option-menu
import database as db #local import 
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import schedule
from time import sleep
# from dotenv import load_dotenv#pip install python-dotenv

#Load the environment variables
account=st.secrets["account"]
pas=st.secrets["pass"]





st.title('勤怠管理')
selected = option_menu(
    menu_title=None,
    options = ['Entry', 'Private Report'],
    orientation = "horizontal",
)

 #--------Database interface---------
def get_all_profile():
        items = db.fetch_all_profile()
        names = [item["name"] for item in items]
        names_list = list(set(names))
        return names_list

def get_all_daytime():
    items = db.fetch_all_profile()
    daytimes = [item["key"] for item in items]
    return daytimes


if selected == "Entry":
    st.text('名前、仕事内容、時間を入力してください。')
    
    name_category = st.radio(
            '名前',
            ('泉野珠穂', '早崎水彩','藤原未奈','清水麻衣','安田希亜良','山村孝輝','鈴木美結','馬場大輝','宮原舞','坂本愛実'),
            key = "name"
        )
    if name_category == '泉野珠穂':
        adress = st.secrets["tama_adress"]
        number = 2252003
    elif name_category == '早崎水彩':
        adress = st.secrets["zaki_adress"]
        number = 2252020
    elif name_category == '藤原未奈':
        adress = st.secrets["wara_adress"]
        number = 2252022
    elif name_category == '清水麻衣':
        adress = st.secrets["maimai_adress"]
        number = 1912012
    elif name_category == '安田希亜良':
        adress = st.secrets["ara_adress"]
        number = 1912039
    elif name_category == '山村孝輝':
        adress = st.secrets["yama_adress"]
        number = 1912040
    elif name_category == '鈴木美結':
        adress = st.secrets["miyu_adress"]
        number = 2012015
    elif name_category == '馬場大輝':
        adress = st.secrets["baba_adress"]
        number = 2012027
    elif name_category == '宮原舞':
        adress = st.secrets["miyamai_adress"]
        number = 2012035
    elif name_category == '坂本愛実':
        adress = st.secrets["saka_adress"]
        number = 2212016
    else:
        print('名前を入力してください')

    
    work_category = st.radio(
            '業務内容',
            ('解析・資料作成補助','洪水解析モデル構築・データ作成','流域生物調査','地域測量','GISデータ作成','球磨川流域治水研究補助','その他')
        )
    if work_category == 'その他':
            work_category = st.text_input(
                '業務内容'
            )
    #日付選択
    date = st.date_input(
        '日付', datetime.now(timezone(timedelta(hours=9))))
    #時間選択
    time = st.time_input(
        '時間',datetime.now(timezone(timedelta(hours=9)))
    )

    with st.form(key='profile_form'):
        place = st.text_input('場所')    
        detail = st.text_input('詳細内容')
        #勤務
        switch = st.radio(
            "出退勤",
            ('出勤','退勤')
        )
        #ボタン
        submit_btn = st.form_submit_button('送信')
        if submit_btn:
            dt = datetime.combine(date,time)#日本時間のdatetimeオブジェクトが生成
            dt_utc = dt - timedelta(hours=9)#時差が反映され-9時間され，tzinfoが付加されたdatetimeオブジェクトが生成
            time_utc = dt_utc.time() 
            time_utc = str(time_utc)
            daytime = str(date) + "_" + str(time) + "_" + str(name_category)
            name = str(name_category)
            work = str(work_category)
            date = str(date)
            time = str(time) 
            switch = str(switch)
            db.insert_profile(daytime, name, date, work, time, switch)
            # Outlook設定
            my_account = account
            my_password = pas
            my_adress = adress

            def send_outlook_mail(msg):
                """
                引数msgをOutlookで送信
                """
                server = smtplib.SMTP('mail.so-net.ne.jp', 587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                # ログインしてメール送信
                server.login(my_account, my_password)
                server.send_message(msg)

            def make_mime(mail_to, subject, body):
                """
                引数をMIME形式に変換
                """
                msg = MIMEText(body, 'plain') #メッセージ本文
                msg['Subject'] = subject #件名
                msg['To'] = mail_to #宛先
                msg['From'] =  my_adress#送信元
                return msg
            
            if name_category == '泉野珠穂':
                def send_tama_message():
                        """
                        メイン処理
                        """
                        # MIME形式に変換
                        msg = make_mime(
                            mail_to='on12kyamamura@ec.usp.ac.jp', #送信したい宛先を指定
                            subject=f'出退勤記録簿報告について　瀧研究室 {number}{name_category}',
                            body=f'お世話になっております。瀧研究室{number}{name_category}と申します。\n{time}で{switch}致します。\n目的：{work_category}\n内容：{detail}\nよろしくお願いいたします。'
                            )
                        # gmailに送信
                        send_outlook_mail(msg)
                        return schedule.CancelJob()
                    schedule.every().day.at(time_utc).do(send_tama_message)
                    st.text(f'{name_category}さん！{time}に{switch}しました。')  
                    while True:
                        schedule.run_pending()
                        sleep(31)
            elif name_category == '早崎水彩':
                def send_zaki_message():
                    """
                    メイン処理
                    """
                    # MIME形式に変換
                    msg = make_mime(
                        mail_to='on12kyamamura@ec.usp.ac.jp', #送信したい宛先を指定
                        subject=f'出退勤記録簿報告について　瀧研究室 {number}{name_category}',
                        body=f'お世話になっております。瀧研究室{number}{name_category}と申します。\n{time}で{switch}致します。\n目的：{work_category}\n内容：{detail}\nよろしくお願いいたします。'
                        )
                    # gmailに送信
                    send_outlook_mail(msg)
                    return schedule.CancelJob()
                schedule.every().day.at(time_utc).do(send_zaki_message)
                st.text(f'{name_category}さん！{time}に{switch}しました。')  
                while True:
                    schedule.run_pending()
                    sleep(31)
            elif name_category == '藤原未奈':
                def send_wara_message():
                    """
                    メイン処理
                    """
                    # MIME形式に変換
                    msg = make_mime(
                        mail_to='on12kyamamura@ec.usp.ac.jp', #送信したい宛先を指定
                        subject=f'出退勤記録簿報告について　瀧研究室 {number}{name_category}',
                        body=f'お世話になっております。瀧研究室{number}{name_category}と申します。\n{time}で{switch}致します。\n目的：{work_category}\n内容：{detail}\nよろしくお願いいたします。'
                        )
                    # gmailに送信
                    send_outlook_mail(msg)
                    return schedule.CancelJob()       
                schedule.every().day.at(time_utc).do(send_wara_message)
                st.text(f'{name_category}さん！{time}に{switch}しました。')  
                while True:
                    schedule.run_pending()
                    sleep(31)
            elif name_category == '清水麻衣':
                def send_mai_message():
                    """
                    メイン処理
                    """
                    # MIME形式に変換
                    msg = make_mime(
                        mail_to='on12kyamamura@ec.usp.ac.jp', #送信したい宛先を指定
                        subject=f'出退勤記録簿報告について　瀧研究室 {number}{name_category}',
                        body=f'お世話になっております。瀧研究室{number}{name_category}と申します。\n{time}で{switch}致します。\n目的：{work_category}\n内容：{detail}\nよろしくお願いいたします。'
                        )
                    # gmailに送信
                    send_outlook_mail(msg)
                    return schedule.CancelJob()            
                schedule.every().day.at(time_utc).do(send_mai_message)
                st.text(f'{name_category}さん！{time}に{switch}しました。')  
                while True:
                    schedule.run_pending()
                    sleep(31)
            elif name_category == '安田希亜良':
                def send_ara_message():
                    """
                    メイン処理
                    """
                    # MIME形式に変換
                    msg = make_mime(
                        mail_to='on12kyamamura@ec.usp.ac.jp', #送信したい宛先を指定
                        subject=f'出退勤記録簿報告について　瀧研究室 {number}{name_category}',
                        body=f'お世話になっております。瀧研究室{number}{name_category}と申します。\n{time}で{switch}致します。\n目的：{work_category}\n内容：{detail}\nよろしくお願いいたします。'
                        )
                    # gmailに送信
                    send_outlook_mail(msg)
                    return schedule.CancelJob()          
                schedule.every().day.at(time_utc).do(send_ara_message)
                st.text(f'{name_category}さん！{time}に{switch}しました。')  
                while True:
                    schedule.run_pending()
                    sleep(31)
            elif name_category == '山村孝輝':
                def send_yama_message():
                    """
                    メイン処理
                    """
                    # MIME形式に変換
                    msg = make_mime(
                        mail_to='on12kyamamura@ec.usp.ac.jp', #送信したい宛先を指定
                        subject=f'出退勤記録簿報告について　瀧研究室 {number}{name_category}',
                        body=f'お世話になっております。瀧研究室{number}{name_category}と申します。\n{time}で{switch}致します。\n目的：{work_category}\n内容：{detail}\nよろしくお願いいたします。'
                        )
                    # gmailに送信
                    send_outlook_mail(msg)
                    return schedule.CancelJob()
                schedule.every().day.at(time_utc).do(send_yama_message)
                st.text(f'{name_category}さん！{time}に{switch}しました。')  
                while True:
                    schedule.run_pending()
                    sleep(31)
            elif name_category == '鈴木美結':
                def send_miyu_message():
                    """
                    メイン処理
                    """
                    # MIME形式に変換
                    msg = make_mime(
                        mail_to='on12kyamamura@ec.usp.ac.jp', #送信したい宛先を指定
                        subject=f'出退勤記録簿報告について　瀧研究室 {number}{name_category}',
                        body=f'お世話になっております。瀧研究室{number}{name_category}と申します。\n{time}で{switch}致します。\n目的：{work_category}\n内容：{detail}\nよろしくお願いいたします。'
                        )
                    # gmailに送信
                    send_outlook_mail(msg)
                    return schedule.CancelJob()     
                schedule.every().day.at(time_utc).do(send_miyu_message)
                st.text(f'{name_category}さん！{time}に{switch}しました。')  
                while True:
                    schedule.run_pending()
                    sleep(31)
            elif name_category == '馬場大輝':
                def send_baba_message():
                    """
                    メイン処理
                    """
                    # MIME形式に変換
                    msg = make_mime(
                        mail_to='on12kyamamura@ec.usp.ac.jp', #送信したい宛先を指定
                        subject=f'出退勤記録簿報告について　瀧研究室 {number}{name_category}',
                        body=f'お世話になっております。瀧研究室{number}{name_category}と申します。\n{time}で{switch}致します。\n目的：{work_category}\n内容：{detail}\nよろしくお願いいたします。'
                        )
                    # gmailに送信
                    send_outlook_mail(msg)
                    return schedule.CancelJob()
                schedule.every().day.at(time_utc).do(send_baba_message)
                st.text(f'{name_category}さん！{time}に{switch}しました。')  
                while True:
                    schedule.run_pending()
                    sleep(31)
            elif name_category == '宮原舞':
                def send_miyamai_message():
                    """
                    メイン処理
                    """
                    # MIME形式に変換
                    msg = make_mime(
                        mail_to='on12kyamamura@ec.usp.ac.jp', #送信したい宛先を指定
                        subject=f'出退勤記録簿報告について　瀧研究室 {number}{name_category}',
                        body=f'お世話になっております。瀧研究室{number}{name_category}と申します。\n{time}で{switch}致します。\n目的：{work_category}\n内容：{detail}\nよろしくお願いいたします。'
                        )
                    # gmailに送信
                    send_outlook_mail(msg)
                    return schedule.CancelJob()
                schedule.every().day.at(time_utc).do(send_miyamai_message)
                st.text(f'{name_category}さん！{time}に{switch}しました。')  
                while True:
                    schedule.run_pending()
                    sleep(31)
            elif name_category == '坂本愛実':
                def send_saka_message():
                    """
                    メイン処理
                    """
                    # MIME形式に変換
                    msg = make_mime(
                        mail_to='on12kyamamura@ec.usp.ac.jp', #送信したい宛先を指定
                        subject=f'出退勤記録簿報告について　瀧研究室 {number}{name_category}',
                        body=f'お世話になっております。瀧研究室{number}{name_category}と申します。\n{time}で{switch}致します。\n目的：{work_category}\n内容：{detail}\nよろしくお願いいたします。'
                        )
                    # gmailに送信
                    send_outlook_mail(msg)
                    return schedule.CancelJob()          
                schedule.every().day.at(time_utc).do(send_saka_message)
                st.text(f'{name_category}さん！{time}に{switch}しました。')  
                while True:
                    schedule.run_pending()
                    sleep(31)
            else:
                print('適切に入力してください。')
                
            st.text(f'{name_category}さん！{time}に{switch}しました。')  
            
#画像
    image = Image.open('20221025_055301993_iOS.jpg')
    st.image(image, width=500)

if selected == "Private Report":
    st.header("Private Report")
    with st.form("saved_periods"):
        name = st.selectbox("Select Name:", get_all_profile())
        submitted = st.form_submit_button("Display")
        if submitted:
            df = pd.DataFrame()
            for i in get_all_daytime():
                data = db.get_private(i)
                name_data = data.get("name")
                if name == name_data:
                    date = data.get("date")
                    work = data.get("work")
                    time = data.get("time")
                    switch = data.get("switch")
                    i = pd.DataFrame(
                        data = [{'date':date,
                                'work':work, 
                                'time':time, 
                                'switch':switch}],
                                index = None,)
                    df = pd.concat([df,i])

            

            st.table(df)
            import base64
            csv = df.to_csv(index=False,encoding='shift_jis')  
            b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="result.csv">download</a>'
            st.markdown(f"ダウンロードする {href}", unsafe_allow_html=True)




