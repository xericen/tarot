import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

interface MonthlyResult {
    card_id: number;
    card_name: string;
    image_url: string;
    month: string;
    subtitle: string;
    overview: string;
    career: string;
    love: string;
    finance: string;
    health: string;
    advice: string;
    keywords: string[];
    lucky_day: string;
    closing: string;
}

export class Component implements OnInit {
    constructor(public service: Service) {}

    public userName: string = '';
    public concern: string = '';
    public showCards: boolean = false;
    public isResultView: boolean = false;
    public isLoading: boolean = false;
    public isSpread: boolean = false;
    public isShuffling: boolean = false;
    public isGathering: boolean = false;

    public tarotCards: number[] = [];
    public flippedCards: boolean[] = [];
    public reversedCards: boolean[] = [];
    public selectedCard: number | null = null;
    public selectedReversed: boolean = false;

    public result: MonthlyResult | null = null;
    public activeSection: string = 'overview';

    public currentMonth: string = '';

    async ngOnInit() {
        await this.service.init();
        if (!await this.service.auth.allow(true, '/login')) return;
        const now = new Date();
        const months = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'];
        this.currentMonth = `${now.getFullYear()}년 ${months[now.getMonth()]}`;
        this.shuffleArray();
        await this.service.render();
    }

    private shuffleArray(): void {
        const cards = Array.from({ length: 78 }, (_, i) => i);
        for (let i = cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [cards[i], cards[j]] = [cards[j], cards[i]];
        }
        this.tarotCards = cards;
        this.selectedCard = null;
        this.selectedReversed = false;
        this.flippedCards = new Array(78).fill(false);
        this.reversedCards = Array.from({ length: 78 }, () => Math.random() < 0.5);
    }

    public startSelection(): void {
        this.showCards = true;
        this.isResultView = false;
        this.isSpread = false;
        this.shuffleCards();
    }

    public shuffleCards(): void {
        if (this.isShuffling) return;
        this.isSpread = false;
        this.isShuffling = false;
        this.isGathering = true;
        this.service.render();

        setTimeout(() => {
            this.isGathering = false;
            this.isShuffling = true;
            this.service.render();

            setTimeout(() => {
                this.shuffleArray();
                this.isShuffling = false;
                this.isSpread = true;
                this.service.render();
            }, 1200);
        }, 600);
    }

    public getSpreadTransform(index: number, total: number): string {
        const angleRange = 60;
        const radius = 280;
        const angle = -angleRange / 2 + (index / (total - 1)) * angleRange;
        const rad = (angle * Math.PI) / 180;
        const x = Math.sin(rad) * radius;
        const y = Math.abs(Math.cos(rad)) * 30;
        return `translate(${x}px, ${y}px) rotate(${angle}deg)`;
    }

    public selectCard(cardIndex: number): void {
        if (this.selectedCard !== null) return;
        this.flippedCards[cardIndex] = true;
        this.selectedCard = Number(this.tarotCards[cardIndex]);
        this.selectedReversed = this.reversedCards[cardIndex];
        this.service.render();
    }

    public async setSection(section: string) {
        this.activeSection = section;
        await this.service.render();
    }

    public async resetSelection(): Promise<void> {
        this.userName = '';
        this.concern = '';
        this.showCards = false;
        this.isResultView = false;
        this.isLoading = false;
        this.result = null;
        this.activeSection = 'overview';
        this.selectedCard = null;
        this.shuffleArray();
        await this.service.render();
    }

    public async showResult(): Promise<void> {
        if (this.selectedCard === null || this.isLoading) return;
        if (!this.userName?.trim() || !this.concern) return;

        this.isLoading = true;
        this.showCards = false;
        this.isResultView = true;
        await this.service.render();

        try {
            const { code, data } = await wiz.call('monthly_draw', {
                name: this.userName,
                concern: this.concern,
                card_id: String(this.selectedCard),
                is_reversed: String(this.selectedReversed),
            });

            if (code === 200 && data) {
                this.result = data as MonthlyResult;
                this.activeSection = 'overview';
            } else {
                alert('운세를 불러오지 못했습니다.');
                this.isResultView = false;
                this.showCards = true;
            }
        } catch (e) {
            alert('서버 오류가 발생했습니다.');
            this.isResultView = false;
            this.showCards = true;
        } finally {
            this.isLoading = false;
            await this.service.render();
        }
    }

    get cardData() {
        if (!this.result) return null;
        return {
            userName: this.userName,
            concern: this.concern || '월간 타로',
            cards: [{ card_name: this.result.card_name, is_reversed: this.selectedReversed }]
        };
    }
}
