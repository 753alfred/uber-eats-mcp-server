#!/usr/bin/env python3
"""
향상된 브라우저 자동화 시스템 - Object Detection 포함
사용자 텍스트 입력, 실시간 검색, 요소 감지 및 시각화
"""

import asyncio
import cv2
import numpy as np
from typing import List, Dict, Tuple, Optional
from playwright.async_api import async_playwright, Browser, Page, Locator
from PIL import Image, ImageDraw, ImageFont
import json
import base64
from io import BytesIO

class ObjectDetector:
    """페이지 요소 감지 및 시각화 클래스"""
    
    def __init__(self):
        self.colors = [
            (255, 0, 0),    # 빨강 - 버튼
            (0, 255, 0),    # 초록 - 입력창
            (0, 0, 255),    # 파랑 - 링크
            (255, 255, 0),  # 노랑 - 이미지
            (255, 0, 255),  # 마젠타 - 기타
        ]
        self.element_types = {
            'button': 0,
            'input': 1, 
            'a': 2,
            'img': 3,
            'other': 4
        }
    
    async def detect_elements(self, page: Page) -> List[Dict]:
        """페이지에서 상호작용 가능한 요소들을 감지"""
        elements = []
        
        # 다양한 종류의 요소들을 감지
        selectors = {
            'button': 'button, input[type="button"], input[type="submit"], [role="button"]',
            'input': 'input[type="text"], input[type="search"], input[type="email"], textarea',
            'link': 'a[href]',
            'image': 'img',
            'clickable': '[onclick], [data-testid*="button"], [data-testid*="click"]'
        }
        
        for element_type, selector in selectors.items():
            try:
                locators = await page.locator(selector).all()
                for i, locator in enumerate(locators):
                    try:
                        # 요소가 보이는지 확인
                        if await locator.is_visible():
                            bbox = await locator.bounding_box()
                            if bbox:
                                text = await locator.inner_text() if await locator.inner_text() else await locator.get_attribute('placeholder') or await locator.get_attribute('alt') or f"{element_type}_{i}"
                                
                                elements.append({
                                    'type': element_type,
                                    'text': text[:50],  # 텍스트 길이 제한
                                    'bbox': bbox,
                                    'selector': selector,
                                    'index': i
                                })
                    except:
                        continue
            except:
                continue
        
        return elements
    
    def draw_bounding_boxes(self, image_path: str, elements: List[Dict], output_path: str = None) -> str:
        """이미지에 바운딩 박스와 라벨을 그리기"""
        if output_path is None:
            output_path = image_path.replace('.png', '_detected.png')
        
        # 이미지 로드
        image = cv2.imread(image_path)
        if image is None:
            return image_path
        
        # PIL 이미지로 변환 (한글 폰트 지원)
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        
        try:
            # 한글 폰트 로드 시도
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
        except:
            # 기본 폰트 사용
            font = ImageFont.load_default()
        
        # 요소별로 바운딩 박스 그리기
        for element in elements:
            bbox = element['bbox']
            element_type = element['type']
            text = element['text']
            
            # 색상 선택
            color_idx = self.element_types.get(element_type, 4)
            color = self.colors[color_idx]
            
            # 바운딩 박스 좌표
            x1, y1 = int(bbox['x']), int(bbox['y'])
            x2, y2 = int(bbox['x'] + bbox['width']), int(bbox['y'] + bbox['height'])
            
            # 바운딩 박스 그리기
            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
            
            # 라벨 배경
            text_bbox = draw.textbbox((x1, y1-25), f"{element_type}: {text}", font=font)
            draw.rectangle([text_bbox[0]-2, text_bbox[1]-2, text_bbox[2]+2, text_bbox[3]+2], 
                          fill=color, outline=color)
            
            # 라벨 텍스트
            draw.text((x1, y1-25), f"{element_type}: {text}", fill=(255, 255, 255), font=font)
        
        # 저장
        final_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, final_image)
        
        return output_path

