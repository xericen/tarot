import { OnInit } from "@angular/core";
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
  constructor(public service: Service) {}

  public userName = '';
  public isLoading = false;
  public isCardDrawn = false;

  public cardImageUrl = '';
  public cardName: string | null = null;
  public isReversed = false;
  public subtitle = '';
  public finance = '';
  public love = '';
  public health = '';
  public focus = '';
  public keywords: string[] = [];
  public oneWord = '';

  async ngOnInit() {
    await this.service.init();
    if (!await this.service.auth.allow(true, '/login')) return;
    await this.service.render();
  }

  public async drawCard() {
    const name = (this.userName || '').trim();
    if (!name || this.isLoading) return;

    this.isLoading = true;
    await this.service.render();

    try {
      const { code, data } = await wiz.call('tarot_draw', { name });

      if (code === 200 && data) {
        this.cardName = data.card_name || null;
        this.cardImageUrl = data.image_url || '';
        this.isReversed = data.is_reversed || false;
        this.subtitle = data.subtitle || '';
        this.finance = data.finance || '';
        this.love = data.love || '';
        this.health = data.health || '';
        this.focus = data.focus || '';
        this.keywords = data.keywords || [];
        this.oneWord = data.one_word || '';
        this.isCardDrawn = true;
      } else {
        alert('운세를 불러오지 못했습니다.');
      }
    } catch (e) {
      console.error(e);
      alert('서버 오류가 발생했습니다.');
    } finally {
      this.isLoading = false;
      await this.service.render();
    }
  }

  get cardData() {
    if (!this.cardName) return null;
    return {
      userName: this.userName,
      concern: '일일 타로',
      cards: [{ card_name: this.cardName, is_reversed: this.isReversed }]
    };
  }

  public reset() {
    this.isCardDrawn = false;
    this.cardImageUrl = '';
    this.cardName = null;
    this.isReversed = false;
    this.subtitle = '';
    this.finance = '';
    this.love = '';
    this.health = '';
    this.focus = '';
    this.keywords = [];
    this.oneWord = '';
    this.service.render();
  }
}
