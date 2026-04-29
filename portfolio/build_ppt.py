"""
AI 타로 웹서비스 포트폴리오 PPT 생성 스크립트
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import os

# ===== 디자인 토큰 =====
PURPLE_DARK = RGBColor(0x2A, 0x1B, 0x4E)   # 배경
PURPLE_MID = RGBColor(0x6B, 0x46, 0xC1)    # 포인트
PURPLE_LIGHT = RGBColor(0xC4, 0xB5, 0xFD)  # 강조
GOLD = RGBColor(0xFB, 0xBF, 0x24)          # 액센트
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY_LIGHT = RGBColor(0xE5, 0xE7, 0xEB)
GRAY = RGBColor(0x9C, 0xA3, 0xAF)
BG_CARD = RGBColor(0x3B, 0x2A, 0x6B)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height


def add_bg(slide, color=PURPLE_DARK):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    bg.line.fill.background()
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.shadow.inherit = False
    return bg


def add_text(slide, text, left, top, width, height,
             size=18, bold=False, color=WHITE, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, font="Pretendard"):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Emu(0)
    tf.margin_top = tf.margin_bottom = Emu(0)
    tf.vertical_anchor = anchor
    lines = text.split("\n") if isinstance(text, str) else text
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = line
        run.font.name = font
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
    return tb


def add_rect(slide, left, top, width, height, fill=BG_CARD, line=None, radius=False):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
        left, top, width, height,
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(1)
    shape.shadow.inherit = False
    return shape


def add_accent_bar(slide, left, top, width=Inches(0.08), height=Inches(0.5), color=GOLD):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    bar.shadow.inherit = False
    return bar


def add_footer(slide, page_num, total):
    add_text(slide, "AI Tarot Web Service · Portfolio",
             Inches(0.5), Inches(7.05), Inches(8), Inches(0.3),
             size=10, color=GRAY)
    add_text(slide, f"{page_num} / {total}",
             Inches(11.5), Inches(7.05), Inches(1.5), Inches(0.3),
             size=10, color=GRAY, align=PP_ALIGN.RIGHT)


def add_title_block(slide, kicker, title):
    add_accent_bar(slide, Inches(0.5), Inches(0.55))
    add_text(slide, kicker, Inches(0.7), Inches(0.5),
             Inches(8), Inches(0.35), size=12, bold=True, color=GOLD)
    add_text(slide, title, Inches(0.7), Inches(0.85),
             Inches(12), Inches(0.7), size=28, bold=True, color=WHITE)
    # divider
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                  Inches(0.7), Inches(1.55),
                                  Inches(12), Emu(8000))
    line.fill.solid()
    line.fill.fore_color.rgb = PURPLE_MID
    line.line.fill.background()


TOTAL_PAGES = 12  # 추후 갱신


# ===== 슬라이드 1: 표지 =====
def slide_cover():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(s, PURPLE_DARK)
    # 좌측 데코 카드
    for i, off in enumerate([0.3, 0.6, 0.9]):
        c = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                               Inches(0.5 + off), Inches(1.8 + off * 0.3),
                               Inches(1.6), Inches(2.4))
        c.fill.solid()
        c.fill.fore_color.rgb = [PURPLE_MID, PURPLE_LIGHT, GOLD][i]
        c.line.color.rgb = WHITE
        c.line.width = Pt(1.5)
        c.rotation = -15 + i * 10
        c.shadow.inherit = False

    add_text(s, "PORTFOLIO · 2026",
             Inches(5.2), Inches(1.6), Inches(8), Inches(0.4),
             size=14, bold=True, color=GOLD)
    add_text(s, "AI 타로 웹서비스",
             Inches(5.2), Inches(2.1), Inches(8), Inches(1.0),
             size=44, bold=True, color=WHITE)
    add_text(s, "Tarot × Generative AI",
             Inches(5.2), Inches(3.1), Inches(8), Inches(0.6),
             size=22, bold=False, color=PURPLE_LIGHT)

    add_rect(s, Inches(5.2), Inches(4.0), Inches(7.5), Inches(2.0),
             fill=BG_CARD, radius=True)
    add_text(s,
             "Gemini AI 기반 대화형 타로 리딩 플랫폼\n"
             "WIZ Framework · Angular · Python · MySQL",
             Inches(5.5), Inches(4.2), Inches(7), Inches(1.6),
             size=16, color=GRAY_LIGHT)
    add_text(s,
             "일일 · 월간 · 연간 · 시즌 · AI 채팅 5종 리딩 모드",
             Inches(5.5), Inches(5.3), Inches(7), Inches(0.6),
             size=14, bold=True, color=GOLD)

    add_text(s, "2026.04 · Personal Project",
             Inches(0.5), Inches(7.0), Inches(8), Inches(0.3),
             size=11, color=GRAY)


# ===== 슬라이드 2: 목차 =====
def slide_agenda():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(s)
    add_title_block(s, "CONTENTS", "목차")
    items = [
        ("01", "프로젝트 개요", "서비스 소개와 핵심 가치"),
        ("02", "주요 기능", "5종 타로 리딩 + AI 채팅"),
        ("03", "기술 스택", "Frontend / Backend / AI / DB"),
        ("04", "시스템 아키텍처", "계층 구조와 데이터 흐름"),
        ("05", "AI 통합", "Gemini API 활용 전략"),
        ("06", "UX / UI 하이라이트", "Fan-spread · 셔플 애니메이션"),
        ("07", "성능 최적화", "AI 호출 4회 → 1회 통합"),
        ("08", "개발 성과 & 회고", "수치와 배운 점"),
    ]
    for i, (num, title, desc) in enumerate(items):
        col = i % 2
        row = i // 2
        x = Inches(0.7 + col * 6.2)
        y = Inches(1.9 + row * 1.25)
        add_rect(s, x, y, Inches(5.9), Inches(1.05), fill=BG_CARD, radius=True)
        add_text(s, num, x + Inches(0.3), y + Inches(0.2),
                 Inches(0.9), Inches(0.7), size=24, bold=True, color=GOLD)
        add_text(s, title, x + Inches(1.2), y + Inches(0.15),
                 Inches(4.5), Inches(0.4), size=15, bold=True, color=WHITE)
        add_text(s, desc, x + Inches(1.2), y + Inches(0.55),
                 Inches(4.5), Inches(0.4), size=11, color=GRAY_LIGHT)
    add_footer(s, 2, TOTAL_PAGES)


# ===== 슬라이드 3: 프로젝트 개요 =====
def slide_overview():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(s)
    add_title_block(s, "01 · OVERVIEW", "프로젝트 개요")

    add_rect(s, Inches(0.7), Inches(1.9), Inches(7.5), Inches(4.8),
             fill=BG_CARD, radius=True)
    add_text(s, "Why Tarot + AI?", Inches(1.0), Inches(2.1),
             Inches(7), Inches(0.5), size=18, bold=True, color=GOLD)
    add_text(s,
             "전통적인 타로 카드 해석은 해석자의 경험과 직관에 의존합니다.\n"
             "Generative AI를 도입하여 누구나 24시간 깊이 있는 타로 리딩을\n"
             "경험할 수 있는 대화형 웹서비스를 구축했습니다.",
             Inches(1.0), Inches(2.65), Inches(7), Inches(1.5),
             size=13, color=GRAY_LIGHT)

    add_text(s, "Key Differentiator", Inches(1.0), Inches(4.0),
             Inches(7), Inches(0.5), size=18, bold=True, color=GOLD)
    bullets = [
        "·  5종 리딩 모드 (일일·월간·연간·시즌·AI 채팅)",
        "·  Gemini AI 기반 구조화된 운세 해석",
        "·  카드 정/역방향 + 78장 풀덱 시뮬레이션",
        "·  히스토리 / 캘린더 / 통계 / 감정 태그 통합",
    ]
    for i, b in enumerate(bullets):
        add_text(s, b, Inches(1.0), Inches(4.55 + i * 0.45),
                 Inches(7), Inches(0.4), size=13, color=WHITE)

    # 우측 KPI 박스
    kpis = [
        ("5", "리딩 모드", PURPLE_LIGHT),
        ("78", "타로 카드", GOLD),
        ("60+", "Devlog 기록", PURPLE_LIGHT),
        ("1개월", "개발 기간", GOLD),
    ]
    for i, (num, label, color) in enumerate(kpis):
        col = i % 2
        row = i // 2
        x = Inches(8.5 + col * 2.2)
        y = Inches(1.9 + row * 2.5)
        add_rect(s, x, y, Inches(2.0), Inches(2.3), fill=PURPLE_MID, radius=True)
        add_text(s, num, x, y + Inches(0.4), Inches(2.0), Inches(1.0),
                 size=42, bold=True, color=color, align=PP_ALIGN.CENTER)
        add_text(s, label, x, y + Inches(1.5), Inches(2.0), Inches(0.5),
                 size=13, color=WHITE, align=PP_ALIGN.CENTER)

    add_footer(s, 3, TOTAL_PAGES)


# ===== 슬라이드 4: 주요 기능 =====
def slide_features():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(s)
    add_title_block(s, "02 · FEATURES", "주요 기능")

    features = [
        ("일일 타로", "오늘의 운세 카드 1장 + AI 구조화 해석", GOLD),
        ("월간 타로", "이번 달 흐름과 조언 카드 분석", PURPLE_LIGHT),
        ("연간 타로", "분기별 4장 카드로 한 해 운세 통합 분석", GOLD),
        ("시즌 타로", "사용자 고민 기반 맞춤 카드 리딩", PURPLE_LIGHT),
        ("AI 채팅", "루카리오 캐릭터와 대화형 타로 상담", GOLD),
        ("히스토리", "캘린더·통계·감정 태그·검색 필터", PURPLE_LIGHT),
    ]
    for i, (title, desc, color) in enumerate(features):
        col = i % 3
        row = i // 3
        x = Inches(0.7 + col * 4.2)
        y = Inches(2.0 + row * 2.5)
        add_rect(s, x, y, Inches(4.0), Inches(2.3), fill=BG_CARD, radius=True)
        add_accent_bar(s, x + Inches(0.3), y + Inches(0.35),
                       width=Inches(0.5), height=Inches(0.08), color=color)
        add_text(s, title, x + Inches(0.3), y + Inches(0.55),
                 Inches(3.5), Inches(0.5), size=18, bold=True, color=WHITE)
        add_text(s, desc, x + Inches(0.3), y + Inches(1.1),
                 Inches(3.5), Inches(1.1), size=12, color=GRAY_LIGHT)

    add_footer(s, 4, TOTAL_PAGES)


# ===== 슬라이드 5: 기술 스택 =====
def slide_stack():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(s)
    add_title_block(s, "03 · TECH STACK", "기술 스택")

    cols = [
        ("Frontend", PURPLE_LIGHT, [
            "Angular (TypeScript)",
            "Pug Template Engine",
            "SCSS · Tailwind utility",
            "RxJS · Service DI",
            "Reactive Forms",
        ]),
        ("Backend", GOLD, [
            "Python 3 · WIZ Framework",
            "Flask (내장)",
            "Peewee ORM",
            "REST API + Socket.IO",
            "Session 인증",
        ]),
        ("AI / Data", PURPLE_LIGHT, [
            "Google Gemini API",
            "Structured JSON Prompt",
            "Streaming Chat (SSE)",
            "MySQL (tarot_history)",
            "78-card 정적 매핑",
        ]),
        ("Infra / Tool", GOLD, [
            "WIZ MCP Tools",
            "Git · Devlog 관리",
            "Mobile-first 반응형",
            "Hot-reload 개발",
            "Build pipeline",
        ]),
    ]
    for i, (title, color, items) in enumerate(cols):
        x = Inches(0.7 + i * 3.1)
        y = Inches(1.9)
        add_rect(s, x, y, Inches(2.95), Inches(5.0), fill=BG_CARD, radius=True)
        add_accent_bar(s, x + Inches(0.25), y + Inches(0.35),
                       width=Inches(0.4), height=Inches(0.07), color=color)
        add_text(s, title, x + Inches(0.25), y + Inches(0.55),
                 Inches(2.6), Inches(0.5), size=17, bold=True, color=WHITE)
        for j, it in enumerate(items):
            add_text(s, "·  " + it, x + Inches(0.25), y + Inches(1.2 + j * 0.55),
                     Inches(2.6), Inches(0.5), size=12, color=GRAY_LIGHT)

    add_footer(s, 5, TOTAL_PAGES)


# ===== 슬라이드 6: 아키텍처 =====
def slide_architecture():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(s)
    add_title_block(s, "04 · ARCHITECTURE", "시스템 아키텍처")

    layers = [
        ("Client (Angular)", "Page · Component · Service", PURPLE_LIGHT),
        ("Controller", "base → user 인증 체인", GOLD),
        ("API Layer", "api.py · route · Socket.IO", PURPLE_LIGHT),
        ("Business Logic", "Struct · Aggregate Root", GOLD),
        ("Data Layer", "Peewee ORM · MySQL · Gemini API", PURPLE_LIGHT),
    ]
    top = Inches(2.0)
    for i, (name, desc, color) in enumerate(layers):
        y = top + Inches(i * 0.95)
        add_rect(s, Inches(0.9), y, Inches(7.5), Inches(0.8),
                 fill=BG_CARD, radius=True)
        add_accent_bar(s, Inches(1.1), y + Inches(0.15),
                       width=Inches(0.08), height=Inches(0.5), color=color)
        add_text(s, name, Inches(1.4), y + Inches(0.1),
                 Inches(3), Inches(0.6), size=15, bold=True, color=WHITE)
        add_text(s, desc, Inches(4.4), y + Inches(0.18),
                 Inches(4), Inches(0.5), size=12, color=GRAY_LIGHT)
        if i < len(layers) - 1:
            arrow = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW,
                                       Inches(4.45), y + Inches(0.78),
                                       Inches(0.4), Inches(0.18))
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = GOLD
            arrow.line.fill.background()

    # 우측: 요청 흐름
    add_rect(s, Inches(8.8), Inches(2.0), Inches(4.0), Inches(4.55),
             fill=PURPLE_MID, radius=True)
    add_text(s, "Request Flow", Inches(9.0), Inches(2.15),
             Inches(3.5), Inches(0.4), size=14, bold=True, color=GOLD)
    flow = [
        "1. 사용자 요청 (Angular)",
        "2. Controller 인증 검증",
        "3. api.py 함수 라우팅",
        "4. Struct → ORM 호출",
        "5. Gemini API 호출",
        "6. JSON 구조화 응답",
        "7. UI 렌더링 + 히스토리 저장",
    ]
    for i, f in enumerate(flow):
        add_text(s, f, Inches(9.0), Inches(2.7 + i * 0.5),
                 Inches(3.7), Inches(0.4), size=11, color=WHITE)

    add_footer(s, 6, TOTAL_PAGES)


# ===== 슬라이드 7: AI 통합 =====
def slide_ai():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(s)
    add_title_block(s, "05 · AI INTEGRATION", "Gemini AI 통합 전략")

    add_rect(s, Inches(0.7), Inches(1.9), Inches(6), Inches(4.9),
             fill=BG_CARD, radius=True)
    add_text(s, "Prompt Engineering", Inches(1.0), Inches(2.1),
             Inches(5.5), Inches(0.5), size=18, bold=True, color=GOLD)
    points = [
        "·  카드명 + 정/역방향 + 사용자 컨텍스트 주입",
        "·  JSON Schema 강제로 응답 구조화",
        "·  past / present / future / advice 4단 분리",
        "·  대화형 채팅: 시스템 페르소나 + 멀티턴",
    ]
    for i, p in enumerate(points):
        add_text(s, p, Inches(1.0), Inches(2.7 + i * 0.55),
                 Inches(5.5), Inches(0.5), size=13, color=WHITE)

    add_text(s, "Response Format", Inches(1.0), Inches(5.0),
             Inches(5.5), Inches(0.5), size=18, bold=True, color=GOLD)
    add_rect(s, Inches(1.0), Inches(5.55), Inches(5.5), Inches(1.15),
             fill=PURPLE_DARK, radius=True)
    code = ('{ "summary": "...",\n'
            '  "advice": "...",\n'
            '  "keywords": ["...", "..."] }')
    add_text(s, code, Inches(1.2), Inches(5.65),
             Inches(5.2), Inches(1.0), size=11, color=PURPLE_LIGHT,
             font="Consolas")

    # 우측: 최적화 비교
    add_rect(s, Inches(7.0), Inches(1.9), Inches(5.8), Inches(4.9),
             fill=BG_CARD, radius=True)
    add_text(s, "성능 최적화 사례", Inches(7.3), Inches(2.1),
             Inches(5.2), Inches(0.5), size=18, bold=True, color=GOLD)
    add_text(s, "연간 타로 AI 호출 통합", Inches(7.3), Inches(2.7),
             Inches(5.2), Inches(0.4), size=13, bold=True, color=WHITE)

    # Before
    add_rect(s, Inches(7.3), Inches(3.2), Inches(5.2), Inches(0.9),
             fill=RGBColor(0x7F, 0x1D, 0x1D), radius=True)
    add_text(s, "Before", Inches(7.5), Inches(3.3),
             Inches(1.5), Inches(0.3), size=11, bold=True, color=WHITE)
    add_text(s, "분기별 4회 API 호출 → ~28초",
             Inches(7.5), Inches(3.55), Inches(4.8), Inches(0.5),
             size=14, bold=True, color=WHITE)

    # After
    add_rect(s, Inches(7.3), Inches(4.3), Inches(5.2), Inches(0.9),
             fill=RGBColor(0x14, 0x5A, 0x32), radius=True)
    add_text(s, "After", Inches(7.5), Inches(4.4),
             Inches(1.5), Inches(0.3), size=11, bold=True, color=WHITE)
    add_text(s, "1회 통합 호출 → ~7초 (75% ↓)",
             Inches(7.5), Inches(4.65), Inches(4.8), Inches(0.5),
             size=14, bold=True, color=GOLD)

    add_text(s, "·  단일 프롬프트로 4분기 동시 분석\n"
                "·  토큰 사용량 절감 + UX 체감 속도 향상\n"
                "·  AI 응답 일관성도 함께 개선",
             Inches(7.3), Inches(5.4), Inches(5.2), Inches(1.4),
             size=12, color=GRAY_LIGHT)

    add_footer(s, 7, TOTAL_PAGES)


# ===== 슬라이드 8: UX/UI =====
def slide_ux():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(s)
    add_title_block(s, "06 · UX / UI", "사용자 경험 디자인")

    items = [
        ("Fan-Spread Picker",
         "78장 카드를 부채꼴로 펼쳐 직관적 선택\n"
         "Hover 애니메이션으로 카드 강조"),
        ("Shuffle Animation",
         "셔플 애니메이션으로 의식적 몰입감\n"
         "순차 펼치기로 자연스러운 흐름"),
        ("Mobile-First",
         "토스 스타일 반응형 디자인\n"
         "네비게이션 심플화 · 단일 컬럼 최적화"),
        ("Theme Identity",
         "보라색 그라디언트 + 골드 액센트\n"
         "신비로운 분위기의 일관된 톤앤매너"),
    ]
    for i, (title, desc) in enumerate(items):
        col = i % 2
        row = i // 2
        x = Inches(0.7 + col * 6.2)
        y = Inches(2.0 + row * 2.4)
        add_rect(s, x, y, Inches(5.9), Inches(2.2), fill=BG_CARD, radius=True)
        add_accent_bar(s, x + Inches(0.3), y + Inches(0.35),
                       width=Inches(0.5), height=Inches(0.08),
                       color=GOLD if i % 2 == 0 else PURPLE_LIGHT)
        add_text(s, title, x + Inches(0.3), y + Inches(0.55),
                 Inches(5.4), Inches(0.5), size=17, bold=True, color=WHITE)
        add_text(s, desc, x + Inches(0.3), y + Inches(1.15),
                 Inches(5.4), Inches(1.0), size=12, color=GRAY_LIGHT)

    add_footer(s, 8, TOTAL_PAGES)


# ===== 슬라이드 9: 트러블슈팅 =====
def slide_troubleshoot():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(s)
    add_title_block(s, "07 · TROUBLESHOOTING", "주요 트러블슈팅")

    cases = [
        ("AI 응답 미표시 버그",
         "JSON 파싱 실패로 결과 화면 공백",
         "응답 스키마 강제 + fallback 키 매핑으로 해결"),
        ("타로 API 500 에러",
         "카드명 ↔ 이미지 매핑 불일치",
         "DB 동적 매핑을 정적 리스트로 통일하여 안정화"),
        ("AI 호출 타임아웃",
         "분기별 4회 호출로 평균 28초 대기",
         "단일 프롬프트 통합 호출로 75% 속도 개선"),
        ("Controller 캐시 이슈",
         "인증 컨트롤러 변경이 반영되지 않음",
         "member.py로 분리하여 캐시 우회 + 클린 빌드"),
    ]
    for i, (title, problem, solution) in enumerate(cases):
        y = Inches(1.9 + i * 1.2)
        add_rect(s, Inches(0.7), y, Inches(12), Inches(1.05),
                 fill=BG_CARD, radius=True)
        add_text(s, title, Inches(1.0), y + Inches(0.15),
                 Inches(3.5), Inches(0.4), size=14, bold=True, color=GOLD)
        add_text(s, "Problem  " + problem,
                 Inches(4.6), y + Inches(0.13), Inches(8), Inches(0.4),
                 size=11, color=GRAY_LIGHT)
        add_text(s, "Solution  " + solution,
                 Inches(4.6), y + Inches(0.55), Inches(8), Inches(0.4),
                 size=11, bold=True, color=WHITE)

    add_footer(s, 9, TOTAL_PAGES)


# ===== 슬라이드 10: 성과 =====
def slide_results():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(s)
    add_title_block(s, "08 · RESULTS", "개발 성과")

    metrics = [
        ("75%", "AI 응답\n속도 개선", GOLD),
        ("19", "구현 페이지\n(Angular App)", PURPLE_LIGHT),
        ("60+", "Devlog\n작업 이력", GOLD),
        ("5", "타로 리딩\n모드", PURPLE_LIGHT),
        ("78", "타로 카드\n풀덱 지원", GOLD),
        ("100%", "모바일\n반응형", PURPLE_LIGHT),
    ]
    for i, (num, label, color) in enumerate(metrics):
        col = i % 3
        row = i // 3
        x = Inches(0.9 + col * 4.1)
        y = Inches(2.0 + row * 2.4)
        add_rect(s, x, y, Inches(3.85), Inches(2.2),
                 fill=BG_CARD, radius=True)
        add_text(s, num, x, y + Inches(0.35),
                 Inches(3.85), Inches(0.9),
                 size=44, bold=True, color=color, align=PP_ALIGN.CENTER)
        add_text(s, label, x, y + Inches(1.35),
                 Inches(3.85), Inches(0.8),
                 size=13, color=WHITE, align=PP_ALIGN.CENTER)

    add_footer(s, 10, TOTAL_PAGES)


# ===== 슬라이드 11: 회고 =====
def slide_retro():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(s)
    add_title_block(s, "09 · RETROSPECTIVE", "회고 & 배운 점")

    blocks = [
        ("Learned",
         GOLD,
         [
             "Generative AI 프로덕션 통합 노하우",
             "프롬프트 엔지니어링과 응답 구조화",
             "WIZ 프레임워크 풀스택 흐름",
             "Devlog 기반 체계적 작업 관리",
         ]),
        ("Improved",
         PURPLE_LIGHT,
         [
             "AI 호출 비용·속도 트레이드오프 인식",
             "모바일 우선 반응형 설계 역량",
             "ORM·세션·인증 체인 설계 패턴",
             "사용자 피드백 기반 빠른 이터레이션",
         ]),
        ("Next",
         GOLD,
         [
             "타로 해석 RAG 도입 (전문 서적 기반)",
             "유저 다이어리 + 감정 분석 연동",
             "PWA 설치형 모바일 앱 전환",
             "다국어(영문/일문) 확장",
         ]),
    ]
    for i, (title, color, items) in enumerate(blocks):
        x = Inches(0.7 + i * 4.1)
        add_rect(s, x, Inches(2.0), Inches(3.95), Inches(4.9),
                 fill=BG_CARD, radius=True)
        add_accent_bar(s, x + Inches(0.3), Inches(2.3),
                       width=Inches(0.4), height=Inches(0.07), color=color)
        add_text(s, title, x + Inches(0.3), Inches(2.5),
                 Inches(3.5), Inches(0.5), size=18, bold=True, color=WHITE)
        for j, it in enumerate(items):
            add_text(s, "·  " + it, x + Inches(0.3), Inches(3.2 + j * 0.7),
                     Inches(3.5), Inches(0.6), size=12, color=GRAY_LIGHT)

    add_footer(s, 11, TOTAL_PAGES)


# ===== 슬라이드 12: Thank You =====
def slide_thanks():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(s, PURPLE_DARK)

    # 중앙 카드 데코
    for i, off in enumerate([-2.0, 0.0, 2.0]):
        c = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                               Inches(5.5 + off), Inches(1.3),
                               Inches(1.8), Inches(2.6))
        c.fill.solid()
        c.fill.fore_color.rgb = [PURPLE_MID, GOLD, PURPLE_LIGHT][i]
        c.line.color.rgb = WHITE
        c.line.width = Pt(1.5)
        c.rotation = -10 + i * 10
        c.shadow.inherit = False

    add_text(s, "Thank You",
             Inches(0), Inches(4.4), SW, Inches(1.0),
             size=54, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, "AI 타로 웹서비스 · Portfolio 2026",
             Inches(0), Inches(5.5), SW, Inches(0.5),
             size=18, color=PURPLE_LIGHT, align=PP_ALIGN.CENTER)
    add_text(s, "Q & A",
             Inches(0), Inches(6.2), SW, Inches(0.5),
             size=20, bold=True, color=GOLD, align=PP_ALIGN.CENTER)


# ===== 빌드 =====
slide_cover()
slide_agenda()
slide_overview()
slide_features()
slide_stack()
slide_architecture()
slide_ai()
slide_ux()
slide_troubleshoot()
slide_results()
slide_retro()
slide_thanks()

out_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(out_dir, "AI_Tarot_Portfolio.pptx")
prs.save(out_path)
print(f"saved: {out_path}")