class EnhancedBrowserAgent:
    """향상된 브라우저 에이전트 - Object Detection 포함"""
    
    def __init__(self):
        self.browser: Browser = None
        self.page: Page = None
        self.playwright = None
        self.detector = ObjectDetector()
        self.search_history = []
    
    async def start_browser(self):
        """브라우저 시작"""
        print("🚀 향상된 브라우저 시작 중...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=False,
            args=[
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        self.page = await context.new_page()
        self.page.set_default_timeout(60000)
    
    async def close_browser(self):
        """브라우저 종료"""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def navigate_and_search(self, search_term: str) -> Dict:
        """사용자 입력 검색어로 네비게이션 및 검색 수행"""
        results = {
            'success': False,
            'search_term': search_term,
            'screenshot_path': None,
            'detected_elements': [],
            'detected_image_path': None,
            'page_content': '',
            'error': None
        }
        
        try:
            # Uber Eats로 이동
            print(f"🌐 Uber Eats 사이트로 이동 중...")
            await self.page.goto("https://www.ubereats.com/", wait_until='domcontentloaded', timeout=60000)
            print("✅ 페이지 로딩 완료")
            
            # 잠시 대기
            await asyncio.sleep(3)
            
            # 검색 수행
            print(f"🔍 '{search_term}' 검색 중...")
            search_success = await self.perform_search(search_term)
            
            # 스크린샷 촬영
            screenshot_path = f"search_{search_term.replace(' ', '_')}_screenshot.png"
            await self.page.screenshot(path=screenshot_path, full_page=False)
            results['screenshot_path'] = screenshot_path
            print(f"📸 스크린샷 저장: {screenshot_path}")
            
            # Object Detection 수행
            print("🔍 Object Detection 수행 중...")
            elements = await self.detector.detect_elements(self.page)
            results['detected_elements'] = elements
            
            # 바운딩 박스가 그려진 이미지 생성
            detected_image_path = self.detector.draw_bounding_boxes(
                screenshot_path, 
                elements, 
                f"search_{search_term.replace(' ', '_')}_detected.png"
            )
            results['detected_image_path'] = detected_image_path
            print(f"🎯 Object Detection 완료: {len(elements)}개 요소 감지")
            
            # 페이지 내용 추출
            content = await self.page.inner_text('body')
            results['page_content'] = content[:500]
            
            # 검색 기록 저장
            self.search_history.append({
                'search_term': search_term,
                'timestamp': asyncio.get_event_loop().time(),
                'elements_count': len(elements),
                'success': search_success
            })
            
            results['success'] = True
            print("✅ 검색 및 Object Detection 완료!")
            
        except Exception as e:
            results['error'] = str(e)
            print(f"❌ 오류 발생: {str(e)}")
        
        return results
    
    async def perform_search(self, search_term: str) -> bool:
        """실제 검색 수행"""
        try:
            # 다양한 검색창 셀렉터 시도
            selectors = [
                'input[type="text"]',
                'input[placeholder*="search"]',
                'input[aria-label*="search"]',
                'input[name="q"]',
                'input[data-testid*="search"]',
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
                await search_input.click()
                await search_input.fill(search_term)
                await search_input.press('Enter')
                await self.page.wait_for_load_state('networkidle', timeout=30000)
                print(f"✅ '{search_term}' 검색 완료")
                return True
            else:
                print("⚠️ 검색창을 찾을 수 없습니다")
                return False
                
        except Exception as e:
            print(f"⚠️ 검색 중 오류: {str(e)}")
            return False
    
    def get_search_history(self) -> List[Dict]:
        """검색 기록 반환"""
        return self.search_history
    
    def generate_detection_report(self, elements: List[Dict]) -> str:
        """감지된 요소들의 리포트 생성"""
        if not elements:
            return "감지된 요소가 없습니다."
        
        report = f"🎯 Object Detection 결과 (총 {len(elements)}개 요소)\n\n"
        
        # 타입별 요소 개수
        type_counts = {}
        for element in elements:
            element_type = element['type']
            type_counts[element_type] = type_counts.get(element_type, 0) + 1
        
        report += "📊 요소 타입별 개수:\n"
        for element_type, count in type_counts.items():
            report += f"  • {element_type}: {count}개\n"
        
        report += "\n📋 상세 요소 목록:\n"
        for i, element in enumerate(elements[:10]):  # 최대 10개만 표시
            report += f"{i+1}. [{element['type']}] {element['text']}\n"
        
        if len(elements) > 10:
            report += f"... 외 {len(elements) - 10}개 더\n"
        
        return report

# 전역 에이전트 인스턴스
global_agent = None

async def initialize_agent():
    """전역 에이전트 초기화"""
    global global_agent
    if global_agent is None:
        global_agent = EnhancedBrowserAgent()
        await global_agent.start_browser()
    return global_agent

async def cleanup_agent():
    """전역 에이전트 정리"""
    global global_agent
    if global_agent:
        await global_agent.close_browser()
        global_agent = None 