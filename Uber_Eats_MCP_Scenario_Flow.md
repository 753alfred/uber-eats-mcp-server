# Uber Eats MCP 시나리오 플로우 분석 🍕

> MCP(Model Context Protocol)를 활용한 Uber Eats 자동화의 실제 동작 과정 완전 분석

## 📋 목차
- [🎯 프로젝트 개요](#-프로젝트-개요)
- [🔄 전체 플로우 다이어그램](#-전체-플로우-다이어그램)
- [💬 실제 대화 시나리오](#-실제-대화-시나리오)
- [🛠️ 기술적 구현 분석](#️-기술적-구현-분석)
- [📊 단계별 상세 분석](#-단계별-상세-분석)
- [🔍 에러 처리 및 예외 상황](#-에러-처리-및-예외-상황)
- [🎯 핵심 성공 요소](#-핵심-성공-요소)
- [🚀 실제 실행 방법](#-실제-실행-방법)

---

## 🎯 프로젝트 개요

### 시스템 구성
```
사용자 ↔ AI모델(Claude/GPT) ↔ MCP서버 ↔ Browser-Use ↔ Uber Eats 웹사이트
```

### 핵심 기능
1. **음식 검색**: 특정 음식을 Uber Eats에서 검색
2. **메뉴 분석**: 검색 결과에서 상위 옵션 추출
3. **자동 주문**: 선택된 음식을 실제로 주문

---

## 🔄 전체 플로우 시퀀스 다이어그램

```mermaid
sequenceDiagram
    participant U as 👤 사용자
    participant AI as 🤖 AI 모델
    participant MCP as 🛠️ MCP 서버
    participant Browser as 🌐 Browser-Use
    participant UberEats as 🍕 Uber Eats

    Note over U,UberEats: 음식 검색 단계
    U->>AI: "오후 간식으로 계피빵 주문하고 싶은데 어디서 살 수 있을까요?"
    AI->>AI: 의도 분석 (계피빵 검색 필요)
    AI->>MCP: find_menu_options("계피빵")
    MCP->>AI: "검색 시작됨, 2분 후 결과 확인"
    
    Note over MCP,UberEats: 백그라운드 브라우저 작업
    MCP->>Browser: 검색 작업 시작
    Browser->>UberEats: https://ubereats.com/se-en/ 접속
    Browser->>UberEats: 전역 검색창에 "계피빵" 입력
    UberEats->>Browser: 검색 결과 페이지 반환 (McDonald's, 7-Eleven 등)
    Browser->>UberEats: McDonald's 확인 → 계피빵 없음
    Browser->>Browser: 계피빵 보유 매장 탐색
    Browser->>UberEats: 7-Eleven에서 계피빵 발견 → 선택
    UberEats->>Browser: 7-Eleven 페이지 로드
    Browser->>UberEats: 매장 내 "계피빵" 검색
    UberEats->>Browser: 계피빵 90g 발견
    Browser->>Browser: 상품 정보 수집 (이름, 가격, URL)
    Browser->>MCP: 검색 결과 전달
    MCP->>MCP: 결과를 리소스로 저장

    Note over AI,U: 결과 제시 단계  
    AI->>MCP: get_search_results(request_id)
    MCP->>AI: 7-Eleven 계피빵 정보 반환
    AI->>AI: 사용자 친화적 형태로 변환
    AI->>U: "좋은 소식! 오후 간식용 계피빵을 찾았습니다!"

    Note over U,UberEats: 주문 단계
    U->>AI: "이걸로 주문해주세요"
    AI->>MCP: order_food(item_url, item_name)
    MCP->>AI: "주문 진행 중..."
    
    Note over MCP,UberEats: 실제 주문 프로세스
    MCP->>Browser: 주문 작업 시작
    Browser->>UberEats: 선택된 아이템 페이지로 이동
    Browser->>UberEats: "Add to order" 클릭
    UberEats->>Browser: 장바구니 업데이트 확인
    Browser->>UberEats: "Go to checkout" 클릭
    UberEats->>Browser: 체크아웃 페이지 로드
    Browser->>UberEats: 업셀 모달 "Skip" 클릭
    Browser->>UberEats: "Place order" 클릭
    UberEats->>Browser: 주문 완료 확인
    Browser->>MCP: 주문 성공 결과 전달

    Note over AI,U: 완료 확인
    MCP->>AI: "주문이 성공적으로 완료됨"
    AI->>U: "🎉 주문 완료! 25-35분 후 도착 예정"
```

---

## 💬 실제 대화 시나리오

### 시나리오 1: 기본 음식 검색 및 주문

#### 👤 사용자
```
"오후 간식으로 계피빵 주문하고 싶은데 어디서 살 수 있을까요?"
```

#### 🤖 AI 분석 과정
```
사용자가 계피빵을 찾고 있음을 인식
→ Uber Eats에서 검색이 필요함을 판단
→ MCP 도구 'find_menu_options' 사용 결정
```

#### 🛠️ MCP 도구 호출
```json
{
  "tool": "find_menu_options",
  "parameters": {
    "search_term": "계피빵"
  }
}
```

#### 🤖 AI 응답 (1차)
```
"오후 간식용 계피빵을 찾을 수 있는 곳을 도와드리겠습니다. Uber Eats에서 옵션을 검색해보겠습니다.

MCP 도구 호출: find_menu_options ✓

Uber Eats에서 '계피빵' 검색을 시작했습니다. 검색 진행 중이며 약 2분 정도 소요될 예정입니다. 결과가 나올 때까지 기다려주세요."
```

#### ⏳ 대기 과정
```
🤖 AI: "시스템이 현재 다음 작업을 수행 중입니다:
1. Uber Eats 웹사이트 열기
2. '계피빵' 검색 수행
3. McDonald's 확인 → 계피빵 없음
4. 7-Eleven에서 계피빵 발견!
5. 상품명, URL, 가격 정보 수집"
```

#### 📋 검색 완료 후 결과 조회
```json
{
  "tool": "get_search_results", 
  "resource_uri": "resource://search_results/{request_id}"
}
```

#### 🤖 AI 응답 (2차 - 결과 제시)
```
"좋은 소식! 오후 간식용 계피빵 옵션을 찾았습니다:

🥐 **계피빵 옵션:**

**7-Eleven St Eriksgatan 89 - 계피빵 90g**
- 가격: 3,500원
- URL: https://ubereats.com/se-en/store/7-eleven-st-eriksgatan-89/item/kanelbulle-90g
- 설명: 신선한 90g 계피빵, 오후 간식으로 완벽

※ McDonald's에서는 계피빵을 판매하지 않아 7-Eleven에서 찾아드렸습니다.

이 계피빵을 주문하시겠습니까? 바로 주문 도와드릴 수 있습니다!"
```

#### 👤 사용자 선택
```
"네, 이걸로 주문해주세요"
```

#### 🛠️ 주문 도구 호출
```json
{
  "tool": "order_food",
  "parameters": {
    "item_url": "https://ubereats.com/se-en/store/7-eleven-st-eriksgatan-89/item/kanelbulle-90g",
    "item_name": "계피빵 90g"
  }
}
```

#### 🤖 AI 응답 (주문 진행)
```
"훌륭한 선택입니다! 지금 7-Eleven의 계피빵 90g를 주문 진행하겠습니다.

'계피빵 90g' 주문이 시작되었습니다. 주문이 처리 중입니다.

시스템이 현재:
1. ✓ 상품 페이지로 이동
2. ⏳ 장바구니에 추가  
3. ⏳ 결제 페이지로 진행
4. ⏳ 주문 완료 처리

주문이 성공적으로 완료되면 확인해드리겠습니다!"
```

#### 🎉 주문 완료
```
"🎉 주문이 성공적으로 완료되었습니다!

7-Eleven의 계피빵 90g가 주문되었습니다:
- 상품: 계피빵 90g  
- 가격: 3,500원
- 예상 배송시간: 25-35분
- 주문번호: #UE202412345

오후 간식으로 완벽합니다! 계피빵이 신선하고 따뜻하게 도착할 예정입니다. 맛있게 드세요!"
```

---

### 시나리오 2: 복잡한 요청 처리

#### 👤 사용자
```
"오후 간식으로 달콤한 걸 원해요. 계피빵이나 마지팬 케이크 중에서 평점 좋은 걸로 찾아주실 수 있나요? 6,000원 이하로 부탁드려요."
```

#### 🤖 AI 분석 과정
```
- 사용자가 두 가지 옵션을 원함: 계피빵 OR 마지팬 케이크
- 가격 제한: 6,000원 이하 (약 50 SEK)
- 평점 기준으로 최고 품질 원함
→ 두 번의 검색이 필요함을 판단
```

#### 🛠️ 첫 번째 검색
```json
{
  "tool": "find_menu_options",
  "parameters": {
    "search_term": "계피빵"
  }
}
```

#### 🛠️ 두 번째 검색  
```json
{
  "tool": "find_menu_options", 
  "parameters": {
    "search_term": "마지팬 케이크"
  }
}
```

#### 🤖 AI 종합 응답
```
"오후 간식용 계피빵과 마지팬 케이크 옵션을 모두 검색했습니다! 6,000원 이하의 평점 좋은 옵션들입니다:

🥐 **계피빵 옵션:**
1. **7-Eleven - 계피빵 90g** (4.5★)
   - 3,500원 | 신선한 90g, 편리한 위치
   
2. **ICA Supermarket - 프리미엄 계피빵** (4.7★)  
   - 4,400원 | 유기농 밀가루, 여분의 계피

🍰 **마지팬 케이크 옵션:**
1. **Café Lagerbäck - 미니 마지팬 케이크** (4.9★)
   - 5,200원 | 전통 레시피, 완벽한 마지팬 코팅
   
2. **Konditori Hollandia - 마지팬 케이크 조각** (4.6★)
   - 4,900원 | 넉넉한 양, 신선한 크림

**추천:** Café Lagerbäck의 미니 마지팬 케이크가 최고 평점(4.9★)이며 5,200원으로 오후 간식에 완벽합니다.

어떤 것이 마음에 드시나요? 바로 주문해드릴 수 있습니다!"
```

---

### 시나리오 3: 에러 상황 및 복구

#### 👤 사용자
```
"좋은 곳에서 스시 주문해주세요"
```

#### 🛠️ 검색 시도
```json
{
  "tool": "find_menu_options",
  "parameters": {
    "search_term": "sushi"
  }
}
```

#### ❌ 검색 실패 상황
```
시나리오: Uber Eats에서 sushi 검색 시 일시적 오류 발생
```

#### 🤖 AI 에러 처리 응답
```
"Uber Eats에서 최고의 스시 옵션을 검색하고 있습니다...

⚠️ 스시 옵션 검색 중 일시적인 문제가 발생했습니다. 다음과 같은 원인일 수 있습니다:
- Uber Eats 트래픽 과부하
- 일시적 연결 문제
- 지역 이용 제한

더 구체적인 검색을 시도해보겠습니다. 알려주실 수 있나요:
1. 어떤 종류의 스시를 선호하시나요? (예: 연어, 참치, 모둠)
2. 특별히 염두에 둔 레스토랑이 있나요?
3. 예산 범위는 어떻게 되나요?

아니면 잠시 후 일반 스시 검색을 다시 시도해볼까요?"
```

#### 👤 사용자 대응
```
"그냥 연어 스시로 다시 시도해보세요, 좋은 곳이면 어디든 괜찮아요"
```

#### 🛠️ 재시도
```json
{
  "tool": "find_menu_options",
  "parameters": {
    "search_term": "salmon sushi"
  }
}
```

#### 🤖 성공 응답
```
"완벽합니다! 이번에는 검색이 성공했습니다. 훌륭한 연어 스시 옵션들입니다:

🍣 **최고의 연어 스시 옵션:**

1. **Sushi Yama - 연어 디럭스 세트** (4.8★)
   - 16,700원 | 프리미엄 연어초밥 8피스 + 연어롤
   
2. **Wasabi Warriors - 연어 스페셜** (4.7★)  
   - 14,400원 | 연어초밥 6피스 + 연어 아보카도 롤 6피스

3. **Tokyo Express - 연어 콤보** (4.6★)
   - 11,300원 | 연어초밥 4피스 + 연어 데리야키 롤

Sushi Yama의 연어 디럭스 세트가 연어 애호가들에게 최고의 품질을 제공합니다. 이걸로 주문해드릴까요?"
```

---

## 🛠️ 기술적 구현 분석

### MCP 서버 구조
```python
# server.py 핵심 함수들
@mcp.tool()
async def find_menu_options(search_term: str, context: Context) -> str:
    # 검색 작업을 백그라운드에서 시작
    task = f"""
    0. Start by going to: https://www.ubereats.com/se-en/
    1. Type "{search_term}" in the global search bar and press enter
    2. Go to the restaurant that actually has "{search_term}" available
    3. Use restaurant-specific search for "{search_term}"
    4. Get name, url and price of available items
    """
    
    # 비동기 작업 시작
    asyncio.create_task(perform_search(context.request_id, search_term, task, context))
    
    return f"Search for '{search_term}' started. Check back using resource URI..."

@mcp.resource(uri="resource://search_results/{request_id}")
async def get_search_results(request_id: str) -> str:
    # 저장된 검색 결과 반환
    return search_results.get(request_id, "No results found")
```

### 브라우저 자동화 과정
```python
# browser.py 에서 실제 브라우저 조작
async def run_browser_agent(task: str, on_step: Callable):
    agent = Agent(
        task=task,
        browser=browser,
        llm=llm,  # Claude AI가 웹페이지 분석
        register_new_step_callback=on_step,
    )
    
    # AI가 실제 웹사이트를 보고 조작
    result = await agent.run()
    return result.final_result()
```

---

## 📊 단계별 상세 분석

### 1단계: 사용자 의도 파악
```
입력: "오후 간식으로 계피빵 주문하고 싶은데 어디서 살 수 있을까요?"

AI 분석:
- '오후 간식' = 간단한 디저트나 베이커리 제품
- '계피빵' = 스웨덴 전통 페이스트리 (kanelbulle)  
- 위치 질문 = 구매 가능한 장소 찾기
→ 결론: Uber Eats에서 계피빵 검색 필요
```

### 2단계: MCP 도구 선택
```
사용 가능한 도구들:
1. find_menu_options: 음식 검색
2. order_food: 음식 주문
3. get_search_results: 검색 결과 조회

선택: find_menu_options(search_term="계피빵")
```

### 3단계: 브라우저 자동화 실행
```
실행 단계:
1. 브라우저 시작 (Chrome headless)
2. https://www.ubereats.com/se-en/ 접속
3. 전역 검색창에 "계피빵" 입력
4. 검색 결과: McDonald's(1위), 7-Eleven(2위) 등 확인
5. McDonald's 확인 → 계피빵 메뉴 없음 확인
6. 7-Eleven St Eriksgatan 89 매장 선택
7. 7-Eleven 매장 페이지 접속
8. 계피빵 90g 상품 정보 수집:
   - 이름 (name)
   - 가격 (price) 
   - URL (url)
```

### 4단계: 결과 처리 및 저장
```python
# 수집된 데이터 예시 (실제 7-Eleven 결과)
search_results[request_id] = {
    "items": [
        {
            "name": "계피빵 90g",
            "price": "3,500원", 
            "url": "https://ubereats.com/se-en/store/7-eleven-st-eriksgatan-89/item/kanelbulle-90g",
            "store": "7-Eleven St Eriksgatan 89",
            "note": "McDonald's에서는 계피빵을 판매하지 않아 7-Eleven에서 발견"
        }
    ],
    "status": "completed",
    "timestamp": "2024-12-28T10:30:00Z"
}
```

### 5단계: AI 결과 해석 및 응답
```
AI가 수행하는 작업:
1. 리소스 URI로 검색 결과 조회
2. 데이터를 사용자 친화적 형태로 변환
3. 가격 비교 및 추천사항 생성
4. 선택 옵션을 명확하게 제시
```

### 6단계: 주문 프로세스 (선택 시)
```
order_food 실행 과정:
1. 선택된 아이템 URL로 이동
2. "Add to order" 버튼 클릭
3. 장바구니 확인 (3초 대기)
4. "Go to checkout" 클릭  
5. 업셀 모달 건너뛰기 ("Skip")
6. "Place order" 클릭
7. 주문 완료 확인
```

---

## 🔍 에러 처리 및 예외 상황

### 일반적인 오류 상황들

#### 1. 네트워크 연결 오류
```python
# 에러 상황
ConnectionError: "Unable to connect to ubereats.com"

# AI 응답 예시
"현재 Uber Eats 연결에 문제가 있습니다. 다음과 같은 원인일 수 있습니다:
- 네트워크 연결 문제
- Uber Eats 사이트 점검  
- 지역 접근 제한

다음 중 어떻게 하시겠습니까:
1. 몇 분 후 다시 시도해볼까요?
2. 다른 음식 배달 플랫폼에서 검색해볼까요?
3. 대신 지역 레스토랑을 찾아드릴까요?"
```

#### 2. 검색 결과 없음
```python
# 에러 상황  
search_results[request_id] = "No items found for '계피빵'"

# AI 응답 예시
"철저히 검색했지만 현재 해당 지역에서 배달 가능한 계피빵 옵션을 찾을 수 없습니다. 다음과 같은 이유일 수 있습니다:

- 해당 지역에서 해당 상품을 구할 수 없음
- 레스토랑이 문을 닫았거나 배달을 하지 않음
- 검색어 조정이 필요할 수 있음

다음 대안을 제안드립니다:
1. '시나몬 롤' 또는 '시나몬 번'으로 검색
2. '카다몬 번' 찾기 (유사한 스웨덴 페이스트리)
3. 계피빵을 판매할 수 있는 인근 베이커리 검색

이 중 어떤 대안을 시도해보시겠습니까?"
```

#### 3. 주문 프로세스 오류
```python
# 에러 상황
OrderError: "Unable to complete checkout process"

# AI 응답 예시
"주문을 진행하는 중 문제가 발생했습니다. 상품은 성공적으로 장바구니에 추가되었지만 결제 과정에서 실패했습니다. 다음과 같은 원인일 수 있습니다:

- 결제 수단 문제
- 배송 주소 문제  
- 레스토랑 일시적 이용 불가
- 높은 수요로 인한 시스템 지연

다음과 같이 권장합니다:
1. Uber Eats 앱/웹사이트에서 수동으로 주문을 완료하실 수 있습니다
2. 상품이 이미 장바구니에 있습니다: '7-Eleven의 계피빵 90g'
3. 또는 같은 매장에서 다른 상품으로 주문을 시도해볼 수 있습니다

어떻게 하시겠습니까?"
```

### 복구 전략

#### 자동 재시도 메커니즘
```python
async def robust_search(search_term: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            result = await perform_search(search_term)
            return result
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(5)  # 5초 대기 후 재시도
                continue
            else:
                return f"Search failed after {max_retries} attempts: {str(e)}"
```

#### 사용자 피드백 루프
```
AI가 오류 시 제공하는 옵션들:
1. 자동 재시도 제안
2. 대안 검색어 제안  
3. 다른 플랫폼 제안
4. 수동 방법 안내
5. 문제 신고 옵션
```

---

## 🎯 핵심 성공 요소

### 1. 자연스러운 대화 흐름
- AI가 사용자 의도를 정확히 파악
- 기술적 복잡성을 숨기고 결과에 집중
- 진행 상황을 투명하게 공유

### 2. 실용적인 오류 처리
- 명확한 오류 설명과 해결 방안 제시
- 사용자에게 선택권 제공
- 자동 복구 시도

### 3. 효율적인 MCP 활용
- 비동기 작업으로 사용자 대기시간 최소화
- 리소스 기반 결과 조회로 안정성 확보
- 모듈화된 도구 설계

---

## 🚀 실제 실행 방법

### 환경 설정 🔧
```bash
# 1. Python 패키지 설치 (한 번에 설치)
pip install browser-use langchain-anthropic python-dotenv fastmcp mcp[cli]

# 2. 브라우저 드라이버 설치 (Playwright 자동화 도구)
playwright install chromium --with-deps

# 3. 환경 변수 파일 생성
cp .env.example .env

# 4. .env 파일 편집 (메모장이나 VS Code로 열어서 API 키 입력)
# ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# 또는
# OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

💡 **API 키 받는 방법:**
- **Anthropic(Claude)**: https://console.anthropic.com 에서 가입 후 API 키 발급
- **OpenAI(GPT)**: https://platform.openai.com 에서 가입 후 API 키 발급

### 실행 과정

#### 1단계: MCP 서버 실행 (터미널 1)
```bash
cd uber-eats-mcp-server
python server.py
```

#### 2단계: AI 모델과 대화 (터미널 2)
```bash
# 방법 1: Claude Desktop 사용 (추천)
# Claude Desktop을 설치하고 MCP 설정에서 서버 추가

# 방법 2: 개발용 도구 사용
uv run mcp dev server.py

# 방법 3: 직접 MCP 클라이언트 실행
npx @modelcontextprotocol/inspector
```

#### 실제 사용법
1. **AI에게 질문**: "오후 간식으로 계피빵 주문하고 싶은데 어디서 살 수 있을까요?"
2. **MCP 서버가 자동 실행**: `find_menu_options` 도구 호출
3. **브라우저 자동화**: Chrome이 열리면서 Uber Eats 접속
4. **실시간 확인 가능**: 브라우저에서 AI가 어떻게 페이지를 조작하는지 볼 수 있음
5. **결과 반환**: AI가 찾은 옵션들을 사용자에게 제시
6. **주문 진행**: 선택 시 `order_food` 도구로 실제 주문

### 시스템 구성
```
[사용자] ↔ [AI 클라이언트] ↔ [MCP 서버] ↔ [Browser-Use] ↔ [Uber Eats]
   ↑           ↑                ↑             ↑              ↑
터미널2     Claude Desktop    server.py    browser.py    실제 웹사이트
```

### 주의사항 및 팁 💡
- **브라우저 창 확인**: 브라우저가 자동으로 열리므로 AI가 어떻게 페이지를 조작하는지 실시간으로 볼 수 있습니다
- **테스트 시 주의**: 실제 주문이 진행되므로 결제 정보 입력 전에 중단하세요
- **인터넷 환경**: 안정적인 인터넷 연결과 Uber Eats 접속이 필요합니다
- **API 키 필수**: Claude API 키(ANTHROPIC_API_KEY) 또는 OpenAI API 키가 필요합니다
- **Chrome 브라우저**: Chrome이 설치되어 있어야 합니다 (자동으로 실행됨)
- **한국어 질문**: "계피빵 주문하고 싶어요", "연어초밥 찾아주세요" 등 자연스러운 한국어로 대화 가능

