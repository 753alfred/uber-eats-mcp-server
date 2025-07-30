#!/usr/bin/env python3
"""
간단한 브라우저 자동화 테스트 스크립트
"""

import asyncio
from browser import run_browser_agent

async def main():
    print("🚀 브라우저 자동화 테스트를 시작합니다...")
    
    # 간단한 작업 정의
    task = "Navigate to Uber Eats and search for pizza"
    
    # 진행 상황을 보여주는 콜백 함수
    step_count = 0
    async def progress_callback():
        nonlocal step_count
        step_count += 1
        print(f"📍 Step {step_count} completed")
    
    try:
        # 브라우저 에이전트 실행
        result = await run_browser_agent(task, progress_callback)
        
        print("\n✅ 작업 완료!")
        print("📋 결과:")
        print(result)
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")

if __name__ == "__main__":
    print("🤖 Uber Eats MCP 브라우저 자동화 데모")
    print("=" * 50)
    asyncio.run(main()) 