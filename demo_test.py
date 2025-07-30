#!/usr/bin/env python3
"""
Uber Eats MCP 시연용 테스트 스크립트
브라우저 창이 열리면서 실제 검색 과정을 보여줍니다.
"""

import asyncio
from browser import run_browser_agent

async def demo_search(search_term: str):
    """시연용 검색 함수"""
    print(f"🍕 '{search_term}' 검색을 시작합니다...")
    print("📱 브라우저가 곧 열립니다. 실시간으로 검색 과정을 확인하세요!")
    
    # Uber Eats 검색 태스크
    task = f"""
0. Start by going to: https://www.ubereats.com/se-en/
1. Type "{search_term}" in the global search bar and press enter
2. Go to the first search result (this is the most popular restaurant).
3. When you can see the menu options for the restaurant, we need to use the specific search input for the restaurant located under the banner (identify it by the placeholder "Search in [restaurant name]"
4. Click the input field and type "{search_term}", then press enter
5. Check for menu options related to "{search_term}"
6. Get the name, url and price of the top 3 items related to "{search_term}". URL is very important
"""
    
    step_count = 0
    
    async def step_handler():
        nonlocal step_count
        step_count += 1
        print(f"✅ 단계 {step_count} 완료")
    
    try:
        result = await run_browser_agent(task=task, on_step=step_handler)
        print(f"\n🎉 검색 완료! 결과:")
        print(result)
        return result
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return None

async def demo_order(item_url: str, item_name: str):
    """시연용 주문 함수"""
    print(f"🛒 '{item_name}' 주문을 시작합니다...")
    print("⚠️  주의: 실제 주문이 진행되므로 결제 전에 중단하세요!")
    
    task = f"""
1. Go to {item_url}
2. Click "Add to order"
3. Wait 3 seconds
4. Click "Go to checkout"
5. If there are upsell modals, click "Skip"
6. STOP HERE - DO NOT ACTUALLY PLACE THE ORDER
7. Just report that you reached the checkout page
"""
    
    step_count = 0
    
    async def step_handler():
        nonlocal step_count
        step_count += 1
        print(f"✅ 주문 단계 {step_count} 완료")
    
    try:
        result = await run_browser_agent(task=task, on_step=step_handler)
        print(f"\n🎉 주문 프로세스 완료! (결제는 하지 않음)")
        print(result)
        return result
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return None

async def main():
    """메인 시연 함수"""
    print("🎬 Uber Eats MCP 시연 시작!")
    print("=" * 50)
    
    # 1. 검색 시연
    search_term = input("검색할 음식을 입력하세요 (기본값: 계피빵): ").strip()
    if not search_term:
        search_term = "계피빵"
    
    result = await demo_search(search_term)
    
    if result:
        print("\n" + "=" * 50)
        print("검색이 완료되었습니다!")
        
        # 2. 주문 시연 여부 확인
        order_demo = input("주문 프로세스도 시연하시겠습니까? (y/N): ").strip().lower()
        
        if order_demo == 'y':
            # 예시 URL (실제 결과에서 추출해야 함)
            item_url = input("주문할 상품 URL을 입력하세요: ").strip()
            item_name = input("상품명을 입력하세요: ").strip()
            
            if item_url and item_name:
                await demo_order(item_url, item_name)
            else:
                print("❌ URL과 상품명이 필요합니다.")
    
    print("\n🎬 시연 완료!")

if __name__ == "__main__":
    print("🍕 Uber Eats MCP 브라우저 자동화 시연")
    print("💡 팁: 브라우저 창이 열리면서 실시간으로 작업 과정을 볼 수 있습니다")
    print()
    
    asyncio.run(main()) 