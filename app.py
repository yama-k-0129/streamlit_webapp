from http import client
import numpy as np
import calendar
from operator import index
import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime, timezone, timedelta
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

    # code = '''
    # import streamlit as st

    
    work_category = st.radio(
            '業務内容',
            ('データ解析補助','研究補佐','講義資料作成','講義補佐','TA','その他')
        )
    if work_category == 'その他':
            work_category = st.text_input(
                '業務内容'
            )

    with st.form(key='profile_form'):
    #テキストボックス
        # address = st.text_input('住所')

        #セレクトボックス#ラジオボタンならst.radioにするだけ
        name_category = st.radio(
            '名前',
            ('泉野珠穂', '早崎水彩','藤原未奈','清水麻衣','長畑智大','安田希亜良','山村孝輝','上田','鈴木','馬場','宮原'),
            key = "name"
        )
        
        place = st.text_input('場所')
        

        #複数選択
        # work_category = st.radio(
        #     '業務内容',
        #     ('データ解析補助','研究補佐','講義資料作成','講義補佐','TA','その他')
        # )
        # if work_category == 'その他':
        #     work_category = st.text_input(
        #         '業務内容'
        #     )
            
        detail = st.text_input('詳細内容')
        
        #日付選択
        date = st.date_input(
            '日付', datetime.now(timezone(timedelta(hours=9))))

        #時間選択
        time = st.time_input(
            '時間',datetime.now(timezone(timedelta(hours=9)))
        )

        #勤務
        switch = st.radio(
            "出退勤",
            ('出勤','退勤')
        )




        #ボタン
        submit_btn = st.form_submit_button('送信')
        # cancel_btn = st.form_submit_button('退勤')
        # print(f'submit_btn: {submit_btn}')
        # print(f'cancel_btn: {cancel_btn}')
        if submit_btn:
            dt = datetime.combine(date,time)#日本時間のdatetimeオブジェクトが生成
            dt_utc = dt.astimezone(timezone.utc)#時差が反映され-9時間され，tzinfoが付加されたdatetimeオブジェクトが生成
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
            my_account = 'kouki0129kouki0129@gmail.com'
            my_password = pas

            def send_outlook_mail(msg):
                """
                引数msgをOutlookで送信
                """
                server = smtplib.SMTP('smtp.gmail.com', 587)
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
                msg['From'] = my_account #送信元
                return msg

            def send_my_message():
                """
                メイン処理
                """
                # MIME形式に変換
                msg = make_mime(
                    mail_to='on12kyamamura@ec.usp.ac.jp', #送信したい宛先を指定
                    subject=f'出退勤記録簿報告について　瀧研究室　{name_category}',
                    body=f'いつもお世話になっております。瀧研究室{name_category}と申します。\n{time}で{switch}致します。\n目的：{work_category}\nよろしくお願いいたします。'
                    )
                # gmailに送信
                send_outlook_mail(msg)
                return schedule.CancelJob()
            
            schedule.every().day.at(time_utc).do(send_my_message)
            st.text(f'{name_category}さん！{time}に{switch}しました。')
            
            while True:
                schedule.run_pending()
                sleep(1)
            
            # data = pd.DataFrame([[name_category,work_category,date,start_time]],columns =['name','workcategory','date','starttime'])
            # df = df.append(data)
            # st.text(f'{name_category}さん！{start_time}から勤務を開始しました。')
            # st.table(df)
            # st.text(f'年齢層：{name_category}')
            # st.text(f'趣味：{", ".join(hobby)}')
        # if cancel_btn:
        #     tdelta = datetime.strptime({start_time}) - datetime.strptime({stop_time})
        #     data = [stop_time,tdelta]
        #     sr2 = pd.Series(data, name="sr2")
        #     df = pd.concat([df, pd.DataFrame(data= sr2.values.reshape(1,-1),columns=['stop_time','time'])],axis=0)
        #     # df['stoptime'] = stop_time
        #     # df['time'] = df['starttime'] - df['stoptime']
        #     st.text(f'{name_category}さん、{stop_time}までお疲れさまでした！')

    # st.table(df)
    # import base64
    # csv = df.to_csv(index=False)  
    # b64 = base64.b64encode(csv.encode()).decode()
    # href = f'<a href="data:application/octet-stream;base64,{b64}" download="result.csv">download</a>'
    # st.markdown(f"ダウンロードする {href}", unsafe_allow_html=True)
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




