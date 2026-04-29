/**
 * Season Tarot 경량 i18n
 * - window.__lang: 현재 언어 코드 (ko/en/ja/zh)
 * - window.__t(key, fallback?): 번역 텍스트 반환
 * - window.__setLang(lang): 언어 변경 + 'lang:change' 이벤트 디스패치
 * - localStorage 'season-tarot-lang' 키에 영구 저장
 */
(function () {
    'use strict';

    var DICT = {
        ko: {
            'lang.ko': '한국어',
            'lang.en': 'English',
            'lang.ja': '日本語',
            'lang.zh': '中文',

            'app.brand': 'SeasonTarot',
            'app.tagline': 'AI 타로 운세',

            'nav.login': '로그인',
            'nav.profile': '프로필',
            'nav.diary': '다이어리',
            'nav.logout': '로그아웃',
            'nav.lang.label': '언어',

            'home.title': '오늘의 운세를 확인하세요',
            'home.subtitle': 'AI가 타로 카드를 통해 당신에게 메시지를 전합니다',
            'home.daily': '일일 타로',
            'home.season': '시즌 타로',
            'home.yearly': '연간 타로',
            'home.monthly': '월간 타로',
            'home.aichat': 'AI 타로 리더',
            'home.history': '내 기록',
            'home.daily.desc': '오늘 하루의 흐름',
            'home.season.desc': '사랑·재물·건강 3장 카드',
            'home.yearly.desc': '봄·여름·가을·겨울 4분기',
            'home.monthly.desc': '이번 달의 운세',
            'home.aichat.desc': '루카리오와 1:1 상담',
            'home.history.desc': '캘린더·통계·다시보기',
            'home.start': '시작하기',

            'login.title': '로그인',
            'login.email': '이메일',
            'login.password': '비밀번호',
            'login.submit': '로그인',
            'login.signup': '회원가입',
            'login.forgot': '비밀번호 찾기',
            'login.name': '이름',
            'login.signup.submit': '가입하기',
            'login.signup.back': '로그인으로 돌아가기',

            'common.loading': '로딩 중...',
            'common.confirm': '확인',
            'common.cancel': '취소',
            'common.save': '저장',
            'common.delete': '삭제',
            'common.back': '뒤로',
            'common.next': '다음',
            'common.error': '오류가 발생했습니다',

            'tarot.shuffle': '카드를 섞는 중',
            'tarot.pick': '카드를 선택하세요',
            'tarot.result': '결과',
            'tarot.ask': '추가 질문',
            'tarot.again': '다시 뽑기',
            'tarot.name.placeholder': '이름을 입력하세요',
            'tarot.concern.placeholder': '고민을 입력하세요',

            'profile.title': '내 프로필',
            'profile.history': '타로 기록',
            'profile.calendar': '캘린더',
            'profile.stats': '통계',

            'main.badge': 'AI TAROT',
            'main.desc1': '당신의 운명을 AI가 해석해 드립니다',
            'main.desc2': '타로 카드를 통해 사랑, 직업, 미래를 확인하세요',
            'main.cta': 'AI 점 보기 시작',
            'main.menu.daily.title': '일일 타로 운세',
            'main.menu.daily.desc': '오늘 하루의 운세를 확인하세요',
            'main.menu.today.title': '오늘의 타로',
            'main.menu.today.desc': 'AI가 오늘의 카드를 해석합니다',
            'main.menu.season.title': 'Season 카드',
            'main.menu.season.desc': '과거·현재·미래 3장 스프레드',
            'main.menu.yearly.title': '연간 타로 운세',
            'main.menu.yearly.desc': '{year}년 사계절 운세를 확인하세요',
            'main.menu.monthly.title': '월간 타로 운세',
            'main.menu.monthly.desc': '이번 달의 운세를 확인하세요',
        },
        en: {
            'lang.ko': '한국어',
            'lang.en': 'English',
            'lang.ja': '日本語',
            'lang.zh': '中文',

            'app.brand': 'SeasonTarot',
            'app.tagline': 'AI Tarot Reading',

            'nav.login': 'Sign in',
            'nav.profile': 'Profile',
            'nav.diary': 'Diary',
            'nav.logout': 'Sign out',
            'nav.lang.label': 'Language',

            'home.title': "Check today's fortune",
            'home.subtitle': 'AI delivers a message through tarot cards',
            'home.daily': 'Daily Tarot',
            'home.season': 'Season Cards',
            'home.yearly': 'Yearly Tarot',
            'home.monthly': 'Monthly Tarot',
            'home.aichat': 'AI Tarot Reader',
            'home.history': 'My Records',
            'home.daily.desc': "Today's flow",
            'home.season.desc': 'Love · Wealth · Health (3 cards)',
            'home.yearly.desc': 'Spring · Summer · Autumn · Winter',
            'home.monthly.desc': "This month's reading",
            'home.aichat.desc': '1:1 chat with Lucario',
            'home.history.desc': 'Calendar · Stats · Replay',
            'home.start': 'Start',

            'login.title': 'Sign in',
            'login.email': 'Email',
            'login.password': 'Password',
            'login.submit': 'Sign in',
            'login.signup': 'Sign up',
            'login.forgot': 'Forgot password?',
            'login.name': 'Name',
            'login.signup.submit': 'Create account',
            'login.signup.back': 'Back to sign in',

            'common.loading': 'Loading...',
            'common.confirm': 'OK',
            'common.cancel': 'Cancel',
            'common.save': 'Save',
            'common.delete': 'Delete',
            'common.back': 'Back',
            'common.next': 'Next',
            'common.error': 'An error occurred',

            'tarot.shuffle': 'Shuffling cards',
            'tarot.pick': 'Pick a card',
            'tarot.result': 'Result',
            'tarot.ask': 'Ask more',
            'tarot.again': 'Draw again',
            'tarot.name.placeholder': 'Enter your name',
            'tarot.concern.placeholder': 'Enter your concern',

            'profile.title': 'My Profile',
            'profile.history': 'Tarot History',
            'profile.calendar': 'Calendar',
            'profile.stats': 'Statistics',

            'main.badge': 'AI TAROT',
            'main.desc1': 'AI interprets your destiny',
            'main.desc2': 'Discover love, career, and future through tarot cards',
            'main.cta': 'Start AI Reading',
            'main.menu.daily.title': 'Daily Tarot',
            'main.menu.daily.desc': "Check today's fortune",
            'main.menu.today.title': "Today's Tarot",
            'main.menu.today.desc': "AI interprets today's card",
            'main.menu.season.title': 'Season Cards',
            'main.menu.season.desc': 'Past · Present · Future spread',
            'main.menu.yearly.title': 'Yearly Tarot',
            'main.menu.yearly.desc': 'Four seasons of {year}',
            'main.menu.monthly.title': 'Monthly Tarot',
            'main.menu.monthly.desc': "This month's fortune",
        },
        ja: {
            'lang.ko': '한국어',
            'lang.en': 'English',
            'lang.ja': '日本語',
            'lang.zh': '中文',

            'app.brand': 'SeasonTarot',
            'app.tagline': 'AIタロット占い',

            'nav.login': 'ログイン',
            'nav.profile': 'プロフィール',
            'nav.diary': 'ダイアリー',
            'nav.logout': 'ログアウト',
            'nav.lang.label': '言語',

            'home.title': '今日の運勢を確認',
            'home.subtitle': 'AIがタロットカードを通してメッセージを伝えます',
            'home.daily': 'デイリータロット',
            'home.season': 'シーズンカード',
            'home.yearly': '年間タロット',
            'home.monthly': '月間タロット',
            'home.aichat': 'AIタロットリーダー',
            'home.history': '記録',
            'home.daily.desc': '今日の流れ',
            'home.season.desc': '愛・財・健康(3枚)',
            'home.yearly.desc': '春・夏・秋・冬',
            'home.monthly.desc': '今月の運勢',
            'home.aichat.desc': 'ルカリオと1対1相談',
            'home.history.desc': 'カレンダー・統計・再閲覧',
            'home.start': 'はじめる',

            'login.title': 'ログイン',
            'login.email': 'メール',
            'login.password': 'パスワード',
            'login.submit': 'ログイン',
            'login.signup': '会員登録',
            'login.forgot': 'パスワードをお忘れの方',
            'login.name': '名前',
            'login.signup.submit': '登録する',
            'login.signup.back': 'ログインに戻る',

            'common.loading': '読み込み中...',
            'common.confirm': '確認',
            'common.cancel': 'キャンセル',
            'common.save': '保存',
            'common.delete': '削除',
            'common.back': '戻る',
            'common.next': '次へ',
            'common.error': 'エラーが発生しました',

            'tarot.shuffle': 'カードをシャッフル中',
            'tarot.pick': 'カードを選択',
            'tarot.result': '結果',
            'tarot.ask': '追加の質問',
            'tarot.again': 'もう一度引く',
            'tarot.name.placeholder': 'お名前を入力',
            'tarot.concern.placeholder': 'お悩みを入力',

            'profile.title': 'プロフィール',
            'profile.history': 'タロット記録',
            'profile.calendar': 'カレンダー',
            'profile.stats': '統計',

            'main.badge': 'AI TAROT',
            'main.desc1': 'あなたの運命をAIが解釈します',
            'main.desc2': 'タロットカードを通して愛・仕事・未来を確認',
            'main.cta': 'AI占いを始める',
            'main.menu.daily.title': 'デイリータロット',
            'main.menu.daily.desc': '今日一日の運勢を確認',
            'main.menu.today.title': '今日のタロット',
            'main.menu.today.desc': 'AIが今日のカードを解釈',
            'main.menu.season.title': 'シーズンカード',
            'main.menu.season.desc': '過去・現在・未来 3枚スプレッド',
            'main.menu.yearly.title': '年間タロット',
            'main.menu.yearly.desc': '{year}年の四季の運勢',
            'main.menu.monthly.title': '月間タロット',
            'main.menu.monthly.desc': '今月の運勢',
        },
        zh: {
            'lang.ko': '한국어',
            'lang.en': 'English',
            'lang.ja': '日本語',
            'lang.zh': '中文',

            'app.brand': 'SeasonTarot',
            'app.tagline': 'AI 塔罗占卜',

            'nav.login': '登录',
            'nav.profile': '个人资料',
            'nav.diary': '日记',
            'nav.logout': '退出',
            'nav.lang.label': '语言',

            'home.title': '查看今日运势',
            'home.subtitle': 'AI 通过塔罗牌向您传递讯息',
            'home.daily': '每日塔罗',
            'home.season': '季节牌',
            'home.yearly': '年度塔罗',
            'home.monthly': '月度塔罗',
            'home.aichat': 'AI 塔罗师',
            'home.history': '我的记录',
            'home.daily.desc': '今天的走势',
            'home.season.desc': '爱情·财运·健康 (3 张)',
            'home.yearly.desc': '春·夏·秋·冬',
            'home.monthly.desc': '本月运势',
            'home.aichat.desc': '与路卡利欧一对一咨询',
            'home.history.desc': '日历·统计·回看',
            'home.start': '开始',

            'login.title': '登录',
            'login.email': '邮箱',
            'login.password': '密码',
            'login.submit': '登录',
            'login.signup': '注册',
            'login.forgot': '忘记密码',
            'login.name': '姓名',
            'login.signup.submit': '注册账号',
            'login.signup.back': '返回登录',

            'common.loading': '加载中...',
            'common.confirm': '确定',
            'common.cancel': '取消',
            'common.save': '保存',
            'common.delete': '删除',
            'common.back': '返回',
            'common.next': '下一步',
            'common.error': '发生错误',

            'tarot.shuffle': '正在洗牌',
            'tarot.pick': '请选择牌',
            'tarot.result': '结果',
            'tarot.ask': '继续提问',
            'tarot.again': '重新抽取',
            'tarot.name.placeholder': '请输入姓名',
            'tarot.concern.placeholder': '请输入您的烦恼',

            'profile.title': '我的资料',
            'profile.history': '塔罗记录',
            'profile.calendar': '日历',
            'profile.stats': '统计',

            'main.badge': 'AI TAROT',
            'main.desc1': 'AI 为您解读命运',
            'main.desc2': '通过塔罗牌洞察爱情·事业·未来',
            'main.cta': '开始 AI 占卜',
            'main.menu.daily.title': '每日塔罗',
            'main.menu.daily.desc': '查看今日运势',
            'main.menu.today.title': '今日塔罗',
            'main.menu.today.desc': 'AI 解读今日之牌',
            'main.menu.season.title': '季节牌',
            'main.menu.season.desc': '过去·现在·未来 三张展开',
            'main.menu.yearly.title': '年度塔罗',
            'main.menu.yearly.desc': '{year}年四季运势',
            'main.menu.monthly.title': '月度塔罗',
            'main.menu.monthly.desc': '本月运势',
        }
    };

    var SUPPORTED = ['ko', 'en', 'ja', 'zh'];
    var STORAGE_KEY = 'season-tarot-lang';

    function detectLang() {
        try {
            var saved = localStorage.getItem(STORAGE_KEY);
            if (saved && SUPPORTED.indexOf(saved) !== -1) return saved;
        } catch (e) { }
        var nav = (navigator.language || 'ko').toLowerCase();
        if (nav.indexOf('zh') === 0) return 'zh';
        if (nav.indexOf('ja') === 0) return 'ja';
        if (nav.indexOf('en') === 0) return 'en';
        return 'ko';
    }

    window.__lang = detectLang();
    document.documentElement.setAttribute('lang', window.__lang);

    window.__supportedLangs = SUPPORTED.slice();

    window.__t = function (key, fallback) {
        var d = DICT[window.__lang] || DICT.ko;
        if (key in d) return d[key];
        var k = DICT.ko;
        if (key in k) return k[key];
        return fallback != null ? fallback : key;
    };

    window.__setLang = function (lang) {
        if (SUPPORTED.indexOf(lang) === -1) return;
        if (lang === window.__lang) return;
        window.__lang = lang;
        try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) { }
        document.documentElement.setAttribute('lang', lang);
        // 쿠키로도 전송하여 백엔드(AI 프롬프트)가 인식 가능하게
        try {
            document.cookie = 'lang=' + lang + '; path=/; max-age=' + (60 * 60 * 24 * 365);
        } catch (e) { }
        window.dispatchEvent(new CustomEvent('lang:change', { detail: { lang: lang } }));
    };

    // 초기 쿠키 동기화
    try {
        document.cookie = 'lang=' + window.__lang + '; path=/; max-age=' + (60 * 60 * 24 * 365);
    } catch (e) { }
})();
