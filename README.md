# 카카오톡 자동응답봇 - originally made by SerenityS / modified by rackis / 급식, 학사일정, 학반별 시간표, 날씨, 공지
> 이 소스는 MIT라이선스 하에 자유롭게 이용할 수 있습니다.

### 개발 참고 사이트
* https://github.com/plusfriend/auto_reply
* http://throughkim.kr/2016/07/11/kakao-haksik/
* http://humit.tistory.com/248
* http://sigool.tistory.com/4
* https://github.com/SerenityS/kakaobot_hyoammeal -- 오리지널 깃
* https://github.com/rackis/cgshmeal -- 이전버전
* 기타 많은 사이트들..

### 개발 환경
* Raspberry pi 3 model b
* PyCharm
* Git

### 사용 언어
* Django
* Python + venv

### 필요 모듈
* beautifulsoup4
* urllib
* lxml
* dateutil

# 설치법 - 라즈베리파이 이용

### 1. VNC활성화
라즈베리파이 Configuration에서 인터페이스 탭의 VNC를 allow 하면 작업표시줄에 아이콘이 생긴다.
VNC프로르램을 아이콘을 눌러 실행하고 옵션을 눌러 접속 비밀번호를 설정한다.
전원을 끈 후 리더기로 sd카드를 컴퓨터에 연결하여 boot/config.txt를 수정한다.
<pre># uncomment to force a console size. By default it will be display's size minus
# overscan.
#framebuffer_width=1280
#framebuffer_height=720</pre>
에서 framebuffer앞의 #을 지우고 뒤에 해상도 값을 원하는 값으로 변경한다.
그러고 다시 라즈베리파이를 부팅한다.

### 2. VNC로 접속
데스크탑에서 VNC Viewer을 다운받아 설치한 후
https://www.realvnc.com/en/connect/download/viewer/
라즈베리파이의 ip로 접속한다.

### 3. 라즈베리파이에 한글 설치
<code>sudo apt-get install fonts-unfonts-core ibus ibus-hangul -y</code>

설치가 완료되면 라즈베리파이 Configuration에서 로컬라이제이션 탭에서 로케일, 시간, 키보드를 변경한다.
<pre>언어 ko (korean)
국가 KR (South Korea) - (UTF-8)
지역 Asia
위치 Seoul
키보드 국가 Korea, Republic of [101/104 key]</pre>

설정이 완료되면 재부팅 한다.

### 4. 기초 패키지 설치
<pre>업데이트 실시 - 자율 실시
   sudo apt-get update
   sudo apt-get upgrade</pre>

<pre>파이썬 패키지 설치 - 라즈베리파이의 경우 미리 설치되어 있다.
   <code>sudo apt-get install python3 python3-pip python3-venv</code></pre>
   
<pre>DB Browser for SQLite 패키지 설치
   <code>sudo apt-get install sqlitebrowser</code></pre>
   
<pre>깃 클론
   <code>git clone https://github.com/rackis/kakaobot_responder /home/pi/Desktop/KAKAO</code> --- 깃 클론 위치(KAKAO)는 변경하여도 상관없다.
   <code>cd /home/pi/Desktop/KAKAO</code> --- 깃 위치로 이동</pre>

<pre>파이선 가상화 실행
   <code>python3 -m venv myvenv</code> --- 가상환경 구축, 설치 처음만 실행
   <code>source myvenv/bin/activate</code> --- 가상환경 실행</pre>

<pre>가상화된 위치에 필요한 모듈 설치 (lxml의 경우 오래 걸리더라도 인내심을 가지고 기다린다.)
   <code>pip install Django beautifulsoup4 python-dateutil
	pip install lxml
	CFLAGS="-O0"  pip install lxml      -   오래걸려도 기다리기</code></pre>

*아래는 lxml 설치 실패시 적용해보기  --  http://lxml.de/installation.html 참고
<code>sudo apt-get install python3-lxml -y
sudo apt-get install libxml2-dev libxslt-dev python-dev -y
pip install lxml==3.6.0</code>

### 5. 학교 코드 수정
타학교에서 사용하기 위해선 학교 코드 수정이 필요하다.

