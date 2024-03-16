import streamlit as st 
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from streamlit_option_menu import option_menu
from PIL import Image
import base64
import gspread

ga = gspread.service_account(filename='key.json')
gh = ga.open('Uni_Alarm')

st.set_page_config(page_title="Alarm Manager", page_icon="👓")
hide_menu = """ 
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_menu, unsafe_allow_html=True)

def main():
    st.title("스마트알람모니터링")
    add_bg_from_local('./images/b_img.jpg')
    password = st.text_input("비밀번호(4자리)를 입력하세요", type='password', key='1')
    login = st.checkbox("Login")
    cancel = st.button("취 소", use_container_width = True)
    if cancel:
        done()
    if login or password == '1':
        add_bg_from_local('./images/in.png')
        st.write("😊 핸드폰은 'Close'버튼을 눌러 종료하세요")
        select = option_menu(
            menu_title="",
            options=["알람", "전체", "종 료"],
            icons=["house", "book"],
            orientation="horizontal"
            )
        if select == "알람":
            count = st_autorefresh(interval=10000, limit=50, key="reload_count")
            if count == 49:
                st.write("자동업데이트종료, 다시 로그인하세요!")
            es = readAlarm()
            ef = pd.DataFrame(es, columns=['위치명','알람내용', '위치도면', '알람상태', '알람정지', '리셋', '통신(분)'])
            st.dataframe(ef, width=700, hide_index=True, column_order=('위치명', '알람내용', '알람정지'))
            for e in es:
                if e[2] == '':
                    image = Image.open('./images/logo.png')
                    st.image(image)
                else:
                    image = Image.open('./images/' + e[2] + '.jpg')
                    st.image(image)
                    if st.button(e[0] + '__알람홀드', use_container_width=True):
                        hsetDb(e[2])
                    elif st.button(e[0] + '__알람리셋', use_container_width=True):
                        esetDb(e[2])
                    elif st.button("전체확인", use_container_width=True):
                        setDb()

        elif select == "전체":
            ts = readData()
            tf = pd.DataFrame(ts, columns=['위치명','알람내용', '위치도면', '통신상태', '통신(분)', '시스템(분)', '현재시간', '변환(분)'])
            st.dataframe(tf, width=700, hide_index=True, column_order=('위치명', '알람내용', '통신상태'))
            if st.button('Update'):
                st.toast('Update 완료!')
            for t in ts:
                image = Image.open('./images/' + t[2] + '.jpg')
                st.image(image)
                st.subheader(t[0])
            st.stop()    

        elif select == "종 료":
            done()
    else:
        st.error("Login failed.")        
def done():
    st.markdown("""
                <meta http-equiv="refresh" content="0; url='https://www.google.com'" />
                """, unsafe_allow_html=True
            )  
              
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

def readAlarm():
    wks = gh.worksheet('AlarmSt')
    event = []
    res = wks.get_all_values()
    for row in res[1:]:
        event.append(row)    
    return event

def readData():
    wks = gh.worksheet('ComSt')
    data = []
    res = wks.get_all_values()
    for row in res[1:]:
        data.append(row)    
    return data

def setDb():
    wks = gh.worksheet('ListSt')
    req = wks.get_all_values()
    for s_row in req[1:]:
        if s_row[3] == '_On':
            wks.update_acell('F'+ str(s_row[2]), 'Off')

def hsetDb(pos):
    wks = gh.worksheet('ListSt')
    wks.update_acell('E'+ pos, 'Set')

def esetDb(pos):
    wks = gh.worksheet('ListSt')
    wks.update_acell('F'+ pos, 'Set')    

if __name__ == "__main__":
    main() 
