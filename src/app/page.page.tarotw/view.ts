import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

interface YearlyResult {
    season: string;
    card_id: number;
    card_name: string;
    message: string;
    image_url: string;
    is_reversed: boolean;
}

export class Component implements OnInit {
    constructor(public service: Service) {}

    userName: string = '';
    loveStatus: string = '';
    jobStatus: string = '';

    isLocked: boolean = false;
    showCards: boolean = false;
    isResultView: boolean = false;
    isLoading: boolean = false;
    currentYear: number = new Date().getFullYear();

    isSpread: boolean = false;
    isShuffling: boolean = false;
    isGathering: boolean = false;

    tarotCards: number[] = [];
    flippedCards: boolean[] = [];
    reversedCards: boolean[] = [];
    selectedCards: (number | null)[] = [null, null, null, null];
    selectedReversed: boolean[] = [false, false, false, false];

    finalResults: YearlyResult[] = [];

    async ngOnInit() {
        await this.service.init();
        if (!await this.service.auth.allow(true, '/login')) return;
        this.shuffleArray();
        await this.service.render();
    }

    async resetSelection(): Promise<void> {
        this.userName = '';
        this.loveStatus = '';
        this.jobStatus = '';
        this.isLocked = false;
        this.showCards = false;
        this.isResultView = false;
        this.isSpread = false;
        this.finalResults = [];
        this.shuffleArray();
        await this.service.render();
    }

    get canShowCardButton(): boolean {
        return !!(this.userName && this.loveStatus && this.jobStatus);
    }

    get canComplete(): boolean {
        return this.selectedCards.every(card => card !== null);
    }

    startCardSelection(): void {
        this.isLocked = true;
        this.showCards = true;
        this.isSpread = false;
        this.shuffleCards();
    }

    private shuffleArray(): void {
        const cards = Array.from({ length: 78 }, (_, i) => i);
        for (let i = cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [cards[i], cards[j]] = [cards[j], cards[i]];
        }
        this.tarotCards = cards;
        this.selectedCards = [null, null, null, null];
        this.selectedReversed = [false, false, false, false];
        this.flippedCards = new Array(78).fill(false);
        this.reversedCards = Array.from({ length: 78 }, () => Math.random() < 0.5);
    }

    shuffleCards(): void {
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

    getSpreadTransform(index: number, total: number): string {
        const angleRange = 60;
        const radius = 280;
        const angle = -angleRange / 2 + (index / (total - 1)) * angleRange;
        const rad = (angle * Math.PI) / 180;
        const x = Math.sin(rad) * radius;
        const y = Math.abs(Math.cos(rad)) * 30;
        return `translate(${x}px, ${y}px) rotate(${angle}deg)`;
    }

    selectCard(cardIndex: number): void {
        if (this.selectedCards.filter(v => v !== null).length >= 4) return;
        if (this.flippedCards[cardIndex]) return;

        this.flippedCards[cardIndex] = true;
        const nextSlot = this.selectedCards.findIndex(slot => slot === null);
        if (nextSlot !== -1) {
            this.selectedCards[nextSlot] = this.tarotCards[cardIndex];
            this.selectedReversed[nextSlot] = this.reversedCards[cardIndex];
        }
        this.service.render();
    }

    getCardImage(i: number): string {
        if (this.selectedCards[i] !== null) {
            return `/assets/TarotCard/${this.selectedCards[i]}.jpg`;
        }
        return '';
    }

    get cardData() {
        if (!this.finalResults.length) return null;
        return {
            userName: this.userName,
            concern: `${this.currentYear}년 연간 타로`,
            cards: this.finalResults.map((r: any) => ({
                card_name: r.card_name,
                is_reversed: r.is_reversed,
                label: r.season
            }))
        };
    }

    public async completeSelection() {
        const selectedIds = this.selectedCards.filter((id): id is number => id !== null);
        if (selectedIds.length !== 4) {
            alert("카드를 4장 선택해주세요.");
            return;
        }

        this.isLoading = true;
        await this.service.render();

        try {
            const { code, data } = await wiz.call('yearly_fortune', {
                name: this.userName,
                love_status: this.loveStatus,
                job_status: this.jobStatus,
                selected: selectedIds.join(","),
                reversed: this.selectedReversed.join(","),
            });

            if (code === 200 && data) {
                this.finalResults = data.results;
                this.isResultView = true;
                this.showCards = false;
            } else {
                alert('운세를 불러오지 못했습니다.');
            }
        } catch (err) {
            console.error("API error:", err);
            alert('서버 오류가 발생했습니다.');
        } finally {
            this.isLoading = false;
            await this.service.render();
        }
    }
}