element/crawl.py를 열어보자.
```python
# 타학교에서 이용시 수정
regionCode = 'gne.go.kr'
schulCode = 'S100000492'
```
라는 코드를 발견할 수 있다.
여기서 regionCode는 각 시도교육청의 주소이며, schulCode는 [링크](http://weezzle.tistory.com/559) 를 참조하도록 하자.

### 6. 급식 정보 받아오기
* 아래 코드 첫 입력으로 급식 정보 파일 생성
<code>python3 element/crawl.py</code>

***crontab을 통한 crawl.py의 주기적 실행
*터미널에에 아래 명령어를 실행하고, 아래 두 줄을 한꺼번에 복사하여 붙여넣기.
```
crontab -e
```
```
# 매주 일요일 0시 0분에 crawl.py 실행
0 0 * * 7 cd ~/Desktop/KAKAO/element && /usr/bin/python3 ~/Desktop/KAKAO/element/crawl.py
```

시간표, 학사일정 정보는 element/database/responder.db 에 존재하므로 수정후 사용하도록 함.
'element/database/maketable.sql' 이 SQL파일을 데이터베이스로 가져오기 하여 새로운 테이블 생성.

### 7. 카카오톡 플러스 친구와 연동
타게시물들을 참조하도록 하자.

### 8. 마이그레이션, 서버 실행
첫 마이그레이션
<code>python3 manage.py migrate</code>
서버 실행
<code>python3 manage.py runserver host-ip:8000</code>

아래와 같이 뜬다면 정상적으로 실행된 것이다. (host-ip는 장치의 IP주소를 입력하는 곳이다.)
<pre><code>Performing system checks...
System check identified no issues (0 silenced).
July 19, 2017 - 19:18:53
Django version 1.11.3, using settings 'kakaobot.settings'
Starting development server at http://host-ip:8000/
Quit the server with CONTROL-C.</code></pre>
여의치 않다면 127.0.0.1 루프백으로 두고 실행해서 테스트해도 된다.

### 9. 동작 확인
카카오톡 플러스친구 자동등답 API에선 http://host-ip:8000/keyboard/에 대한 반응을 필수로 요구한다.

터미널에 <code>curl -XGET 'http://host-ip:8000/keyboard/'</code>를 입력해보자.
<pre><code>serenitys@serenitys-X34:~$ curl -XGET 'http://host-ip:8000/keyboard/'
{"type": "buttons", "buttons": ["\uc870\uc2dd", "\uc911\uc2dd", "\uc11d\uc2dd", "\ub0b4\uc77c\uc758 \uc870\uc2dd", "\ub0b4\uc77c\uc758 \uc911\uc2dd", "\ub0b4\uc77c\uc758 \uc11d\uc2dd"]}</code></pre>
정상적으로 작동한다면 이와 같은 정보가 오는것을 확인할 수 있다.

또한 keyboard에서 선택한 메뉴의 응답으로 message를 반환하는데 POST형태로 서버로 요구사항을 전달하고  GET으로 정보를 받는다.
 
터미널에 
```
curl -XPOST 'http://host-ip:8000/message' -d '{ "user_key": "encryptedUserKey", "type" : "text", "content": "중식"}'
```
  를 입력해보자.
  
  <pre>serenitys@serenitys-X34:~$ curl -XPOST (생략)
{"keyboard": {"type": "buttons", "buttons": ["\uc870\uc2dd", "\uc911\uc2dd", "\uc11d\uc2dd", "\ub0b4\uc77c\uc758 \uc870\uc2dd", "\ub0b4\uc77c\uc758 \uc911\uc2dd", "\ub0b4\uc77c\uc758 \uc11d\uc2dd"]}, "message": {"text": "07\uc6d4 19\uc77c \uc218\uc694\uc77c \uc911\uc2dd \uba54\ub274\uc785\ub2c8\ub2e4. \n \n\ub098\ubb3c\ube44\ube54\ubc25/\uc57d\uace0\ucd94\uc7a5\n\uac10\uc790\ub41c\uc7a5\uad6d\n\uc18c\uc13</pre>
와 같이 반환됨을 확인함으로서 정상 작동함을 알 수 있다.

## 작동 화면
