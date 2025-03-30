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
    
    # 패션 트렌드/용어 선택 (수정)
    st.markdown('<div class="all-things-fashion">All Things Fashion</div>', unsafe_allow_html=True)
    search_option = st.radio(
        "",
        ["Trend & Information", "Brands"]
    )
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

# 타이틀
st.title("FASHION TREND-SETTER")
st.markdown("### 패션 트렌드/용어")

# 검색 기능
if search_option == "Trend & Information":
    search_query = st.text_input("", placeholder="(예: Y2K 패션, 아방가르드, 하이엔드 등)")
    
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
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 패션 전문가입니다. 패션 트렌드, 용어, 브랜드에 대한 정보를 상세하게 제공해주세요. 응답은 반드시 유효한 JSON 형식이어야 합니다."},
                    {"role": "user", "content": f"다음 패션 트렌드에 대해 알려주세요: {query}. 다음 JSON 형식으로만 응답해주세요(추가 텍스트 없이): {{\"description\": \"상세 설명\", \"styling_tips\": [\"팁1\", \"팁2\", \"팁3\"], \"related_keywords\": [\"연관키워드1\", \"연관키워드2\", \"연관키워드3\"]}}"}
                ],
                response_format={"type": "json_object"}
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
        # API 키 확인
        if not st.session_state.openai_api_key:
            st.error("OpenAI API 키를 입력해주세요. 사이드바의 'API 키 설정'에서 입력할 수 있습니다.")
        else:
            with st.spinner("정보를 검색 중입니다..."):
                try:
                    # 브랜드 정보 추가
                    search_text = search_query
                    if search_type == "패션 트렌드":
                        # 패션 트렌드 정보 가져오기
                        import json
                        trend_info_str = get_fashion_trend_info(search_text)
                        if trend_info_str:
                            try:
                                trend_info = json.loads(trend_info_str)
                                
                                # 필수 키가 있는지 확인
                                required_keys = ["description", "styling_tips", "related_keywords"]
                                for key in required_keys:
                                    if key not in trend_info:
                                        st.error(f"API 응답에 필요한 '{key}' 정보가 없습니다. 다시 시도해 주세요.")
                                        raise KeyError(f"Missing required key: {key}")
                                
                                # 이미지 URL 가져오기
                                image_url = get_image_url(search_text + " fashion")
                                
                                # 트렌드 정보 표시
                                col1, col2 = st.columns([1, 1])
                                
                                with col1:
                                    st.markdown(f"<div class='card'><h2>{search_text}</h2>", unsafe_allow_html=True)
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
                                    st.image(image_url, caption=f"{search_text} 이미지", use_container_width=True)
                                    st.markdown("</div>", unsafe_allow_html=True)
                            except json.JSONDecodeError as e:
                                st.error(f"JSON 파싱 오류: {e}")
                                st.error("API 응답이 올바른 JSON 형식이 아닙니다. 다시 시도해 주세요.")
                            except KeyError as e:
                                st.error(f"필수 데이터 누락: {e}")
                
                    else:  # 패션 용어
                        # 패션 용어 정보 가져오기
                        import json
                        term_info_str = get_fashion_term_info(search_text)
                        if term_info_str:
                            try:
                                term_info = json.loads(term_info_str)
                                
                                # 필수 키가 있는지 확인
                                required_keys = ["definition", "examples", "brands", "related_terms"]
                                for key in required_keys:
                                    if key not in term_info:
                                        st.error(f"API 응답에 필요한 '{key}' 정보가 없습니다. 다시 시도해 주세요.")
                                        raise KeyError(f"Missing required key: {key}")
                                
                                # 이미지 URL 가져오기
                                image_url = get_image_url(search_text + " fashion")
                                
                                # 용어 정보 표시
                                col1, col2 = st.columns([1, 1])
                                
                                with col1:
                                    st.markdown(f"<div class='card'><h2>{search_text}</h2>", unsafe_allow_html=True)
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
                                    st.image(image_url, caption=f"{search_text} 이미지", use_container_width=True)
                                    st.markdown("</div>", unsafe_allow_html=True)
                            except json.JSONDecodeError as e:
                                st.error(f"JSON 파싱 오류: {e}")
                                st.error("API 응답이 올바른 JSON 형식이 아닙니다. 다시 시도해 주세요.")
                            except KeyError as e:
                                st.error(f"필수 데이터 누락: {e}")
                
                except Exception as e:
                    st.error(f"오류 발생: {e}")
                    st.error("검색 결과를 처리하는 중 문제가 발생했습니다. 다시 시도해 주세요.")
else:  # 브랜드 검색
    # 패션 브랜드 정보 문구와 드롭다운 대신 검색창 추가
    search_query = st.text_input("", placeholder="브랜드명을 입력하세요 (예: 구찌, 프라다, 나이키 등)")
    
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
                            
                            # 이미지 URL 가져오기
                            image_url = get_image_url(brand_name + " fashion brand")
                            
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