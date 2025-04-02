import streamlit as st
import streamlit.components.v1 as components
import openai
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
import json
import time
import datetime
import pandas as pd
import io
import base64
import random

# .env 파일에서 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="FASHION TREND-SETTER",
    page_icon=None,
    layout="wide"
)

# 세션 상태 초기화
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")
if 'unsplash_api_key' not in st.session_state:
    st.session_state.unsplash_api_key = os.getenv("UNSPLASH_ACCESS_KEY", "")

# CSS 스타일 적용
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
    }
    .trend-image {
        border-radius: 10px;
        width: 100%;
    }
    .related-keyword {
        display: inline-block;
        background-color: #f0f0f0;
        padding: 5px 10px;
        border-radius: 15px;
        margin-right: 8px;
        margin-bottom: 8px;
        font-size: 14px;
    }
    .footer-small {
        font-size: 14px;
        margin-top: 40px;
    }
    .footer-tiny {
        font-size: 12px;
        color: #6c757d;
        margin-top: 5px;
    }
    .footer-container {
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid #eaeaea;
    }
    .api-section {
        margin-bottom: 20px;
    }
    .sidebar-footer {
        position: absolute;
        bottom: 0;
        left: 0;
        padding: 20px;
        width: 100%;
    }
    
    /* 사이드바 스타일 변경 */
    .sidebar.sidebar-content {
        background: linear-gradient(to bottom, #f0f0f0, #d0d0d0);
    }
    
    /* All Things Fashion 폰트 변경 */
    .all-things-fashion {
        font-size: 1.2em;
        font-weight: 700;
        margin-bottom: 5px;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* FASHION TREND-SETTER 입체적 스타일 */
    .fashion-trend-title {
        font-size: 1.8em;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #333;
        text-shadow: 2px 2px 3px rgba(0,0,0,0.1);
        background: linear-gradient(to bottom, #444, #000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
        line-height: 1.2;
    }
    
    /* 패션 뉴스 섹션 스타일 */
    .news-section {
        padding: 10px 0;
        margin: 20px 0;
        position: relative;
    }
    .news-container {
        display: flex;
        flex-wrap: nowrap;
        gap: 12px;
        margin: 20px 0;
        overflow-x: auto;
        padding: 10px 0 20px 0;
        white-space: nowrap;
        -webkit-overflow-scrolling: touch;
        scroll-behavior: smooth;
        scrollbar-width: thin;
        scrollbar-color: #888 #f1f1f1;
        width: 100%;
        position: relative;
        scroll-snap-type: x mandatory;
    }
    .news-container::-webkit-scrollbar {
        height: 4px;
    }
    .news-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    .news-container::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 10px;
    }
    .news-container::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    .news-card {
        background-color: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 3px 5px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin: 5px 0;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .news-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    }
    .news-card img {
        width: 100%;
        height: 180px;
        object-fit: cover;
        object-position: center;
    }
    .news-content {
        padding: 10px;
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }
    .news-category {
        font-size: 10px;
        color: #6c757d;
        margin-bottom: 2px;
        font-weight: 600;
    }
    .news-title {
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 6px;
        line-height: 1.2;
        height: 45px;
        overflow: hidden;
    }
    .news-info {
        font-size: 10px;
        color: #6c757d;
        margin-top: auto;
    }

    /* TREND NEWS 제목 스타일 */
    .trend-news-title {
        font-size: 1.8em;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #333;
        margin-bottom: 10px;
        padding-top: 10px;
    }

    /* 네비게이션 버튼 스타일 */
    .stButton > button {
        border-radius: 50%;
        width: 40px !important;
        height: 40px !important;
        font-weight: bold;
        font-size: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0 !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        background-color: white;
        border: 1px solid #eaeaea;
        color: #333;
        transition: all 0.3s ease;
    }
    .stButton > button:hover:enabled {
        background-color: #f5f5f5;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    .stButton > button:disabled {
        opacity: 0.4;
        cursor: not-allowed;
    }
    .nav-button-container {
        display: flex;
        height: 100%;
        align-items: center;
        justify-content: center;
    }

    /* 스타일링 검색 화면의 안내 문구 스타일 추가 */
    .styling-guide {
        font-size: 13px;
        color: #6c757d;
        margin: 0 0 5px 2px;
    }

    /* 네비게이션 버튼 스타일 */
    .nav-button {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        background-color: white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        cursor: pointer;
        z-index: 10;
        border: none;
    }
    .nav-prev {
        left: -20px;
    }
    .nav-next {
        right: -20px;
    }
    .news-cols-container {
        position: relative;
        padding: 0 25px;
    }
    .stButton > button {
        font-weight: bold;
    }

    /* 메인 컨텐츠 섹션 스타일 */
    .main-content {
        margin-top: 30px;
    }

    /* 메인 페이지 옵션 버튼 */
    .main-option-button {
        margin-top: 10px;
        height: 100px !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        background-color: #f8f9fa !important;
        color: #333 !important;
        border: 1px solid #ddd !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    .main-option-button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15) !important;
        background-color: #fff !important;
    }
    .back-button {
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 사이드바 스타일 변경
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #f5f5f5, #e0e0e0, #d0d0d0);
    }
</style>
""", unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.markdown('<div class="fashion-trend-title">FASHION<br>TREND-SETTER</div>', unsafe_allow_html=True)
    
    # 패션 트렌드/용어 선택 섹션 숨기기
    # st.markdown('<div class="all-things-fashion">All Things Fashion</div>', unsafe_allow_html=True)
    # search_option = st.radio(
    #     "",
    #     ["Trend & Information", "Brands", "Styling Search"]
    # )
    search_type = "패션 트렌드"  # 트렌드 검색 기본값
    
    # API 키 입력 섹션 (사이드바)
    with st.expander("API 키 설정"):
        openai_key = st.text_input("OpenAI API 키", value=st.session_state.openai_api_key, type="password")
        unsplash_key = st.text_input("Unsplash API 키 (선택사항)", value=st.session_state.unsplash_api_key, type="password")
        
        if st.button("API 키 저장"):
            st.session_state.openai_api_key = openai_key
            st.session_state.unsplash_api_key = unsplash_key
            st.success("API 키가 저장되었습니다.")
    
    # 푸터 정보 (사이드바 하단)
    st.markdown("<div class='sidebar-footer'>", unsafe_allow_html=True)
    st.markdown("<div class='footer-small'>### FASHION TREND-SETTER 앱 정보</div>", unsafe_allow_html=True)
    st.markdown("<div class='footer-tiny'>이 앱은 OpenAI API를 사용하여 패션 트렌드와 용어에 대한 정보를 제공합니다.<br>트렌드 이미지는 Unsplash API를 통해 제공됩니다.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 패션 뉴스 섹션 함수화 (모든 페이지 상단에 표시)
def display_trend_news():
    # TREND NEWS 타이틀과 스타일 적용
    st.markdown("""
    <div class="trend-news-title">TREND NEWS</div>
    """, unsafe_allow_html=True)
    
    # 세션 상태에 뉴스 인덱스가 없으면 초기화
    if 'news_index' not in st.session_state:
        st.session_state.news_index = 0
    
    # 패션 뉴스 목록 (실제로는 API 또는 데이터베이스에서 가져올 수 있음)
    fashion_news = [
        {
            "category": "트렌드",
            "title": "2025 S/S 컬렉션에서 주목해야 할 5가지 트렌드",
            "date": "2025.03.15",
            "author": "패션 에디터",
            "image": "https://images.unsplash.com/photo-1605296867304-46d5465a13f1?w=600"
        },
        {
            "category": "컬렉션",
            "title": "파리 패션위크 하이라이트: 샤넬과 디올의 새로운 비전",
            "date": "2025.03.12",
            "author": "패션 저널리스트",
            "image": "https://images.unsplash.com/photo-1581044777550-4cfa60707c03?w=600"
        },
        {
            "category": "지속가능성",
            "title": "친환경 패션의 미래: 리사이클 소재의 혁신",
            "date": "2025.03.10",
            "author": "환경 전문가",
            "image": "https://images.unsplash.com/photo-1523381294911-8d3cead13475?w=600"
        },
        {
            "category": "스트리트 패션",
            "title": "서울 스트리트 스타일: Z세대가 이끄는 새로운 트렌드",
            "date": "2025.03.08",
            "author": "스트리트 포토그래퍼",
            "image": "https://images.unsplash.com/photo-1600950207944-0d63e8edbc3f?w=600"
        },
        {
            "category": "디자이너",
            "title": "신진 디자이너 특집: 미래의 패션을 선도할 10인",
            "date": "2025.03.05",
            "author": "패션 큐레이터",
            "image": "https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=600"
        },
        {
            "category": "컬래버레이션",
            "title": "럭셔리 브랜드와 아티스트의 만남: 경계를 허무는 협업",
            "date": "2025.03.03",
            "author": "아트 디렉터",
            "image": "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?w=600"
        },
        {
            "category": "기술",
            "title": "패션테크의 진화: AI가 디자인하는 맞춤형 의류",
            "date": "2025.03.01",
            "author": "테크 애널리스트",
            "image": "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=600"
        },
        {
            "category": "액세서리",
            "title": "2025년 주목해야 할 액세서리 트렌드",
            "date": "2025.02.28",
            "author": "스타일리스트",
            "image": "https://images.unsplash.com/photo-1611085583191-a3b181a88401?w=600"
        },
        {
            "category": "뷰티",
            "title": "런웨이에서 영감받은 메이크업 트렌드",
            "date": "2025.02.25",
            "author": "뷰티 에디터",
            "image": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600"
        },
        {
            "category": "이벤트",
            "title": "2025 메트 갈라: 패션의 밤을 빛낸 스타들",
            "date": "2025.02.20",
            "author": "연예 기자",
            "image": "https://images.unsplash.com/photo-1533928298208-27ff66555d8d?w=600"
        }
    ]
    
    # 컨테이너 생성
    with st.container():
        # 뉴스 카드를 표시할 레이아웃
        news_cols = st.columns([0.5, 4, 0.5])  # 왼쪽 버튼, 카드, 오른쪽 버튼

        # 이전 버튼 (왼쪽)
        with news_cols[0]:
            st.markdown('<div class="nav-button-container">', unsafe_allow_html=True)
            prev_disabled = st.session_state.news_index <= 0
            if st.button("◀", key="prev_news_btn", disabled=prev_disabled):
                if st.session_state.news_index > 0:
                    st.session_state.news_index -= 4
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 뉴스 카드 표시 (중앙)
        with news_cols[1]:
            cards_cols = st.columns(4)
            end_idx = min(st.session_state.news_index + 4, len(fashion_news))
            
            for i, col in enumerate(cards_cols):
                idx = st.session_state.news_index + i
                if idx < end_idx and idx < len(fashion_news):
                    news = fashion_news[idx]
                    with col:
                        st.markdown(f"""
                        <div class="news-card">
                            <img src="{news['image']}" alt="{news['title']}">
                            <div class="news-content">
                                <div class="news-category">{news['category']}</div>
                                <div class="news-title">{news['title']}</div>
                                <div class="news-info">{news['date']} | {news['author']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        # 다음 버튼 (오른쪽)
        with news_cols[2]:
            st.markdown('<div class="nav-button-container">', unsafe_allow_html=True)
            next_disabled = st.session_state.news_index >= len(fashion_news) - 4
            if st.button("▶", key="next_news_btn", disabled=next_disabled):
                if st.session_state.news_index + 4 < len(fashion_news):
                    st.session_state.news_index += 4
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# 타이틀
st.title("FASHION TREND-SETTER")

# 첫 페이지 상태 관리
if 'page' not in st.session_state:
    st.session_state.page = 'main'  # 초기 페이지는 'main'

# 메인 페이지일 때만 TREND NEWS 표시
if st.session_state.page == 'main':
    # TREND NEWS 표시
    display_trend_news()
    
    # 메인 컨텐츠 구분선
    st.markdown("<hr/>", unsafe_allow_html=True)
    
    # 선택 버튼들
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 버튼 스타일 추가
    st.markdown("""
    <style>
    div.stButton > button {
        height: 100px;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 8px;
        background-color: #f8f9fa;
        color: #333;
        border: 2px solid #FF0000 !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        background-color: #fff;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Trend & Information", use_container_width=True, key="trend_info_btn", help="패션 트렌드와 용어 정보 검색"):
            st.session_state.page = "trend_info"
            st.session_state.search_option = "Trend & Information"
            st.rerun()
    
    with col2:
        if st.button("Brands", use_container_width=True, key="brands_btn", help="패션 브랜드 정보 검색"):
            st.session_state.page = "brands"
            st.session_state.search_option = "Brands"
            st.rerun()
    
    with col3:
        if st.button("Styling Search", use_container_width=True, key="styling_btn", help="패션 스타일링 이미지 검색"):
            st.session_state.page = "styling"
            st.session_state.search_option = "Styling Search"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 다른 페이지 표시
else:
    # 검색 페이지용 UI
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # 뒤로가기 버튼 스타일
    st.markdown("""
    <style>
    /* 뒤로가기 버튼 스타일 */
    div.stButton > button:first-child {
        background-color: #f1f3f5;
        border-color: #FF0000 !important;
        border-width: 2px !important;
        color: #495057;
        font-weight: 500;
        margin-bottom: 20px;
    }
    div.stButton > button:first-child:hover {
        background-color: #e9ecef;
        border-color: #FF0000 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 뒤로가기 버튼
    if st.button("← 메인으로 돌아가기"):
        st.session_state.page = "main"
        st.rerun()
    
    # 선택된 옵션에 따른 페이지 표시
    if st.session_state.page == "trend_info":
        st.markdown("### 패션 트렌드/용어")
        search_query = st.text_input("", placeholder="(예: Y2K 패션, 아방가르드, 하이엔드 등)", key="trend_search")
        
        # GPT를 통한 트렌드 정보 검색
        def get_fashion_trend_info(query):
            try:
                if not st.session_state.openai_api_key:
                    st.error("OpenAI API 키를 입력해주세요. 사이드바의 'API 키 설정'에서 입력할 수 있습니다.")
                    return None
                
                client = OpenAI(api_key=st.session_state.openai_api_key)
                
                # 최대 3번 시도
                max_attempts = 3
                for attempt in range(max_attempts):
                    try:
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "당신은 패션 용어와 트렌드에 대한 설명을 제공하는 패션 전문가입니다. 사용자가 입력한 패션 용어나 트렌드에 대해 자세히 설명해주세요."},
                                {"role": "user", "content": f"다음 패션 용어/트렌드의 의미와 특징을 알려주세요: {query}"}
                            ],
                            temperature=0.7,
                            max_tokens=500
                        )
                        
                        content = response.choices[0].message.content
                        if content and len(content.strip()) > 0:
                            return {"description": content.strip()}
                        else:
                            if attempt < max_attempts - 1:
                                time.sleep(1)  # 잠시 대기 후 재시도
                                continue
                            else:
                                st.error("API에서 빈 응답을 받았습니다. 다른 검색어로 시도해 보세요.")
                                return None
                    except Exception as e:
                        if attempt < max_attempts - 1:
                            time.sleep(1)  # 잠시 대기 후 재시도
                            continue
                        else:
                            raise e
                
                return None
            except Exception as e:
                st.error(f"OpenAI API 호출 중 오류 발생: {e}")
                return None

        # 패션 용어/브랜드 정보 검색
        def get_fashion_term_info(query):
            try:
                # API 키 확인
                if not st.session_state.openai_api_key:
                    st.error("OpenAI API 키를 입력해주세요. 사이드바의 'API 설정'에서 입력할 수 있습니다.")
                    return None
                
                # OpenAI 클라이언트 초기화
                client = OpenAI(api_key=st.session_state.openai_api_key)
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "당신은 패션 전문가입니다. 패션 용어와 브랜드에 대한 상세한 정보를 제공해주세요. 응답은 반드시 유효한 JSON 형식이어야 합니다."},
                        {"role": "user", "content": f"다음 패션 용어 또는 브랜드에 대해 알려주세요: {query}. 다음 JSON 형식으로만 응답해주세요(추가 텍스트 없이): {{\"definition\": \"정의\", \"examples\": [\"예시1\", \"예시2\"], \"brands\": [\"브랜드1\", \"브랜드2\"], \"related_terms\": [\"관련용어1\", \"관련용어2\"]}}"}
                    ],
                    response_format={"type": "json_object"}
                )
                return response.choices[0].message.content
            except Exception as e:
                st.error(f"OpenAI API 호출 중 오류 발생: {e}")
                return None

        # 검색 실행
        if search_query:
            if not st.session_state.openai_api_key:
                st.error("OpenAI API 키를 입력해주세요. 사이드바의 'API 키 설정'에서 입력할 수 있습니다.")
            else:
                with st.spinner("정보를 검색 중입니다..."):
                    try:
                        # 트렌드/용어 정보 가져오기
                        trend_info = get_fashion_trend_info(search_query)
                        if trend_info and "description" in trend_info:
                            # 설명 표시 ('에 대한 설명' 문구 제거)
                            st.markdown(f"### '{search_query}'")
                            st.write(trend_info["description"])
                            
                            # 구분선 추가
                            st.markdown("---")
                            
                            # 이미지 표시
                            st.markdown("### 관련 이미지")
                            # 이미지 검색 키워드 정제
                            image_url = get_image_url(search_query)
                            if image_url:
                                st.image(image_url, caption=f"{search_query} 관련 이미지", use_container_width=True)
                        else:
                            st.error("검색 결과를 가져오지 못했습니다. 다른 검색어로 시도해 보세요.")
                    except Exception as e:
                        st.error(f"검색 중 오류 발생: {e}")
                        st.error("잠시 후 다시 시도해 주세요.")

    elif st.session_state.page == "brands":
        st.markdown("### 패션 브랜드 알아보기")
        search_query = st.text_input("", placeholder="브랜드명을 입력하세요 (예: 구찌, 프라다, 나이키 등)", key="brand_search")
        
        if search_query:
            # API 키 확인
            if not st.session_state.openai_api_key:
                st.error("OpenAI API 키를 입력해주세요. 사이드바의 'API 키 설정'에서 입력할 수 있습니다.")
            else:
                with st.spinner("브랜드 정보를 검색 중입니다..."):
                    try:
                        # 브랜드 이름 정리
                        brand_name = search_query
                        
                        # 브랜드 정보 가져오기
                        import json
                        brand_info_str = get_fashion_term_info(brand_name)
                        if brand_info_str:
                            try:
                                brand_info = json.loads(brand_info_str)
                                
                                # 필수 키가 있는지 확인
                                required_keys = ["definition", "examples", "brands", "related_terms"]
                                for key in required_keys:
                                    if key not in brand_info:
                                        st.error(f"API 응답에 필요한 '{key}' 정보가 없습니다. 다시 시도해 주세요.")
                                        raise KeyError(f"Missing required key: {key}")
                                
                                # 이미지 URL 가져오기 - 브랜드 특화 검색어 사용
                                specific_query = f"{brand_name} brand logo fashion"
                                image_url = get_image_url(specific_query)
                                
                                # 브랜드 정보 표시
                                col1, col2 = st.columns([1, 1])
                                
                                with col1:
                                    st.markdown(f"<div class='card'><h2>{brand_name}</h2>", unsafe_allow_html=True)
                                    st.markdown(f"<p>{brand_info['definition']}</p></div>", unsafe_allow_html=True)
                                    
                                    st.markdown("<div class='card'><h3>대표 제품/스타일</h3>", unsafe_allow_html=True)
                                    for example in brand_info['examples']:
                                        st.markdown(f"- {example}")
                                    st.markdown("</div>", unsafe_allow_html=True)
                                    
                                    st.markdown("<div class='card'><h3>관련 용어</h3>", unsafe_allow_html=True)
                                    term_html = ""
                                    for term in brand_info['related_terms']:
                                        term_html += f"<span class='related-keyword'>{term}</span>"
                                    st.markdown(term_html, unsafe_allow_html=True)
                                    st.markdown("</div>", unsafe_allow_html=True)
                                
                                with col2:
                                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                                    st.image(image_url, caption=f"{brand_name} 이미지", use_container_width=True)
                                    st.markdown("</div>", unsafe_allow_html=True)
                            except json.JSONDecodeError as e:
                                st.error(f"JSON 파싱 오류: {e}")
                                st.error("API 응답이 올바른 JSON 형식이 아닙니다. 다시 시도해 주세요.")
                            except KeyError as e:
                                st.error(f"필수 데이터 누락: {e}")
                    
                    except Exception as e:
                        st.error(f"오류 발생: {e}")
                        st.error("브랜드 정보를 처리하는 중 문제가 발생했습니다. 다시 시도해 주세요.")

    elif st.session_state.page == "styling":
        st.markdown("### 스타일링 검색")
        st.markdown("<p class='styling-guide'>원하는 패션 스타일, 아이템, 색상 등을 검색하여 관련 이미지를 확인해보세요.</p>", unsafe_allow_html=True)
        
        style_query = st.text_input("", placeholder="검색어를 입력하세요 (예: 미니멀 스타일링, 블루 코트, 캐주얼 룩 등)", key="style_search")
        
        if style_query:
            with st.spinner("스타일링 이미지를 검색 중입니다..."):
                try:
                    # 스타일 검색 키워드는 get_multiple_images 함수 내에서 처리
                    images = get_multiple_images(style_query)
                    
                    if images:
                        st.markdown(f"### '{style_query}'")
                        
                        # 이미지를 3개씩 2행으로 표시
                        for i in range(0, len(images), 3):
                            cols = st.columns(3)
                            for j in range(3):
                                if i+j < len(images):
                                    with cols[j]:
                                        st.image(images[i+j], use_container_width=True)
                    
                        st.markdown("""
                        <div class='footer-tiny' style='text-align: center; margin-top: 20px;'>
                        이미지 제공: Unsplash
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("이미지를 찾을 수 없습니다. 다른 검색어로 시도해 보세요.")
                except Exception as e:
                    st.error(f"이미지 검색 중 오류 발생: {e}")
                    st.error("잠시 후 다시 시도해 주세요.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# 푸터 추가 (모든 탭에서 공통으로 표시)
st.markdown("---")
st.markdown("""
<div class="footer-tiny" style="text-align: center; margin-top: 20px;">
© 2025 FASHION TREND-SETTER. All rights reserved.
</div>
""", unsafe_allow_html=True)

# Unsplash API를 통한 이미지 검색 개선
def get_image_url(query):
    try:
        unsplash_access_key = st.session_state.unsplash_api_key
        if not unsplash_access_key:
            # API 키가 없는 경우 기본 이미지 반환
            st.warning("Unsplash API 키가 설정되지 않아 기본 이미지를 사용합니다.")
            return "https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93?w=600"
        
        # 패션 관련 키워드 추가하여 관련성 높은 이미지 검색
        # 검색 키워드 정제 (언어 감지 및 영문 처리)
        if any('\u3131' <= c <= '\u318F' or '\uAC00' <= c <= '\uD7A3' for c in query):  # 한글 감지
            # 패션 관련 검색 키워드 추가 (한글)
            search_queries = [
                f"{query} 패션",
                f"{query} 패션 스타일",
                f"{query} fashion look",
                f"{query} fashion style"
            ]
        else:
            # 패션 관련 검색 키워드 추가 (영문)
            search_queries = [
                f"{query} fashion",
                f"{query} fashion look",
                f"{query} fashion style",
                f"{query} clothing"
            ]
            
        # 이미지 결과 저장
        best_images = []
        
        # 여러 키워드로 검색하여 결과 합치기
        for search_query in search_queries:
            try:
                url = f"https://api.unsplash.com/search/photos?query={search_query}&client_id={unsplash_access_key}&per_page=5&orientation=landscape"
                response = requests.get(url)
                data = response.json()
                
                if 'results' in data and len(data['results']) > 0:
                    # 결과가 있으면 이미지 저장
                    for result in data['results']:
                        best_images.append(result['urls']['regular'])
            except Exception:
                continue
        
        # 결과가 있으면 첫 번째 이미지 반환
        if best_images:
            return best_images[0]
                    
        # 결과가 없으면 기본 검색 시도
        try:
            url = f"https://api.unsplash.com/search/photos?query=fashion style&client_id={unsplash_access_key}&per_page=5"
            response = requests.get(url)
            data = response.json()
            
            if 'results' in data and len(data['results']) > 0:
                return data['results'][0]['urls']['regular']
        except Exception:
            pass
        
        # 모든 시도 실패 시 기본 이미지 반환
        return "https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93?w=600"
    except Exception as e:
        st.error(f"이미지 검색 중 오류 발생: {e}")
        # 오류 발생 시 기본 이미지 반환
        return "https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93?w=600"

# 여러 이미지 가져오기 - 검색 정확도 개선
def get_multiple_images(query, count=6):
    try:
        unsplash_access_key = st.session_state.unsplash_api_key
        if not unsplash_access_key:
            # API 키가 없는 경우 기본 이미지 반환
            st.warning("Unsplash API 키가 설정되지 않아 기본 이미지를 사용합니다.")
            # 다양한 패션 기본 이미지들
            default_images = [
                "https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93",
                "https://images.unsplash.com/photo-1490481651871-ab68de25d43d",
                "https://images.unsplash.com/photo-1445205170230-053b83016050",
                "https://images.unsplash.com/photo-1479064555552-3ef4979f8908",
                "https://images.unsplash.com/photo-1485968579580-b6d095142e6e",
                "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f"
            ]
            # 필요한 수 만큼 기본 이미지 리스트 확장
            while len(default_images) < count:
                default_images += default_images[:count-len(default_images)]
            return default_images[:count]
        
        # 이미지 결과 저장
        all_images = []
        
        # 검색 키워드 정제 (언어 감지 및 영문 처리)
        if any('\u3131' <= c <= '\u318F' or '\uAC00' <= c <= '\uD7A3' for c in query):  # 한글 감지
            # 패션 관련 검색 키워드 추가 (한글)
            search_queries = [
                f"{query} 패션",
                f"{query} 스타일링",
                f"{query} 코디",
                f"{query} 패션 코디",
                f"{query} fashion look"
            ]
        else:
            # 패션 관련 검색 키워드 추가 (영문)
            search_queries = [
                f"{query} fashion",
                f"{query} style",
                f"{query} outfit",
                f"{query} look",
                f"{query} styling"
            ]
        
        # 여러 키워드로 검색하여 최대한 많은 이미지 확보
        for search_query in search_queries:
            try:
                url = f"https://api.unsplash.com/search/photos?query={search_query}&client_id={unsplash_access_key}&per_page={count}&orientation=portrait"
                response = requests.get(url)
                data = response.json()
                
                if 'results' in data and len(data['results']) > 0:
                    # 결과가 있는 경우 이미지 URL 리스트에 추가
                    for item in data['results']:
                        if item['urls']['regular'] not in all_images:
                            all_images.append(item['urls']['regular'])
            except Exception:
                continue
        
        # 결과가 충분하면 지정된 수만큼 반환
        if len(all_images) >= count:
            return all_images[:count]
        # 결과가 부족하면 기본 검색 추가
        elif all_images:
            # 결과가 있지만 부족한 경우, 기본 패션 검색으로 보충
            try:
                url = f"https://api.unsplash.com/search/photos?query=fashion style&client_id={unsplash_access_key}&per_page={count-len(all_images)}"
                response = requests.get(url)
                data = response.json()
                
                if 'results' in data and len(data['results']) > 0:
                    for item in data['results']:
                        if item['urls']['regular'] not in all_images:
                            all_images.append(item['urls']['regular'])
            except Exception:
                pass
            
            # 필요한 수 만큼 반복
            while len(all_images) < count:
                all_images += all_images[:count-len(all_images)]
            return all_images[:count]
        else:
            # 결과가 없는 경우 기본 패션 이미지 리스트 반환
            default_images = [
                "https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93",
                "https://images.unsplash.com/photo-1490481651871-ab68de25d43d",
                "https://images.unsplash.com/photo-1445205170230-053b83016050",
                "https://images.unsplash.com/photo-1479064555552-3ef4979f8908",
                "https://images.unsplash.com/photo-1485968579580-b6d095142e6e",
                "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f"
            ]
            # 필요한 수 만큼 기본 이미지 리스트 확장
            while len(default_images) < count:
                default_images += default_images[:count-len(default_images)]
            return default_images[:count]
    except Exception as e:
        st.error(f"이미지 검색 중 오류 발생: {e}")
        # 오류 발생 시 기본 이미지 반환
        default_images = [
            "https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93",
            "https://images.unsplash.com/photo-1490481651871-ab68de25d43d",
            "https://images.unsplash.com/photo-1445205170230-053b83016050",
            "https://images.unsplash.com/photo-1479064555552-3ef4979f8908",
            "https://images.unsplash.com/photo-1485968579580-b6d095142e6e",
            "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f"
        ]
        # 필요한 수 만큼 기본 이미지 리스트 확장
        while len(default_images) < count:
            default_images += default_images[:count-len(default_images)]
        return default_images[:count] 