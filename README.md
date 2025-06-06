# 패션 트렌드 세터

패션 트렌드와 용어를 검색하고 학습할 수 있는 스트림릿 애플리케이션입니다.

## 기능

- 패션 트렌드 검색: 최신 패션 트렌드에 대한 정보, 스타일링 팁, 연관 키워드 제공
- 패션 용어/브랜드 검색: 패션 용어와 브랜드에 대한 정의, 예시, 관련 브랜드, 관련 용어 제공
- 시각적 정보: 검색어와 관련된 이미지 제공
- API 키 설정: 사이드바에서 OpenAI API 키와 Unsplash API 키를 웹 인터페이스에서 직접 입력 가능

## 설치 및 실행 방법

1. 저장소 클론
```
git clone https://github.com/사용자명/패션-트렌드-세터.git
cd 패션-트렌드-세터
```

2. 의존성 설치
```
pip install -r requirements.txt
```

3. 애플리케이션 실행
```
streamlit run app.py
```

## API 키 설정 방법

1. [OpenAI API 키](https://platform.openai.com/account/api-keys)를 발급받으세요.
2. (선택사항) [Unsplash API 키](https://unsplash.com/developers)를 발급받으세요.
3. API 키는 두 가지 방법으로 설정할 수 있습니다:
   - `.env` 파일에 API 키 설정:
     ```
     OPENAI_API_KEY=여기에_OPENAI_API_키_입력
     UNSPLASH_ACCESS_KEY=여기에_UNSPLASH_API_키_입력
     ```
   - 웹 인터페이스에서 직접 설정: 애플리케이션 사이드바의 'API 설정' 섹션에서 API 키를 입력하고 저장할 수 있습니다.

## 기술 스택

- Streamlit: 웹 인터페이스
- OpenAI API (v1.69.0): 패션 정보 생성
- Unsplash API: 이미지 검색

## 주의사항

- 이 애플리케이션은 OpenAI API v1.69.0 버전을 사용합니다.
- 최신 버전의 OpenAI 라이브러리가 필요합니다.
- 최신 버전으로 업데이트하려면 다음 명령어를 실행하세요:
  ```
  pip install openai --upgrade
  ```

## 스트림릿 클라우드 배포

1. [Streamlit Cloud](https://streamlit.io/cloud)에 가입하세요.
2. 깃허브 저장소를 연결하세요.
3. Secrets 섹션에서 `.env` 파일에 있는 환경 변수를 설정하세요.
4. 배포 버튼을 클릭하여 애플리케이션을 배포하세요.

## 스크린샷

![앱 스크린샷](https://via.placeholder.com/800x400?text=패션+트렌드+세터+스크린샷)

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 