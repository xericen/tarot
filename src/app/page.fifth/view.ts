import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

interface TarotCardInfo {
  card_name: string;
  image_url: string;
  card_id?: number;
  is_reversed: boolean;
  keyword: string;
  fortune: string;
  guide_good: string;
  guide_caution: string;
  lucky_color: string;
  lucky_tip: string;
}

export class Component implements OnInit {
  constructor(public service: Service) {}

  public userName = '';
  public showCards = false;
  public isResultView = false;
  public canComplete = false;
  public isSpread = false;
  public isShuffling = false;
  public isGathering = false;

  public tarotCards: number[] = [];
  public selectedCard: number | null = null;
  public selectedReversed: boolean = false;
  public reversedCards: boolean[] = [];
  public flippedCards: boolean[] = [];

  public cardInfo: TarotCardInfo | null = null;
  public isLoading = false;

  async ngOnInit() {
    await this.service.init();
    if (!await this.service.auth.allow(true, '/login')) return;
    this.shuffleArray();
    await this.service.render();
  }

  public startSelection(): void {
    this.showCards = true;
    this.isResultView = false;
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
    this.selectedCard = null;
    this.selectedReversed = false;
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

    // Phase 1: Gather (카드 모이기) - 0.6s
    setTimeout(() => {
      this.isGathering = false;
      this.isShuffling = true;
      this.service.render();

      // Phase 2: Shuffle (섹기) - 1.2s
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

  public getCardBackImage(): string {
    return '/assets/images/CardB.png';
  }

  public selectCard(cardIndex: number): void {
    if (this.selectedCard !== null) return;
    this.flippedCards[cardIndex] = true;
    this.selectedCard = Number(this.tarotCards[cardIndex]);
    if (!Number.isInteger(this.selectedCard)) {
      this.selectedCard = null;
      return;
    }
    this.selectedReversed = this.reversedCards[cardIndex];
    this.canComplete = true;
  }

  get cardData() {
    if (!this.cardInfo) return null;
    return {
      userName: this.userName || '',
      concern: '오늘의 타로',
      cards: [{ card_name: this.cardInfo.card_name, is_reversed: this.cardInfo.is_reversed }]
    };
  }

  public async restart(): Promise<void> {
    this.isResultView = false;
    this.showCards = false;
    this.cardInfo = null;
    this.userName = '';
    this.selectedCard = null;
    this.selectedReversed = false;
    this.canComplete = false;
    this.flippedCards = new Array(78).fill(false);
    this.shuffleArray();
    await this.service.render();
  }

  public async showResult(): Promise<void> {
    if (this.selectedCard === null || this.isLoading) return;

    const cid = Number(this.selectedCard);
    if (!Number.isInteger(cid) || cid < 0 || cid > 77) {
      alert('선택한 카드가 잘못되었습니다.');
      return;
    }

    this.isLoading = true;
    this.showCards = false;
    this.isResultView = true;
    await this.service.render();

    try {
      const { code, data } = await wiz.call('tarot_result', { card_id: String(cid), is_reversed: String(this.selectedReversed), name: this.userName });

      if (code === 200 && data) {
        this.cardInfo = {
          card_id: data.card_id,
          card_name: data.card_name || '',
          image_url: data.image_url || `/assets/TarotCard/${cid}.jpg`,
          is_reversed: data.is_reversed || false,
          keyword: data.keyword || '',
          fortune: data.fortune || '',
          guide_good: data.guide_good || '',
          guide_caution: data.guide_caution || '',
          lucky_color: data.lucky_color || '',
          lucky_tip: data.lucky_tip || '',
        };
      } else {
        alert('카드 정보를 불러오지 못했습니다.');
        this.isResultView = false;
        this.showCards = true;
      }
    } catch (e: any) {
      alert('서버 오류가 발생했습니다.');
      this.isResultView = false;
      this.showCards = true;
    } finally {
      this.isLoading = false;
      await this.service.render();
    }
  }
}
