import streamlit as st 
import pandas as pd
from back_image import add_bg_from_local
from db import readAlarm, readData, setDb, esetDb
from streamlit_autorefresh import st_autorefresh
from streamlit_option_menu import option_menu
from PIL import Image

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
            st_autorefresh(interval=10000, key="reload_count")
            es = readAlarm()
            ef = pd.DataFrame(es, columns=['위치명','알람내용', '위치도면', '알람상태', '알람확인', '리셋', '통신(분)'])
            st.dataframe(ef, width=700, hide_index=True, column_order=('위치명', '알람내용', '리셋'))
            for e in es:
                if e[2] == '':
                    image = Image.open('./images/logo.png')
                    st.image(image)
                else:
                    image = Image.open('./images/' + e[2] + '.jpg')
                    st.image(image)
                    if st.button(e[0] + '__알람리셋', use_container_width=True):
                        esetDb(e[2])
                        st.rerun()
                    elif st.button("전체확인", use_container_width=True):
                        setDb()
                        st.rerun()

        elif select == "전체":
            ts = readData()
            tf = pd.DataFrame(ts, columns=['위치명','알람내용', '위치도면', '통신상태', '통신(분)', '시스템(분)', '현재시간'])
            st.dataframe(tf, width=700, hide_index=True, column_order=('위치명', '알람내용', '통신상태'))
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

if __name__ == "__main__":
    main() 