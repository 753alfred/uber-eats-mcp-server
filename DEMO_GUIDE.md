# 🤖 Uber Eats MCP Server 시연 가이드

## 📋 프로젝트 개요

이 프로젝트는 **Model Context Protocol (MCP)**를 사용하여 Claude Desktop에서 Uber Eats 웹사이트를 자동으로 제어할 수 있는 서버입니다.

### 🎯 주요 기능
- 🔍 **음식점/음식 검색**: 자연어로 음식을 검색
- 🛒 **자동 주문**: 원하는 음식을 자동으로 주문
- 🌐 **브라우저 자동화**: Playwright 기반 웹 제어
- 📸 **스크린샷 캡처**: 작업 과정 시각적 기록

## 🛠️ 기술 스택

- **FastMCP**: MCP 서버 프레임워크
- **Playwright**: 브라우저 자동화
- **Anthropic Claude**: LLM 엔진
- **Python 3.10+**: 메인 개발 언어

## 🚀 설치 및 설정

### 1. 가상환경 설정
```bash
python3.10 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate     # Windows
```

### 2. 의존성 설치
```bash
pip install --upgrade pip
pip install langchain-anthropic langchain-openai python-dotenv playwright fastmcp
playwright install chromium --with-deps
```

### 3. 환경변수 설정
`.env` 파일 생성:
```env
ANTHROPIC_API_KEY=your-api-key-here
OPENAI_API_KEY=your-openai-key-here
```

## 📱 Claude Desktop 연결

Claude Desktop의 설정 파일에 다음을 추가:

### macOS
경로: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows
경로: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "uber_eats": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/Users/a753/git_macbook/uber-eats-mcp-server",
      "env": {
        "ANTHROPIC_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## 🎮 시연 시나리오

### 시나리오 1: 음식 검색
```
Claude에게 말하기: "pizza 검색해줘"
```
- ✅ Uber Eats 사이트 접속
- ✅ 검색창에 "pizza" 입력
- ✅ 검색 결과 상위 3개 추출
- ✅ 이름, URL, 가격 정보 제공

### 시나리오 2: 자동 주문
```
Claude에게 말하기: "이 피자를 주문해줘: [URL]"
```
- ✅ 지정된 메뉴 페이지로 이동
- ✅ "장바구니에 추가" 클릭
- ✅ 결제 페이지로 이동
- ✅ 주문 완료 처리

## 🧪 로컬 테스트

브라우저 자동화 기능만 별도로 테스트:
```bash
python test_browser.py
```

### 예상 출력:
```
🤖 Uber Eats MCP 브라우저 자동화 데모
==================================================
🚀 브라우저 시작 중...
📍 Step 1 completed
🌐 https://www.ubereats.com/로 이동 중...
✅ 페이지 로딩 완료
📍 Step 2 completed
🔍 'pizza' 검색 중...
✅ 검색창 발견: input[type="text"]
✅ 검색 완료
📄 페이지 내용 추출 중...
📸 스크린샷 저장: screenshot.png
✅ 작업 완료!
```

## 🛡️ 문제 해결

### 일반적인 문제들

#### 1. Playwright 브라우저 미설치
```bash
playwright install chromium
```

#### 2. Python 버전 호환성
- Python 3.10+ 필수
- 3.8/3.9는 지원하지 않음

#### 3. 타임아웃 오류
- 네트워크 상태 확인
- VPN 사용 시 해제 후 재시도

#### 4. API 키 오류
- `.env` 파일의 API 키 확인
- Claude Desktop 설정의 환경변수 확인

## 📁 프로젝트 구조

```
uber-eats-mcp-server/
├── server.py              # MCP 서버 메인 파일
├── browser.py              # 브라우저 자동화 로직
├── test_browser.py         # 로컬 테스트 스크립트
├── requirements.txt        # Python 의존성
├── .env                    # 환경변수 (gitignore)
├── venv/                   # 가상환경
├── screenshot.png          # 자동 생성 스크린샷
└── DEMO_GUIDE.md          # 이 파일
```

## 🎥 시연 체크리스트

### 사전 준비
- [ ] 가상환경 활성화
- [ ] 모든 의존성 설치 완료
- [ ] API 키 설정 완료
- [ ] Claude Desktop 설정 완료

### 시연 순서
1. [ ] **MCP 서버 시작**: `python server.py`
2. [ ] **Claude Desktop 열기**
3. [ ] **연결 확인**: MCP 서버 상태 체크
4. [ ] **음식 검색 시연**: "pizza 검색해줘"
5. [ ] **결과 확인**: 검색 결과 3개 표시
6. [ ] **스크린샷 확인**: `screenshot.png` 파일 확인

### 예상 시연 시간
- 설정 및 준비: 3분
- 실제 시연: 5분
- 질답 및 설명: 5분
- **총 소요시간: 약 13분**

## 🔗 유용한 링크

- [FastMCP 공식 문서](https://gofastmcp.com/)
- [Model Context Protocol 설명](https://modelcontextprotocol.io/)
- [Playwright 문서](https://playwright.dev/python/)
- [Claude Desktop 설정 가이드](https://docs.anthropic.com/claude/docs/desktop-app)

## 🤝 기여하기

버그 발견이나 개선사항이 있으시면 이슈를 등록해주세요!

## 📄 라이선스

MIT License

---

**⚡ 시연 성공을 위한 팁:**
1. 안정적인 인터넷 연결 필수
2. Uber Eats 사이트 접근 가능 확인
3. 브라우저 창이 보이도록 headless=False 설정
4. 각 단계별 로그 메시지 주의 깊게 관찰 