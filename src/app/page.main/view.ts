import { OnInit, OnDestroy, ChangeDetectorRef } from "@angular/core";
import { Service } from '@wiz/libs/portal/season/service';

declare const window: any;

export class Component implements OnInit, OnDestroy {
    constructor(public service: Service, public ref: ChangeDetectorRef) { }

    public currentYear: number = new Date().getFullYear();

    private langChangeHandler = () => this.ref.detectChanges();

    public t(key: string, fallback?: string, vars?: any): string {
        let txt = (typeof window.__t === 'function') ? window.__t(key, fallback) : (fallback != null ? fallback : key);
        if (vars) {
            for (const k of Object.keys(vars)) {
                txt = txt.split('{' + k + '}').join(String(vars[k]));
            }
        }
        return txt;
    }

    public async ngOnInit() {
        await this.service.init();
        if (!await this.service.auth.allow(true, '/login')) return;
        window.addEventListener('lang:change', this.langChangeHandler);
        await this.service.render();
    }

    ngOnDestroy() {
        window.removeEventListener('lang:change', this.langChangeHandler);
    }
}
