import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

interface TarotResult {
    label: string;
    card_id: number | null;
    card_name: string | null;
    subtitle: string;
    message: string;
    keywords: string[];
    flow_word: string;
    image_url: string;
}

export class Component implements OnInit {
    constructor(public service: Service) { }

    public loveStatus: string = '';
    public userName: string = '';
    public isLocked: boolean = false;
    public showCards: boolean = false;
    public canComplete: boolean = false;
    public isLoading: boolean = false;

    public isResultView: boolean = false;
    public finalCards: TarotResult[] = [];
    public activeTab: number = 0;
    public flowWords: string[] = [];
    public closingMessage: string = '';

    public isSpread: boolean = false;
    public isShuffling: boolean = false;
    public isGathering: boolean = false;

    public tarotCards: number[] = [];
    public flippedCards: boolean[] = [];
    public reversedCards: boolean[] = [];
    public selectedCards: (number | null)[] = [null, null, null];
    public selectedReversed: boolean[] = [false, false, false];

    async ngOnInit() {
        await this.service.init();
        if (!await this.service.auth.allow(true, '/login')) return;
        this.shuffleArray();
        await this.service.render();
    }

    public onLoveStatusChange(value: string): void {
        this.loveStatus = value;
        this.isLocked = true;
    }

    public async setTab(index: number) {
        this.activeTab = index;
        await this.service.render();
    }

    public async resetSelection(): Promise<void> {
        this.userName = '';
        this.loveStatus = '';
        this.isLocked = false;
        this.showCards = false;
        this.isResultView = false;
        this.isLoading = false;
        this.isSpread = false;
        this.finalCards = [];
        this.activeTab = 0;
        this.flowWords = [];
        this.closingMessage = '';
        this.shuffleArray();
        await this.service.render();
    }

    public startCardSelection(): void {
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
        this.selectedCards = [null, null, null];
        this.selectedReversed = [false, false, false];
        this.canComplete = false;
        this.flippedCards = new Array(78).fill(false);
        this.reversedCards = Array.from({ length: 78 }, () => Math.random() < 0.5);
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

    getCardBackImage(): string {
        return '/assets/images/CardB.png';
    }

    selectCard(cardIndex: number): void {
        if (this.selectedCards.filter(v => v !== null).length >= 3) return;
        if (this.flippedCards[cardIndex]) return;

        this.flippedCards[cardIndex] = true;
        const nextSlot = this.selectedCards.findIndex(slot => slot === null);
        if (nextSlot !== -1) {
            this.selectedCards[nextSlot] = this.tarotCards[cardIndex];
            this.selectedReversed[nextSlot] = this.reversedCards[cardIndex];
        }
        if (this.selectedCards.filter(v => v !== null).length === 3) {
            this.canComplete = true;
        }
        this.service.render();
    }

    get cardData() {
        if (!this.finalCards.length) return null;
        return {
            userName: this.userName,
            concern: this.loveStatus,
            cards: this.finalCards.map((c: any) => ({
                card_name: c.card_name,
                is_reversed: c.is_reversed,
                label: c.label
            }))
        };
    }

    public async showFortune() {
        if (!this.userName?.trim() || !this.loveStatus) return;

        const selectedIds = this.selectedCards.filter((id): id is number => id !== null);

        if (selectedIds.length !== 3) {
            alert("카드를 3장 선택해주세요.");
            return;
        }

        this.isLoading = true;
        await this.service.render();

        try {
            const { code, data } = await wiz.call('tarot_draw_three', {
                name: this.userName,
                concern: this.loveStatus,
                selected: selectedIds.join(","),
                reversed: this.selectedReversed.join(","),
            });

            if (code === 200 && data) {
                this.finalCards = data.results.map((card: any) => ({
                    ...card,
                    image_url: `/assets/TarotCard/${card.card_id}.jpg`
                }));
                this.flowWords = data.flow_words || [];
                this.closingMessage = data.closing_message || '';
                this.activeTab = 0;
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
