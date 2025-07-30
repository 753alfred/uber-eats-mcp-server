# 🎯 Claude Desktop MCP 서버 연결 가이드

## 🌟 원작자 스타일 시연 방법!

Claude Desktop (PC 버전)에서 자연어로 "피자 검색해줘"라고 말하면 자동으로 브라우저가 열려서 Uber Eats에서 검색하는 마법같은 시연을 해보겠습니다!

## 🚀 1단계: MCP 서버 실행 확인

```bash
# 현재 디렉토리에서 서버 실행 (이미 실행 중)
source venv/bin/activate
python server.py
```

서버가 실행되면 다음과 같은 출력이 나타납니다:
```
🚀 FastMCP 서버가 시작되었습니다!
📊 사용 가능한 도구들:
  - find_menu_options: Uber Eats 음식 검색
  - get_search_results: 검색 결과 조회
```

## 🔌 2단계: Claude Desktop 설정

### macOS 설정 경로:
```bash
# Claude Desktop 설정 디렉토리로 이동
~/Library/Application\ Support/Claude/config.json
```

### Windows 설정 경로:
```
%APPDATA%\Claude\config.json
```

### 설정 파일 내용:
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

## 🎬 3단계: Claude Desktop에서 시연

### 📱 Claude Desktop 재시작
1. Claude Desktop 완전 종료
2. 다시 실행
3. 설정이 올바르면 MCP 서버 연결 표시 확인

### 💬 자연어 명령 예시

**기본 검색:**
```
"Uber Eats에서 피자 메뉴를 검색해줘"
"치킨 버거를 찾아줘"
"한식당을 찾아서 메뉴를 보여줘"
```

**상세 검색:**
```
"Uber Eats에서 비건 피자를 찾아서 
상위 3개 메뉴의 이름, 가격, URL을 알려줘"
```

**검색 결과 조회:**
```
"방금 검색한 결과를 보여줘"
"검색 ID [request_id]의 결과를 가져와줘"
```

## 🎯 4단계: 실시간 시연 시나리오

### **시나리오 A: 기본 음식 검색**
```
👤 사용자: "피자를 검색해줘"
🤖 Claude: "네, Uber Eats에서 피자를 검색하겠습니다..."
🌐 브라우저: 자동으로 열리면서 Uber Eats 접속 → 피자 검색
📊 결과: 2분 후 상위 3개 피자 메뉴 정보 반환
```

### **시나리오 B: 특정 음식점 검색**
```
👤 사용자: "맥도날드에서 빅맥 세트 가격을 알려줘"
🤖 Claude: "맥도날드 메뉴를 검색하고 빅맥 세트를 찾아보겠습니다..."
🌐 브라우저: 맥도날드 → 빅맥 검색 → 가격 추출
📊 결과: 빅맥 세트 정보 및 가격 반환
```

## ⚡ 5단계: 고급 기능 활용

### **멀티 검색**
```bash
# 여러 음식을 동시에 검색
"피자, 치킨, 버거를 모두 검색해서 비교해줘"
```

### **가격 비교**
```bash
# 같은 음식의 다른 레스토랑 비교
"피자를 3개 다른 레스토랑에서 찾아서 가격 비교해줘"
```

## 🛠️ 문제 해결

### 🔧 연결 실패 시:
```bash
# 1. 서버 재시작
pkill -f server.py
python server.py

# 2. 포트 확인
lsof -i :8000

# 3. 환경변수 확인
echo $ANTHROPIC_API_KEY
```

### 🔧 브라우저 문제 시:
```bash
# Playwright 재설치
playwright install chromium --with-deps
```

## 🎊 시연 체크리스트

### ✅ **시연 전 준비**
- [ ] 가상환경 활성화
- [ ] server.py 실행 중
- [ ] Claude Desktop 설정 완료
- [ ] API 키 설정 확인
- [ ] 브라우저 자동화 테스트 완료

### ✅ **실제 시연**
- [ ] Claude Desktop에서 "피자 검색해줘" 입력
- [ ] 브라우저 자동 실행 확인
- [ ] Uber Eats 접속 및 검색 확인
- [ ] 검색 결과 반환 확인
- [ ] 스크린샷 저장 확인

### ✅ **고급 기능 시연**
- [ ] 복잡한 검색 쿼리 테스트
- [ ] 검색 결과 조회 기능
- [ ] 에러 핸들링 확인

## 🎯 원작자 스타일 완벽 재현!

이제 정말로 **Claude Desktop에서 자연어로 말하면 자동으로 브라우저가 실행되어서 Uber Eats에서 음식을 검색해주는** 원작자와 똑같은 시연이 가능합니다!

### 🌟 핵심 포인트:
1. **Zero Code**: 코딩 없이 자연어만으로 제어
2. **실시간**: Claude Desktop → MCP Server → 브라우저 자동화
3. **시각적**: 브라우저 창이 실제로 열려서 작업 과정 확인 가능
4. **완전 자동**: 검색부터 결과 추출까지 모든 과정 자동화

**이제 Claude Desktop에서 "피자 검색해줘"라고 말씀해보세요! 🍕✨** 