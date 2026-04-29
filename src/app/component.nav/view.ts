import { OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';

declare const wiz: any;
declare const window: any;

export class Component implements OnInit, OnDestroy {
    public isLoggedIn: boolean = false;
    public userName: string = '';

    private langChangeHandler = () => this.ref.detectChanges();

    constructor(public ref: ChangeDetectorRef) { }

    public t(key: string, fallback?: string): string {
        if (typeof window.__t === 'function') return window.__t(key, fallback);
        return fallback != null ? fallback : key;
    }

    async ngOnInit() {
        try {
            const { code, data } = await wiz.call('check');
            if (code === 200 && data?.logged_in) {
                this.isLoggedIn = true;
                this.userName = data.name || '';
            }
        } catch (e) { }
        window.addEventListener('lang:change', this.langChangeHandler);
    }

    ngOnDestroy() {
        window.removeEventListener('lang:change', this.langChangeHandler);
    }
}
