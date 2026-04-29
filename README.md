# 🔮 Season Tarot — AI 타로 웹서비스

> **Generative AI(Google Gemini) 기반의 대화형 타로 리딩 플랫폼.**
> 78장 풀덱 타로 카드 시뮬레이션과 AI 해석을 결합하여, 누구나 24시간 깊이 있는 타로 상담을 경험할 수 있는 무료 웹서비스입니다.

<p align="left">
  <img alt="Framework" src="https://img.shields.io/badge/framework-WIZ-6B46C1?style=flat-square">
  <img alt="Frontend" src="https://img.shields.io/badge/frontend-Angular-DD0031?style=flat-square&logo=angular&logoColor=white">
  <img alt="Backend" src="https://img.shields.io/badge/backend-Python%203-3776AB?style=flat-square&logo=python&logoColor=white">
  <img alt="AI" src="https://img.shields.io/badge/AI-Gemini%202.5%20Flash-FBBF24?style=flat-square&logo=google&logoColor=white">
  <img alt="Database" src="https://img.shields.io/badge/database-MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white">
</p>

---

## 📋 목차

1. [프로젝트 소개](#1-프로젝트-소개)
2. [핵심 기능](#2-핵심-기능)
3. [기술 스택](#3-기술-스택)
4. [시스템 아키텍처](#4-시스템-아키텍처)
5. [데이터베이스 스키마](#5-데이터베이스-스키마)
6. [프로젝트 구조](#6-프로젝트-구조)
7. [설치 및 실행](#7-설치-및-실행)
8. [주요 페이지 라우팅](#8-주요-페이지-라우팅)
9. [개발 성과 및 최적화 사례](#9-개발-성과-및-최적화-사례)
10. [개발 이력](#10-개발-이력)

---

## 1. 프로젝트 소개

### 배경

전통적인 타로 카드 해석은 해석자의 경험과 직관에 크게 의존합니다. 본 프로젝트는 **Generative AI를 활용해 24시간 일관된 품질의 타로 리딩**을 제공하고, 사용자가 자신의 운세 흐름을 데이터로 추적·분석할 수 있도록 설계된 웹서비스입니다.

### 차별점

| 항목 | 내용 |
|------|------|
| **5종 리딩 모드** | 일일 · 월간 · 연간 · 시즌 · AI 채팅 |
| **78장 풀덱 시뮬레이션** | 메이저 22 + 마이너 56장 모두 지원, 정·역방향 처리 |
| **AI 구조화 응답** | JSON Schema 기반의 일관된 해석(요약·조언·키워드 등) |
| **히스토리 통합** | 캘린더 · 통계 · 감정 태그 · 검색 필터 |
| **모바일 우선 UX** | 토스 스타일 반응형, Fan-Spread 카드 픽업 인터랙션 |

### 미리보기

- 🏠 홈 — 5종 리딩 모드 진입
- 🔮 일일/월간/연간/시즌 카드 — 카드 셔플 → Fan-Spread 선택 → AI 해석
- 💬 루카리오 AI 챗봇 — 멀티턴 대화형 타로 리딩
- 📅 프로필 — 타로 기록(캘린더/리스트/통계)

---

## 2. 핵심 기능

### 2.1 타로 리딩 (5종)

| 모드 | 페이지 | 특징 |
|------|--------|------|
| **일일 타로** | `/tarot` | 카드 1장으로 오늘의 운세, AI 구조화 해석 |
| **시즌 카드** | `/fourth` | 3장으로 사랑운·건강운·재물운 분석 |
| **연간 타로** | `/tarotw` | 4장으로 봄·여름·가을·겨울 운세, **단일 통합 호출 최적화** |
| **월간 타로** | `/monthly` | 이번 달 관심사 기반 카드 리딩 |
| **AI 타로 리더** | `/chat` | 루카리오 캐릭터와 1:1 멀티턴 채팅 상담 |

### 2.2 사용자 경험

- **카드 셔플 애니메이션** — 의식적 몰입감을 주는 셔플 모션
- **Fan-Spread 카드 피커** — 78장 카드를 부채꼴로 펼쳐 직관적 선택
- **카드 정/역방향(Reversed)** — 동일 카드라도 방향에 따라 해석 분기
- **카드 AI 상담** — 결과 페이지에서 뽑은 카드를 주제로 추가 질문(컨텍스트 유지)

### 2.3 회원 / 히스토리

- **세션 기반 인증** — 로그인 / 회원가입 / 비밀번호 찾기(이메일 검증)
- **타로 기록 DB 저장** — 카드 ID / 감정 태그 / AI 해석 자동 저장
- **히스토리 화면** — 리스트 · 캘린더 뷰 · 통계 · 필터 검색 · 상세 보기

### 2.4 디자인

- 보라색 그라디언트 + 골드 액센트의 **신비로운 일관 톤앤매너**
- **모바일 퍼스트** 반응형(토스 스타일) — 단일 컬럼 최적화

---

## 3. 기술 스택

### Frontend

| 기술 | 용도 |
|------|------|
| **Angular** (TypeScript) | SPA 프레임워크 |
| **Pug** | 간결한 HTML 템플릿 엔진 |
| **SCSS + Tailwind CSS** | 디자인 시스템 / 유틸리티 |
| **RxJS · Service DI** | 상태 관리 / 비동기 흐름 |

### Backend

| 기술 | 용도 |
|------|------|
| **Python 3** | 백엔드 런타임 |
| **WIZ Framework** | 풀스택 프레임워크 (Flask 내장) |
| **Peewee ORM** | MySQL 모델링 |
| **Socket.IO** | 실시간 채팅 통신 |

### AI / Data

| 기술 | 용도 |
|------|------|
| **Google Gemini 2.5 Flash** | 타로 해석 / 채팅 응답 |
| **Structured Prompt (JSON Schema)** | 응답 일관성 확보 |
| **MySQL** | 사용자 / 타로 히스토리 |

---

## 4. 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│  Client (Angular SPA)                                   │
│  ─ Page · Component · Service                           │
└────────────────────────────┬────────────────────────────┘
                             │ REST API · Socket.IO
┌────────────────────────────▼────────────────────────────┐
│  Controller Chain                                       │
│  ─ base.py (세션 초기화)                                │
│      └─ user.py (인증 검증)                             │
└────────────────────────────┬────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────┐
│  API Layer                                              │
│  ─ api.py (App-bound)  · route/ (REST endpoint)         │
└────────────────────────────┬────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────┐
│  Business Logic                                         │
│  ─ Struct (Aggregate Root · 도메인 캡슐화)              │
└────────────────────────────┬────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────┐
│  Data Layer                                             │
│  ─ Peewee ORM (MySQL)   · Gemini API (HTTP)             │
└─────────────────────────────────────────────────────────┘
```

### Request Flow

1. 사용자가 카드 선택 → Angular Service → `wiz.call()`
2. **Controller**가 인증 / 세션 검증
3. **api.py**가 요청 라우팅
4. **Struct → ORM**으로 사용자 / 카드 데이터 조회
5. **Gemini API**로 AI 해석 호출 (구조화 JSON 응답)
6. 해석 결과를 화면에 렌더링 + 히스토리 DB 저장

---

## 5. 데이터베이스 스키마

| 테이블 | 설명 | 주요 필드 |
|--------|------|-----------|
| `login` | 회원 정보 | id, email, password(hash), name, role, created |
| `tarot` | 일일 타로 기록 | id, user_id, card_id, reversed, ai_result, mood_tags, created |
| `tarotp` | 월간 타로 기록 | id, user_id, theme, card_id, ai_result, created |
| `tarott` | 연간 타로 기록 | id, user_id, year, card_ids, ai_result, mood_tags, created |

---

## 6. 프로젝트 구조

```
project/main/
├── config/                       # 환경 설정 (database, season 등)
├── src/
│   ├── app/                      # Angular Apps
│   │   ├── page.home/            # 홈 (서비스 진입)
│   │   ├── page.login/           # 로그인 / 회원가입 / PW 찾기
│   │   ├── page.page.tarot/      # 일일 타로
│   │   ├── page.fourth/          # 시즌 카드 (3장)
│   │   ├── page.page.tarotw/     # 연간 타로 (4장)
│   │   ├── page.monthly/         # 월간 타로
│   │   ├── page.fifth/           # 오늘의 타로
│   │   ├── page.second/          # AI 타로 리더 선택
│   │   ├── page.chat/            # 루카리오 AI 채팅
│   │   ├── page.profile/         # 프로필 / 히스토리
│   │   ├── component.card/       # 카드 표시
│   │   ├── component.chat/       # AI 채팅 (78장 피커)
│   │   ├── component.card.chat/  # 카드 AI 상담
│   │   ├── component.related/    # 추천 섹션
│   │   ├── layout.navbar/        # 메인 레이아웃
│   │   └── layout.empty/         # 풀스크린 레이아웃
│   ├── controller/               # 인증 체인 (base / user / member)
│   ├── model/
│   │   └── db/                   # Peewee 테이블 (login, tarot, tarotp, tarott)
│   ├── route/                    # REST 엔드포인트 (auth.login, test)
│   ├── portal/season/            # 공통 패키지 (Service · Auth · UI)
│   └── assets/                   # 78장 타로 카드 이미지
├── devlog/                       # 일자별 개발 로그
├── portfolio/                    # 포트폴리오 PPT + 빌드 스크립트
└── README.md
```

---

## 7. 설치 및 실행

### 사전 준비

- WIZ Framework 환경
- MySQL 8.x
- Google AI Studio API Key

### 환경 변수

```bash
export GEMINI_API_KEY="your-google-ai-api-key"
```

### DB 설정

`config/database.py`에 namespace별 접속 정보를 등록한 뒤, `src/model/db/`의 테이블 스키마에 맞춰 마이그레이션 합니다.

### 빌드 & 실행

```bash
# WIZ MCP 또는 CLI에서
wiz_project_build              # Angular + Python 빌드
wiz service restart            # 서버 재시작 (필요 시)
```

> 코드 변경 시 hot-reload로 자동 반영되며, `socket.py` 추가/수정 또는 새 API 함수 추가 시에만 클린 빌드 + 서비스 재시작이 필요합니다.

---

## 8. 주요 페이지 라우팅

| 경로 | 페이지 | 인증 |
|------|--------|------|
| `/` | 홈 | 공개 |
| `/login` | 로그인 / 회원가입 | 공개 |
| `/tarot` | 일일 타로 | 로그인 |
| `/fourth` | 시즌 카드 (3장) | 로그인 |
| `/tarotw` | 연간 타로 (4장) | 로그인 |
| `/monthly` | 월간 타로 | 로그인 |
| `/fifth` | 오늘의 타로 | 로그인 |
| `/second` | AI 타로 리더 선택 | 로그인 |
| `/chat` | 루카리오 AI 채팅 | 로그인 |
| `/profile` | 프로필 / 히스토리 | 로그인 |

---

## 9. 개발 성과 및 최적화 사례

### 9.1 AI 호출 4회 → 1회 통합 (75% 속도 개선)

연간 타로는 **봄/여름/가을/겨울** 4분기를 분석합니다. 초기 구현은 분기별로 Gemini API를 4회 호출하여 평균 **약 28초**가 소요되었습니다.

- ✅ **단일 통합 프롬프트**로 4분기를 동시 분석하도록 재설계
- ✅ JSON Schema에 분기 키를 명시하여 구조 일관성 확보
- ✅ 평균 응답 시간 **28s → 7s (약 75% 단축)**, 토큰 비용도 함께 절감

### 9.2 카드 이름↔이미지 매핑 통일

- **문제**: DB 동적 매핑 + 다국어 표기 혼재로 카드 이미지 누락 / 500 에러 발생
- **해결**: 78장 정적 매핑 리스트로 단일화, 카드 ID 기준 통합

### 9.3 AI 응답 파싱 안정화

- **문제**: Gemini 자유 응답에서 키 이름이 흔들려 화면 공백 발생
- **해결**: JSON Schema 강제 + fallback 키 매핑 + 타임아웃·재시도 처리

### 9.4 Controller 캐시 우회

- **문제**: 인증 컨트롤러 변경이 hot-reload에 반영되지 않는 케이스
- **해결**: `member.py`로 분리하여 캐시 우회 + 클린 빌드 절차 정립

### 9.5 모바일 UX 최적화

- 토스 스타일 단일 컬럼 레이아웃, 네비게이션 심플화
- 카드 Fan-Spread 인터랙션 (78장에서도 부드러운 픽업)
- 셔플 애니메이션과 순차 펼치기로 의식적 몰입감 부여

---

## 10. 개발 이력

전체 작업 이력은 [`devlog.md`](devlog.md)에 일자별로 정리되어 있습니다. 한 작업 단위마다 상세 파일(`devlog/{YYYY-MM-DD}/{NNN}-{slug}.md`)이 함께 관리됩니다.

| 카테고리 | 주요 작업 |
|----------|-----------|
| **기능 추가** | 5종 타로 리딩, AI 채팅, 히스토리 캘린더/통계, 감정 태그 |
| **성능 개선** | AI 호출 통합(4→1), 카드 매핑 정적화, 응답 파싱 강화 |
| **UX 개선** | Fan-Spread, 셔플/펼치기 애니메이션, 모바일 반응형 |
| **버그 수정** | 결과 미표시, API 500, Reversed 표시, 회원가입 응답 형식 |
| **인프라** | 세션 인증, Controller 체인, DB 스키마 확장 |

---

## 📂 포트폴리오

본 프로젝트의 종합 포트폴리오 PPT는 [`portfolio/AI_Tarot_Portfolio.pptx`](portfolio/AI_Tarot_Portfolio.pptx)에 있습니다.
빌드 스크립트([`portfolio/build_ppt.py`](portfolio/build_ppt.py))로 디자인·내용 수정 후 재생성이 가능합니다.

---

## 📝 라이선스 / 저작권

- 본 프로젝트는 학습 / 포트폴리오 목적으로 제작되었습니다.
- 타로 카드 이미지는 퍼블릭 도메인 자산을 사용했습니다.
- AI 응답은 Google Gemini API의 응답을 기반으로 하며, 실제 점술 행위를 대체하지 않습니다.

---

<p align="center">
  <b>Made with 🔮 + 🤖</b><br>
  <sub>Tarot × Generative AI · 2026</sub>
</p>
