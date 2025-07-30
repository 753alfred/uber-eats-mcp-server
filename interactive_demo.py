#!/usr/bin/env python3
"""
인터랙티브 Uber Eats 검색 시연 - Object Detection 포함
사용자가 텍스트를 입력하여 실시간 검색 및 요소 감지 수행
"""

import gradio as gr
import asyncio
import os
from enhanced_browser import initialize_agent, cleanup_agent, global_agent
from typing import Tuple, Optional
import json
from datetime import datetime

class InteractiveDemo:
    """인터랙티브 시연 클래스"""
    
    def __init__(self):
        self.agent = None
        self.is_initialized = False
        
    async def initialize(self):
        """에이전트 초기화"""
        if not self.is_initialized:
            print("🚀 브라우저 에이전트 초기화 중...")
            self.agent = await initialize_agent()
            self.is_initialized = True
            print("✅ 초기화 완료!")
        return self.agent
    
    async def cleanup(self):
        """리소스 정리"""
        if self.is_initialized:
            await cleanup_agent()
            self.is_initialized = False
            print("🔄 리소스 정리 완료")

# 전역 데모 인스턴스
demo_instance = InteractiveDemo()

def sync_search_and_detect(search_term: str) -> Tuple[str, Optional[str], Optional[str], str, str]:
    """
    동기 함수로 비동기 검색 및 Object Detection 실행
    
    Returns:
        - status_message: 상태 메시지
        - original_image: 원본 스크린샷 경로
        - detected_image: Object Detection 적용된 이미지 경로
        - detection_report: 감지 결과 리포트
        - page_content: 페이지 내용
    """
    if not search_term or not search_term.strip():
        return (
            "❌ 검색어를 입력해주세요!", 
            None, None, 
            "검색어가 비어있습니다.", 
            ""
        )
    
    # 이벤트 루프 실행
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # 에이전트 초기화
        agent = loop.run_until_complete(demo_instance.initialize())
        
        # 검색 및 Object Detection 실행
        print(f"\n{'='*50}")
        print(f"🔍 검색어: '{search_term}'")
        print(f"{'='*50}")
        
        results = loop.run_until_complete(agent.navigate_and_search(search_term))
        
        if results['success']:
            # 성공 메시지 생성
            status_msg = f"✅ 검색 완료!\n"
            status_msg += f"🎯 감지된 요소: {len(results['detected_elements'])}개\n"
            status_msg += f"📝 검색어: '{search_term}'\n"
            status_msg += f"⏰ 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Object Detection 리포트 생성
            detection_report = agent.generate_detection_report(results['detected_elements'])
            
            return (
                status_msg,
                results['screenshot_path'],
                results['detected_image_path'],
                detection_report,
                results['page_content']
            )
        else:
            error_msg = f"❌ 검색 실패: {results.get('error', '알 수 없는 오류')}"
            return (
                error_msg,
                None, None,
                "검색에 실패했습니다.",
                ""
            )
            
    except Exception as e:
        error_msg = f"❌ 시스템 오류: {str(e)}"
        print(f"오류 발생: {str(e)}")
        return (
            error_msg,
            None, None,
            f"시스템 오류가 발생했습니다: {str(e)}",
            ""
        )
    finally:
        loop.close()

def get_search_history() -> str:
    """검색 기록 가져오기"""
    try:
        if demo_instance.agent and demo_instance.is_initialized:
            history = demo_instance.agent.get_search_history()
            if not history:
                return "📝 검색 기록이 없습니다."
            
            history_text = "📚 검색 기록:\n\n"
            for i, record in enumerate(history[-10:], 1):  # 최근 10개만
                timestamp = datetime.fromtimestamp(record['timestamp']).strftime('%H:%M:%S')
                status = "✅" if record['success'] else "❌"
                history_text += f"{i}. [{timestamp}] {status} '{record['search_term']}' "
                history_text += f"({record['elements_count']}개 요소)\n"
            
            return history_text
        else:
            return "🔄 에이전트가 초기화되지 않았습니다."
    except Exception as e:
        return f"❌ 기록 조회 오류: {str(e)}"

