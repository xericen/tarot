# 🔮 Season Tarot

무료 AI 타로 운세 서비스

## 주요 기능

- **일일 타로** — 매일 카드 한 장으로 오늘의 운세 확인
- **오늘의 타로** — 이름 입력 후 카드 선택, AI 해석 제공
- **시즌 카드** — 3장 카드로 사랑운·건강운·재물운 분석
- **연간 타로** — 4장 카드로 봄·여름·가을·겨울 운세
- **월간 타로** — 이번 달 관심사별 카드 리딩
- **AI 타로 리더** — 루카리오와 1:1 채팅 타로 상담 (78장 카드 피커)
- **카드 AI 상담** — 결과 페이지에서 뽑은 카드에 대해 추가 질문

## 기술 스택

| 영역 | 기술 |
|------|------|
| 프레임워크 | WIZ Framework |
| 프론트엔드 | Angular, Pug, SCSS, Tailwind CSS |
| 백엔드 | Python (WIZ exec 환경) |
| AI | Google Gemini 2.5 Flash |
| DB | MySQL (Peewee ORM) |

## 환경 변수

```bash
export GEMINI_API_KEY="your-google-ai-api-key"
```

## 프로젝트 구조

```
src/
├── app/
│   ├── page.login/          # 로그인/회원가입/비밀번호 찾기
│   ├── page.page.tarot/     # 일일 타로
│   ├── page.fifth/          # 오늘의 타로
│   ├── page.fourth/         # 시즌 카드 (3장)
│   ├── page.page.tarotw/    # 연간 타로 (4장)
│   ├── page.monthly/        # 월간 타로
│   ├── page.second/         # AI 타로 리더 선택
│   ├── page.third/          # 루카리오 채팅
│   ├── page.profile/        # 프로필 / 타로 기록
│   ├── component.chat/      # AI 채팅 컴포넌트 (78장 피커)
│   ├── component.card.chat/  # 카드 AI 상담 컴포넌트
│   ├── component.card/       # 카드 표시 컴포넌트
│   └── component.related/    # 추천 섹션
├── model/                    # DB 모델
└── assets/                   # 타로 카드 이미지 (78장)
```
