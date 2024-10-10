# SA 문서
## 프로젝트 기획서
  - 팀 소개: Living Ease는 편안한 생활을 위한 다양한 솔루션을 제공하는 팀입니다. 우리는 반려동물과 함께하는 삶이 더욱 풍요롭고 행복해질 수 있도록 돕고자 합니다. 현대 사회에서 반려동물은 가족의 일원으로 자리 잡고 있으며, 각자의 라이프스타일과 성격에 맞는 반려동물을 선택하는 것은 매우 중요합니다. 이를 위해, Living Ease는 성숙한 반려동물 문화를 조성하기 위해 최적의 반려동물을 매칭할 수 있는 솔루션을 개발하고 있습니다. 우리의 목표는 사람과 반려동물이 함께 조화롭게 살아갈 수 있는 환경을 조성하는 것입니다.
  
  <br/>

  - 프로젝트 개요: 우리 프로젝트는 예비 견주와 초보 견주를 위한 맞춤형 서비스를 제공합니다. 반려견을 처음 맞이하는 분들이나 준비 중인 분들이 반려견과의 생활을 보다 즐겁고 원활하게 시작할 수 있도록 돕고자 합니다. 각 개인의 필요와 상황에 맞춘 정보를 제공받아, 반려견 매칭 서비스, 반려견의 건강 관리 및 병원추천 서비스, 커뮤니티를 통한 견주 산책메이트 탐색 등 다양한 지원을 통해 행복한 반려 생활을 지원합니다.

  <br/>

## 개발 기간, 일정(주 단위)
   24.09.25 ~ 24.10.23

  <br/>

## 핵심 기능
  AI를 통한 반려동물 매칭
  추천 받은 반려동물에 대한 입양소 정보 제공
  커뮤니티 기능을 통하여 유저간 정보 공유

## 기능 상세
  - 유저
    - 로그인
    - 로그아웃
    - 프로필 조회
    - 프로필 수정
    - 회원 가입
    - 회원 탈퇴

  - 반려동물
    - 질문 리스트 조회
    - 유저 맞춤형 반려동물(반려견) 추천 서비스(LLM 기반)
    - 입양 경로 추천 서비스(유기견 보호 센터, 공공데이터 활용)

  - 커뮤니티
    - 커뮤니티글 등록
    - 커뮤니티글 수정
    - 커뮤니티글 삭제
    - 커뮤니티글 목록 조회
    - 커뮤니티글 상세 조회
  
  - 고객센터
    - 문의 사항 등록
    - 문의 사항 수정
    - 문의 사항 삭제
    - 문의 사항 목록 조회
    - 문의 사항 상세 조회

  - 공지사항
    - 공지사항 전체 목록 조회
    - 공지사항 상세 조회
    - 공지사항 우선 순위

  - 댓글
    - 커뮤니티 댓글 등록
    - 커뮤니티 댓글 수정
    - 커뮤니티 댓글 삭제

  - 검색
   - 아이디 검색
   - 제목 검색
   - 내용 검색

  - 위치서비스(예정)
    - 동물병원 추천 서비스
    - 산책로 추천 서비스

  - 견종 백과(예정)
   - 상세 조회
   - 전체 목록 조회
   - 찜하기

  - 애견 수첩(예정)
   - 반려견 정보 등록
   - 반려견 정보 수정
   - 반려견 정보 삭제
   - 반려견 정보 조회

  <br/>

## 역할 분담
  - 유저 : 정순겸(09.25 ~ 09.27)
   - 유저 로그인 username -> email 수정(10.03~10.07)
  - 게시판 : 정순겸(09.30~10.03)
  - 반려동물 : 서영환(09.25)
    - 반려동물 정보 업데이트:
    - 질문 내역 리스트 등록:
    - 공공데이터 연동:
  - 사이트 전체적인 디자인 & 퍼블리싱: 김민주(09.25~ )
  - 사이트 프론트앤드: 이승주(09.25 ~)

  <br/>

## 개발 환경
    Python 3.10, Django 4.2, React 18.3.1

  <br/>

## 와이어프레임
  - ...


  <br/>

## ERD
  - ...



## API 문서
  - ...