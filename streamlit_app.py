import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import rc, font_manager
import pandas as pd

# 폰트 설정
font_path = "./malgun.ttf"  # Windows 기준
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# Streamlit 기본 설정
st.set_page_config(layout="wide")
st.title("YES24 베스트셀러 장르 및 가격 분석")

if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

st.markdown("""
본 웹 앱은 Selenium을 이용해 수집한 YES24 국내도서 베스트셀러 데이터를 바탕으로 장르와 가격의 분포를 시각적으로 분석한다.
""")

# 데이터 
try:
    df_prices = pd.read_excel("./data/yes24_best_prices.xlsx")
    df_genres = pd.read_excel("./data/yes24_best_genres.xlsx")

    prices = df_prices["price"]
    genres = df_genres["genre"].value_counts()

    df = df_genres.merge(df_prices, on="book_id")

    total = genres.sum()
    ratio = genres / total

    # 5% 이상 / 미만 분리
    main_genres = genres[ratio >= 0.05]
    others = genres[ratio < 0.05].sum()

    # 기타 추가
    if others > 0:
        main_genres = pd.concat(
            [main_genres, pd.Series({"기타": others})]
        )

    # 크기 기준 내림차순 정렬
    main_genres = main_genres.sort_values(ascending=False)
    # 크롤링 날짜 
    date = sorted(df_prices["crawl_date"].unique())

    col_left, col_center, col_right = st.columns(3)
    # 왼쪽: 장르별 개수 파이 차트
    with col_left:
        st.subheader("장르별 도서 개수 분포")

        fig1, ax1 = plt.subplots(figsize = (4,4), dpi = 200)
        ax1.pie(
            main_genres.values,
            labels=main_genres.index,
            autopct="%1.1f%%",
            startangle=90
        )
        for text in ax1.texts:
            text.set_fontsize(7)
        ax1.axis("equal")
        plt.tight_layout()
        st.pyplot(fig1)

    # 중앙: 전체 가격 분포
    with col_center:
        st.subheader("전체 도서 가격 분포")

        fig2, ax2 = plt.subplots()
        ax2.hist(prices, bins=10)
        ax2.set_xlabel("가격 (원)")
        ax2.set_ylabel("도서 수")

        st.pyplot(fig2)
        

    # 오른쪽: 장르별 가격 분포
    with col_right:
        st.subheader("선택한 장르의 가격 분포")        
        
        fig3, ax3 = plt.subplots()
        ax3.hist(
            df[df["genre"] == st.session_state.get("selected_genre", genres.index[0])]["price"],
            bins=8
        )
        ax3.set_xlabel("가격")
        ax3.set_ylabel("도서 수")
        ax3.set_title(f"{st.session_state.get("selected_genre", genres.index[0])} 장르 가격 분포")
        st.pyplot(fig3)

        selected_genre = st.selectbox(
            "장르 선택",
            main_genres.index[1:],
            key="selected_genre"
        )
        
    # 그래프 별 설명
    txt_left, txt_center, txt_right = st.columns(3)
    with txt_left:
        st.write('''
                본 파이 차트는 YES24 국내도서 베스트셀러 상위 240개 중 나이제한 상품을 제외한 목록에 포함된 도서들의 장르 분포를 시각화한 것이다. 
                각 장르는 해당 장르에 속한 도서의 개수를 기준으로 구성되었으며, 전체 대비 비율을 통해 베스트셀러 시장에서 어떤 장르가 상대적으로 높은 비중을 차지하는지를 파악할 수 있다.
                다양한 장르를 가진 도서는 각 장르에 모두 포함하였다.
                또한 전체 비중의 5% 미만을 차지하는 소수 장르는 ‘기타’ 항목으로 통합하여 시각적 가독성을 향상시켰으며, 장르 비중이 큰 순서대로 정렬함으로써 주요 장르의 상대적 중요도를 직관적으로 확인할 수 있도록 하였다.
                 ''')
    with txt_center:
        st.write('''
                본 그래프는 YES24 베스트셀러 도서들의 전체 가격 분포를 나타낸 것이다. 도서 가격을 일정한 구간으로 나누어 각 가격대에 속하는 도서의 개수를 집계함으로써, 베스트셀러 도서들이 주로 형성되는 가격 범위를 확인할 수 있다.
                이를 통해 베스트셀러 시장에서 소비자가 선호하는 가격대가 어느 구간에 집중되어 있는지 파악할 수 있다.
                 ''')  
    with txt_right:
        st.write('''
                본 그래프는 사용자가 선택한 특정 장르에 대해 해당 장르에 속한 도서들의 가격 분포를 시각화한 것이다. 
                전체 가격 분포와 달리, 장르별 가격 특성을 개별적으로 분석할 수 있도록 설계되었다.
                이를 통해 특정 장르의 가격대가 분포되어있는 구조를 파악할 수 있으며, 장르별 출판 및 소비 특성의 차이를 분석하는 데 활용할 수 있다.
                 ''')
        
    st.write(f"{date[0]} 기준")
except Exception as e:
    print(e)
    st.write("아직 분석 전입니다..")