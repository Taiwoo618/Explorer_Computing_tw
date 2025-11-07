import streamlit as st
import pandas as pd

tab1, tab2 = st.tabs(["자기소개", "시간표"])

with tab1:
    st.title("나의 소개 페이지")
    st.header("자기소개")
    st.text("안녕하세요, 제 이름은 김태우입니다.")
    st.write("저는 **게임개발**과 *웹툰*에 관심이 있습니다.")
    st.header("좋아하는 것")
    st.write("저는 게임과 웹툰을 좋아합니다")
    st.write("가장 자주 방문하는 사이트는 [유튜브](https://www.youtube.com)입니다.")
    st.header("앞으로의 목표")
    st.write("앞으로 다양한 프로젝트를 진행하면서 실력을 키우고 싶습니다.")
    st.caption("제가 좋아하는 파이썬 코드 예시")
    st.code("for i in range(9):\n   print(\"*\" * i)", language = "python")
    st.caption("인수 분해")
    st.latex(r"a^2 + 2ab + b^2 = (a+b)^2")
with tab2:
    data = {"시간": ["오전", "오후"], "월요일": ["서양 조경의 역사와 이론", "조경 계량분석기법"], "화요일": ["", ""], "수요일": ["", ""], "목요일": ["", "조경설계2"], "금요일": ["컴퓨팅탐색", "국토 및 지역계획"]}
    df = pd.DataFrame(data)
    json_data = {"서양 조경의 역사와 이론": {"교수": "배정한", "강의실": "200-9207"}, "조경계량분석기법": {"교수": "윤희연", "강의실": "200-9210"}, "조경설계2": {"교수": "정욱주", "강의실": "200-9207"}, "컴퓨팅 탐색": {"교수": "변해선", "강의실": "26-104"}, "국토 및 지역계획": {"교수": "홍사흠", "강의실": "35-316"}}

    st.title("나의 수업 시간표")

    st.header("정적 시간표")
    st.table(df)

    st.header("수업 정보")
    st.json(json_data)

    st.header("이번 학기 요약")
    st.metric(label = "수강 과목 수", value = "5", delta = "-2")
    st.metric(label = "총 학점", value = "15", delta = "-4")