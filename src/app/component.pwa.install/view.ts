import { OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';

declare const window: any;

export class Component implements OnInit, OnDestroy {
    public canInstall: boolean = false;
    public installed: boolean = false;
    public dismissed: boolean = false;

    private installableHandler = () => {
        this.canInstall = true;
        this.ref.detectChanges();
    };
    private installedHandler = () => {
        this.canInstall = false;
        this.installed = true;
        this.ref.detectChanges();
    };

    constructor(public ref: ChangeDetectorRef) { }

    async ngOnInit() {
        // 이미 PWA로 실행 중이면 배너 숨김
        if (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) {
            this.installed = true;
            return;
        }
        if ((window.navigator as any).standalone === true) {
            this.installed = true;
            return;
        }

        // 사용자가 한번 닫았으면 24시간 동안 안보이게
        const dismissedAt = localStorage.getItem('pwa-dismissed-at');
        if (dismissedAt && Date.now() - parseInt(dismissedAt) < 24 * 60 * 60 * 1000) {
            this.dismissed = true;
        }

        // 이미 캐시된 prompt 이벤트가 있으면 즉시 노출
        if (window.__pwaInstallPrompt) {
            this.canInstall = true;
        }

        window.addEventListener('pwa:installable', this.installableHandler);
        window.addEventListener('pwa:installed', this.installedHandler);
    }

    ngOnDestroy() {
        window.removeEventListener('pwa:installable', this.installableHandler);
        window.removeEventListener('pwa:installed', this.installedHandler);
    }

    public async install() {
        const prompt = window.__pwaInstallPrompt;
        if (!prompt) return;
        try {
            prompt.prompt();
            const { outcome } = await prompt.userChoice;
            if (outcome === 'accepted') {
                this.installed = true;
            }
            window.__pwaInstallPrompt = null;
            this.canInstall = false;
            this.ref.detectChanges();
        } catch (e) {
            console.warn('[PWA] install failed', e);
        }
    }

    public dismiss() {
        this.dismissed = true;
        localStorage.setItem('pwa-dismissed-at', String(Date.now()));
        this.ref.detectChanges();
    }
}
