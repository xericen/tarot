import { OnInit, OnDestroy, ChangeDetectorRef, HostListener } from '@angular/core';

declare const window: any;

interface LangOption {
    code: string;
    label: string;
    flag: string;
}

export class Component implements OnInit, OnDestroy {
    public open: boolean = false;
    public current: string = 'ko';
    public langs: LangOption[] = [
        { code: 'ko', label: '한국어', flag: '🇰🇷' },
        { code: 'en', label: 'English', flag: '🇺🇸' },
        { code: 'ja', label: '日本語', flag: '🇯🇵' },
        { code: 'zh', label: '中文', flag: '🇨🇳' },
    ];

    private langChangeHandler = (e: any) => {
        this.current = e.detail?.lang || window.__lang || 'ko';
        this.ref.detectChanges();
    };

    constructor(public ref: ChangeDetectorRef) { }

    ngOnInit() {
        this.current = window.__lang || 'ko';
        window.addEventListener('lang:change', this.langChangeHandler);
    }

    ngOnDestroy() {
        window.removeEventListener('lang:change', this.langChangeHandler);
    }

    public toggle(event?: Event) {
        if (event) {
            event.stopPropagation();
            event.preventDefault();
        }
        this.open = !this.open;
    }

    public select(code: string, event?: Event) {
        if (event) event.stopPropagation();
        this.open = false;
        if (code === this.current) return;
        if (typeof window.__setLang === 'function') {
            window.__setLang(code);
        }
        this.current = code;
        this.ref.detectChanges();
        // 리렌더 강제: 살짝 지연 후 페이지 리렌더 트리거
        // (Angular 변경감지가 동작하지 않는 곳까지 반영)
        setTimeout(() => {
            window.dispatchEvent(new Event('resize'));
        }, 0);
    }

    @HostListener('document:click')
    public onDocClick() {
        if (this.open) {
            this.open = false;
            this.ref.detectChanges();
        }
    }

    public get currentLabel(): string {
        const item = this.langs.find(l => l.code === this.current);
        return item ? item.flag : '🌐';
    }

    public get currentCode(): string {
        return this.current.toUpperCase();
    }
}
