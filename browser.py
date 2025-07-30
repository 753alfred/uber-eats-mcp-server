from typing import Awaitable, Callable
from playwright.async_api import async_playwright, Browser, Page
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import warnings
import asyncio

load_dotenv()

warnings.filterwarnings("ignore")

class BrowserAgent:
    def __init__(self):
        self.browser: Browser = None
        self.page: Page = None
        self.llm = ChatAnthropic(model_name="claude-3-5-sonnet-latest")
        self.playwright = None
    
    async def start_browser(self):
        """브라우저를 시작합니다."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=False,  # 시연용: 브라우저 창을 보이게 설정
            args=[
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        self.page = await context.new_page()
        # 타임아웃을 60초로 늘림
        self.page.set_default_timeout(60000)
    
    async def close_browser(self):
        """브라우저를 닫습니다."""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def navigate_to(self, url: str):
        """지정된 URL로 이동합니다."""
        if not self.page:
            await self.start_browser()
        
        print(f"🌐 {url}로 이동 중...")
        try:
            # 더 긴 타임아웃과 wait_until 옵션 사용
            await self.page.goto(url, wait_until='domcontentloaded', timeout=60000)
            print("✅ 페이지 로딩 완료")
            
            # 잠시 대기하여 JavaScript 로딩 완료
            await asyncio.sleep(3)
            
        except Exception as e:
            print(f"⚠️ 페이지 로딩 중 오류: {str(e)}")
            # 간단한 대체 사이트로 테스트
            await self.page.goto("https://www.google.com", wait_until='domcontentloaded')
            print("📍 Google로 대체 이동 완료")
    
    async def search_and_click(self, search_term: str):
        """검색어를 입력하고 검색합니다."""
        try:
            print(f"🔍 '{search_term}' 검색 중...")
            # 다양한 검색 입력창 셀렉터 시도
            selectors = [
                'input[type="text"]',
                'input[placeholder*="search"]',
                'input[aria-label*="search"]',
                'input[name="q"]',
                'input[name="search"]',
                '[data-testid="search-input"]'
            ]
            
            search_input = None
            for selector in selectors:
                try:
                    search_input = await self.page.wait_for_selector(selector, timeout=5000)
                    if search_input:
                        print(f"✅ 검색창 발견: {selector}")
                        break
                except:
                    continue
            
            if search_input:
                await search_input.fill(search_term)
                await search_input.press('Enter')
                await self.page.wait_for_load_state('networkidle', timeout=30000)
                print("✅ 검색 완료")
            else:
                print("⚠️ 검색창을 찾을 수 없습니다")
                
        except Exception as e:
            print(f"⚠️ 검색 중 오류: {str(e)}")
    
    async def get_page_content(self):
        """현재 페이지의 텍스트 내용을 가져옵니다."""
        if self.page:
            try:
                content = await self.page.inner_text('body')
                return content[:1000]  # 처음 1000자만 반환
            except:
                return "페이지 내용을 가져올 수 없습니다"
        return "페이지가 로드되지 않았습니다"
    
    async def take_screenshot(self, path: str = "screenshot.png"):
        """스크린샷을 찍습니다."""
        if self.page:
            try:
                await self.page.screenshot(path=path)
                print(f"📸 스크린샷 저장: {path}")
            except Exception as e:
                print(f"⚠️ 스크린샷 실패: {str(e)}")

async def run_browser_agent(task: str, on_step: Callable[[], Awaitable[None]] = None):
    """브라우저 에이전트를 실행합니다."""
    agent = BrowserAgent()
    
    try:
        print("🚀 브라우저 시작 중...")
        await agent.start_browser()
        
        if on_step:
            await on_step()
        
        # Uber Eats 사이트로 이동 (실패시 Google로 대체)
        await agent.navigate_to("https://www.ubereats.com/")
        
        if on_step:
            await on_step()
        
        # 작업이 검색과 관련된 경우 처리
        if "search" in task.lower():
            # 작업에서 검색어 추출 (간단한 예시)
            search_term = task.split("search for")[-1].strip().strip('"\'')
            if search_term:
                await agent.search_and_click(search_term)
                
                if on_step:
                    await on_step()
        
        # 페이지 내용 가져오기
        print("📄 페이지 내용 추출 중...")
        content = await agent.get_page_content()
        
        # 스크린샷 찍기
        await agent.take_screenshot()
        
        if on_step:
            await on_step()
        
        return f"✅ Task completed: {task}\n📄 Page content preview:\n{content}"
        
    except Exception as e:
        return f"❌ Error executing task: {str(e)}"
    finally:
        print("🔄 브라우저 종료 중...")
        await agent.close_browser()
