import streamlit as st
import openai
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="패션 트렌드 세터",
    page_icon="👗",
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
</style>
""", unsafe_allow_html=True)

# 타이틀
st.title("👗 패션 트렌드 세터")
st.markdown("### 최신 패션 트렌드와 용어를 검색하고 학습하세요")

# 사이드바
with st.sidebar:
    st.header("검색 옵션")
    search_type = st.radio(
        "검색 유형 선택",
        ["패션 트렌드", "패션 용어/브랜드"]
    )
    
    # API 키 입력 섹션
    st.header("API 설정")
    with st.expander("API 키 설정"):
        openai_key = st.text_input("OpenAI API 키", value=st.session_state.openai_api_key, type="password")
        unsplash_key = st.text_input("Unsplash API 키 (선택사항)", value=st.session_state.unsplash_api_key, type="password")
        
        if st.button("API 키 저장"):
            st.session_state.openai_api_key = openai_key
            st.session_state.unsplash_api_key = unsplash_key
            st.success("API 키가 저장되었습니다.")

# 검색 기능
search_query = st.text_input("검색어 입력 (예: Y2K 패션, 아방가르드, 하이엔드 등)", placeholder="여기에 입력하세요...")

# Unsplash API를 통한 이미지 검색 (무료 API 사용)
def get_image_url(query):
    try:
        unsplash_access_key = st.session_state.unsplash_api_key
        if not unsplash_access_key:
            # API 키가 없는 경우 기본 이미지 반환
            st.warning("Unsplash API 키가 설정되지 않아 기본 이미지를 사용합니다.")
            return "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=600"
        
        url = f"https://api.unsplash.com/search/photos?query={query}&client_id={unsplash_access_key}"
        response = requests.get(url)
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0]['urls']['regular']
        else:
            # 검색 결과가 없는 경우 기본 이미지 반환
            return "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=600"
    except Exception as e:
        st.error(f"이미지 검색 중 오류 발생: {e}")
        # 오류 발생 시 기본 이미지 반환
        return "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=600"

# GPT를 통한 트렌드 정보 검색
def get_fashion_trend_info(query):
    try:
        # API 키 확인
        if not st.session_state.openai_api_key:
            st.error("OpenAI API 키를 입력해주세요. 사이드바의 'API 설정'에서 입력할 수 있습니다.")
            return None
            
        # OpenAI 클라이언트 초기화
        client = OpenAI(api_key=st.session_state.openai_api_key)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 패션 전문가입니다. 패션 트렌드, 용어, 브랜드에 대한 정보를 상세하게 제공해주세요."},
                {"role": "user", "content": f"다음 패션 트렌드에 대해 알려주세요: {query}. 다음 형식으로 JSON 응답을 제공해주세요: {{\"description\": \"상세 설명\", \"styling_tips\": [\"팁1\", \"팁2\", \"팁3\"], \"related_keywords\": [\"연관키워드1\", \"연관키워드2\", \"연관키워드3\"]}}"}
            ]
        )
        return response.choices[0].message.content
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
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 패션 전문가입니다. 패션 용어와 브랜드에 대한 상세한 정보를 제공해주세요."},
                {"role": "user", "content": f"다음 패션 용어 또는 브랜드에 대해 알려주세요: {query}. 다음 형식으로 JSON 응답을 제공해주세요: {{\"definition\": \"정의\", \"examples\": [\"예시1\", \"예시2\"], \"brands\": [\"브랜드1\", \"브랜드2\"], \"related_terms\": [\"관련용어1\", \"관련용어2\"]}}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"OpenAI API 호출 중 오류 발생: {e}")
        return None

# 검색 실행
if search_query:
    # API 키 확인
    if not st.session_state.openai_api_key:
        st.error("OpenAI API 키를 입력해주세요. 사이드바의 'API 설정'에서 입력할 수 있습니다.")
    else:
        with st.spinner("정보를 검색 중입니다..."):
            try:
                if search_type == "패션 트렌드":
                    # 패션 트렌드 정보 가져오기
                    import json
                    trend_info_str = get_fashion_trend_info(search_query)
                    if trend_info_str:
                        trend_info = json.loads(trend_info_str)
                        
                        # 이미지 URL 가져오기
                        image_url = get_image_url(search_query + " fashion")
                        
                        # 트렌드 정보 표시
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            st.markdown(f"<div class='card'><h2>{search_query}</h2>", unsafe_allow_html=True)
                            st.markdown(f"<p>{trend_info['description']}</p></div>", unsafe_allow_html=True)
                            
                            st.markdown("<div class='card'><h3>스타일링 팁</h3>", unsafe_allow_html=True)
                            for tip in trend_info['styling_tips']:
                                st.markdown(f"- {tip}")
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            st.markdown("<div class='card'><h3>연관 키워드</h3>", unsafe_allow_html=True)
                            keyword_html = ""
                            for keyword in trend_info['related_keywords']:
                                keyword_html += f"<span class='related-keyword'>{keyword}</span>"
                            st.markdown(keyword_html, unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown("<div class='card'>", unsafe_allow_html=True)
                            st.image(image_url, caption=f"{search_query} 이미지", use_column_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                
                else:  # 패션 용어/브랜드
                    # 패션 용어 정보 가져오기
                    import json
                    term_info_str = get_fashion_term_info(search_query)
                    if term_info_str:
                        term_info = json.loads(term_info_str)
                        
                        # 이미지 URL 가져오기
                        image_url = get_image_url(search_query + " fashion")
                        
                        # 용어 정보 표시
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            st.markdown(f"<div class='card'><h2>{search_query}</h2>", unsafe_allow_html=True)
                            st.markdown(f"<p>{term_info['definition']}</p></div>", unsafe_allow_html=True)
                            
                            st.markdown("<div class='card'><h3>예시</h3>", unsafe_allow_html=True)
                            for example in term_info['examples']:
                                st.markdown(f"- {example}")
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            st.markdown("<div class='card'><h3>관련 브랜드</h3>", unsafe_allow_html=True)
                            for brand in term_info['brands']:
                                st.markdown(f"- {brand}")
                            st.markdown("</div>", unsafe_allow_html=True)
                            
                            st.markdown("<div class='card'><h3>관련 용어</h3>", unsafe_allow_html=True)
                            term_html = ""
                            for term in term_info['related_terms']:
                                term_html += f"<span class='related-keyword'>{term}</span>"
                            st.markdown(term_html, unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown("<div class='card'>", unsafe_allow_html=True)
                            st.image(image_url, caption=f"{search_query} 이미지", use_column_width=True)
                            st.markdown("</div>", unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"오류 발생: {e}")
                st.error("검색 결과를 처리하는 중 문제가 발생했습니다. 다시 시도해 주세요.")

# 앱 정보 (하단)
st.markdown("<div class='footer-container'></div>", unsafe_allow_html=True)
st.markdown("<div class='footer-small'>### 패션 트렌드 세터 앱 정보</div>", unsafe_allow_html=True)
st.markdown("<div class='footer-tiny'>이 앱은 OpenAI API를 사용하여 패션 트렌드와 용어에 대한 정보를 제공합니다.<br>트렌드 이미지는 Unsplash API를 통해 제공됩니다.</div>", unsafe_allow_html=True) 