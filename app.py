from http import client
import numpy as np
import calendar
from operator import index
import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime, timezone,timedelta
from streamlit_option_menu import option_menu #pip install streamlit-option-menu
import database as db #local import 






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

months = list(calendar.month_name[1:])
names = ['泉野珠穂','早崎水彩','藤原未奈','清水麻衣','長畑智大','安田希亜良','山村孝輝','上田','鈴木','馬場','宮原']


if selected == "Entry":
    st.text('名前、仕事内容、時間を入力してください。')

    # code = '''
    # import streamlit as st

    
    

    with st.form(key='profile_form'):
    #テキストボックス
        # address = st.text_input('住所')

        #セレクトボックス#ラジオボタンならst.radioにするだけ
        name_category = st.radio(
            '名前',
            ('泉野珠穂', '早崎水彩','藤原未奈','清水麻衣','長畑智大','安田希亜良','山村孝輝','上田','鈴木','馬場','宮原'),
            key = "name"
        )

        #複数選択
        work_category = st.radio(
            '業務内容',
            ('データ解析補助','研究補佐','講義資料作成','講義補佐','TA')
        )

        #日付選択
        date = st.date_input(
            '日付')

        #時間選択
        time = st.time_input(
            '時間',datetime.time()
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
            st.text(f'{name_category}さん！{time}に{switch}しました。')
            daytime = str(date) + "_" + str(time) + "_" + str(name_category)
            name = str(name_category)
            work = str(work_category)
            date = str(date)
            time = str(time) 
            switch = str(switch)
            db.insert_profile(daytime, name, date, work, time, switch)
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



