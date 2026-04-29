import { OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

declare const wiz: any;
declare const window: any;

const SENTIMENT_LABEL: any = {
    joy: { ko: '기쁨', en: 'Joy', ja: '喜び', zh: '喜悦', emoji: '😄', color: '#FFD166' },
    sad: { ko: '슬픔', en: 'Sad', ja: '悲しみ', zh: '悲伤', emoji: '😢', color: '#73A8FF' },
    angry: { ko: '분노', en: 'Angry', ja: '怒り', zh: '愤怒', emoji: '😠', color: '#EF476F' },
    anxious: { ko: '불안', en: 'Anxious', ja: '不安', zh: '焦虑', emoji: '😰', color: '#9D8BD9' },
    calm: { ko: '평온', en: 'Calm', ja: '穏やか', zh: '平静', emoji: '😌', color: '#7CDFCF' },
    excited: { ko: '설렘', en: 'Excited', ja: '興奮', zh: '兴奋', emoji: '🤩', color: '#FB8B24' },
    neutral: { ko: '중립', en: 'Neutral', ja: '中立', zh: '中性', emoji: '😐', color: '#A0A0B0' }
};

const MOOD_OPTIONS = [
    { key: 'happy', emoji: '😊' },
    { key: 'love', emoji: '🥰' },
    { key: 'tired', emoji: '😪' },
    { key: 'angry', emoji: '😡' },
    { key: 'sad', emoji: '😭' },
    { key: 'anxious', emoji: '😰' },
    { key: 'calm', emoji: '😌' },
    { key: 'excited', emoji: '🤩' }
];

export class Component implements OnInit, OnDestroy {
    constructor(public service: Service, private cdr: ChangeDetectorRef) { }

    public loaded = false;
    public mode: 'list' | 'write' | 'detail' = 'list';
    public items: any[] = [];
    public total = 0;
    public stats: any = { counts: {}, timeline: [], total: 0 };

    // write/edit 폼
    public form: any = { diary_id: '', diary_date: '', title: '', content: '', mood: '', related_draw_id: '' };
    public moodOptions = MOOD_OPTIONS;
    public recentTarots: any[] = [];
    public detailItem: any = null;
    public saving = false;

    private langChangeHandler: any;

    public t(key: string, fallback?: string, vars?: any): string {
        const w: any = window;
        return w.__t ? w.__t(key, fallback, vars) : (fallback || key);
    }

    public sentimentLabel(code: string): string {
        const lang = window.__getLang ? window.__getLang() : 'ko';
        const e = SENTIMENT_LABEL[code];
        if (!e) return code || '';
        return `${e.emoji} ${e[lang] || e.ko}`;
    }

    public sentimentColor(code: string): string {
        const e = SENTIMENT_LABEL[code];
        return e ? e.color : '#999';
    }

    public scoreToWidth(score: number): string {
        // -1.0~1.0 → 0~100%
        const v = Math.max(-1, Math.min(1, score || 0));
        return ((v + 1) / 2 * 100).toFixed(1) + '%';
    }

    public async ngOnInit() {
        await this.service.init();
        this.langChangeHandler = () => { this.cdr.detectChanges(); };
        window.addEventListener('lang:change', this.langChangeHandler);

        // URL 쿼리스트링 ?mode=write 또는 ?id=xxx 처리
        const url = new URL(window.location.href);
        const m = url.searchParams.get('mode');
        const id = url.searchParams.get('id');
        if (id) {
            await this.openDetail(parseInt(id, 10));
        } else if (m === 'write') {
            await this.openWrite();
        } else {
            await this.loadList();
        }
        this.loaded = true;
        await this.service.render();
    }

    public ngOnDestroy() {
        if (this.langChangeHandler) {
            window.removeEventListener('lang:change', this.langChangeHandler);
        }
    }

    public async loadList() {
        const res = await wiz.call('list', { page: 1, dump: 50 });
        if (res.code === 200) {
            this.items = res.data.items || [];
            this.total = res.data.total || 0;
        }
        const sres = await wiz.call('stats', {});
        if (sres.code === 200) {
            this.stats = sres.data || { counts: {}, timeline: [], total: 0 };
        }
        await this.service.render();
    }

    public async openList() {
        this.mode = 'list';
        this.detailItem = null;
        await this.loadList();
    }

    public async openWrite(prefill?: any) {
        this.mode = 'write';
        const today = new Date();
        const ymd = today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');
        this.form = {
            diary_id: prefill?.diary_id || '',
            diary_date: prefill?.diary_date || ymd,
            title: prefill?.title || '',
            content: prefill?.content || '',
            mood: prefill?.mood || '',
            related_draw_id: prefill?.related_draw_id || ''
        };
        // 최근 타로 기록 로드
        const res = await wiz.call('list_recent_tarot', {});
        if (res.code === 200) {
            this.recentTarots = res.data.items || [];
        }
        await this.service.render();
    }

    public async openDetail(id: number) {
        const res = await wiz.call('get', { diary_id: id });
        if (res.code === 200) {
            this.detailItem = res.data.item;
            this.mode = 'detail';
        } else {
            this.service.alert.show({ title: 'Error', message: res.data?.message || '불러오기 실패' });
        }
        await this.service.render();
    }

    public selectMood(key: string) {
        this.form.mood = (this.form.mood === key) ? '' : key;
        this.service.render();
    }

    public selectTarot(id: any) {
        this.form.related_draw_id = (String(this.form.related_draw_id) === String(id)) ? '' : id;
        this.service.render();
    }

    public async submit() {
        if (this.saving) return;
        if (!this.form.title?.trim()) {
            this.service.alert.show({ title: '알림', message: this.t('diary.alert.title_required', '제목을 입력해주세요.') });
            return;
        }
        if (!this.form.content?.trim()) {
            this.service.alert.show({ title: '알림', message: this.t('diary.alert.content_required', '내용을 입력해주세요.') });
            return;
        }
        this.saving = true;
        await this.service.render();
        try {
            const res = await wiz.call('save', this.form);
            if (res.code === 200) {
                this.service.alert.show({ title: 'OK', message: this.t('diary.alert.saved', '저장되었습니다.') });
                await this.openList();
            } else {
                this.service.alert.show({ title: 'Error', message: res.data?.message || '저장 실패' });
            }
        } finally {
            this.saving = false;
            await this.service.render();
        }
    }

    public async editDetail() {
        if (!this.detailItem) return;
        await this.openWrite(this.detailItem);
    }

    public async deleteDetail() {
        if (!this.detailItem) return;
        if (!confirm(this.t('diary.confirm.delete', '정말 삭제하시겠어요?'))) return;
        const res = await wiz.call('remove', { diary_id: this.detailItem.diary_id });
        if (res.code === 200) {
            this.service.alert.show({ title: 'OK', message: this.t('diary.alert.deleted', '삭제되었습니다.') });
            await this.openList();
        } else {
            this.service.alert.show({ title: 'Error', message: res.data?.message || '삭제 실패' });
        }
    }

    public moodEmoji(key: string): string {
        const o = MOOD_OPTIONS.find(x => x.key === key);
        return o ? o.emoji : '';
    }

    public statKeys(): string[] {
        return Object.keys(this.stats?.counts || {});
    }

    public statBarWidth(key: string): string {
        const total = this.stats?.total || 0;
        if (!total) return '0%';
        return ((this.stats.counts[key] / total) * 100).toFixed(1) + '%';
    }
}