def cleanup_demo():
    """데모 리소스 정리"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(demo_instance.cleanup())
        loop.close()
        return "✅ 브라우저가 성공적으로 종료되었습니다."
    except Exception as e:
        return f"❌ 종료 중 오류: {str(e)}"

# Gradio 인터페이스 구성
def create_interface():
    """Gradio 인터페이스 생성"""
    
    with gr.Blocks(
        title="🤖 Uber Eats Interactive Search & Object Detection Demo",
        theme=gr.themes.Soft()
    ) as demo:
        
        # 헤더
        gr.Markdown("""
        # 🤖 Uber Eats Interactive Search & Object Detection Demo
        
        **실시간 검색과 AI 객체 감지를 체험해보세요!**
        
        ### 🎯 기능:
        - 📝 **텍스트 입력**: 원하는 음식을 자유롭게 입력
        - 🔍 **실시간 검색**: Uber Eats에서 자동 검색 수행  
        - 🎯 **Object Detection**: 페이지 요소 자동 감지 및 시각화
        - 📸 **스크린샷 비교**: 원본 vs Object Detection 결과
        - 📊 **상세 분석**: 감지된 요소들의 상세 리포트
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                # 입력 섹션
                gr.Markdown("## 📝 검색 입력")
                search_input = gr.Textbox(
                    label="🔍 검색할 음식을 입력하세요",
                    placeholder="예: pizza, burger, sushi, 치킨, 피자...",
                    lines=1
                )
                
                search_btn = gr.Button(
                    "🚀 검색 및 Object Detection 실행", 
                    variant="primary",
                    size="lg"
                )
                
                # 상태 표시
                status_output = gr.Textbox(
                    label="📊 실행 상태",
                    lines=4,
                    interactive=False
                )
            
            with gr.Column(scale=2):
                # 이미지 결과 섹션
                gr.Markdown("## 📸 검색 결과 이미지")
                
                with gr.Row():
                    original_image = gr.Image(
                        label="📷 원본 스크린샷",
                        height=300
                    )
                    detected_image = gr.Image(
                        label="🎯 Object Detection 결과",
                        height=300
                    )
        
        with gr.Row():
            with gr.Column():
                # Object Detection 리포트
                gr.Markdown("## 🎯 Object Detection 리포트")
                detection_report = gr.Textbox(
                    label="📋 감지된 요소 상세 정보",
                    lines=10,
                    interactive=False
                )
            
            with gr.Column():
                # 페이지 내용 미리보기
                gr.Markdown("## 📄 페이지 내용 미리보기")
                page_content = gr.Textbox(
                    label="📝 추출된 텍스트 내용",
                    lines=10,
                    interactive=False
                )
        
        # 검색 기록 및 제어
        with gr.Row():
            with gr.Column():
                gr.Markdown("## 📚 검색 기록")
                history_btn = gr.Button("📜 검색 기록 보기")
                search_history = gr.Textbox(
                    label="🕒 최근 검색 기록",
                    lines=5,
                    interactive=False
                )
            
            with gr.Column():
                gr.Markdown("## ⚙️ 시스템 제어")
                cleanup_btn = gr.Button(
                    "🔄 브라우저 종료 및 리소스 정리", 
                    variant="secondary"
                )
                cleanup_status = gr.Textbox(
                    label="🔧 시스템 상태",
                    lines=2,
                    interactive=False
                )
        
        # 사용법 안내
        gr.Markdown("""
        ---
        ### 📖 사용법:
        1. **검색어 입력**: 위 입력창에 찾고 싶은 음식을 입력하세요
        2. **검색 실행**: "🚀 검색 및 Object Detection 실행" 버튼을 클릭하세요
        3. **결과 확인**: 
           - 왼쪽 이미지: 원본 스크린샷
           - 오른쪽 이미지: Object Detection이 적용된 결과 (색깔별 바운딩 박스)
        4. **상세 분석**: 아래 리포트에서 감지된 요소들의 상세 정보 확인
        
        ### 🎨 Object Detection 색상 코드:
        - 🔴 **빨간색**: 버튼 (Button)
        - 🟢 **초록색**: 입력창 (Input)  
        - 🔵 **파란색**: 링크 (Link)
        - 🟡 **노란색**: 이미지 (Image)
        - 🟣 **보라색**: 기타 요소
        
        ### ⚠️ 주의사항:
        - 첫 실행 시 브라우저 초기화로 약간의 시간이 걸릴 수 있습니다
        - 네트워크 상태에 따라 로딩 시간이 달라질 수 있습니다
        """)
        
        # 이벤트 핸들러 연결
        search_btn.click(
            fn=sync_search_and_detect,
            inputs=[search_input],
            outputs=[status_output, original_image, detected_image, detection_report, page_content]
        )
        
        history_btn.click(
            fn=get_search_history,
            outputs=[search_history]
        )
        
        cleanup_btn.click(
            fn=cleanup_demo,
            outputs=[cleanup_status]
        )
        
        # Enter 키로도 검색 가능
        search_input.submit(
            fn=sync_search_and_detect,
            inputs=[search_input],
            outputs=[status_output, original_image, detected_image, detection_report, page_content]
        )
    
    return demo

if __name__ == "__main__":
    print("🚀 인터랙티브 Uber Eats 검색 & Object Detection 데모 시작")
    print("=" * 60)
    
    # Gradio 인터페이스 생성 및 실행
    demo = create_interface()
    
    print("🌐 웹 인터페이스를 시작합니다...")
    print("📱 브라우저에서 http://localhost:7860 으로 접속하세요")
    print("=" * 60)
    
    # 공개 링크 생성 (선택사항)
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,  # 공개 링크 생성
        debug=True,
        show_error=True
    ) 