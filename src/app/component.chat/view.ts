import { OnInit, ViewChild, ElementRef } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

interface CardInfo {
    card_id: number;
    card_name: string;
    is_reversed: boolean;
    image_url: string;
}

interface ChatMessage {
    role: 'bot' | 'user';
    text: string;
    html?: string;
    card?: CardInfo;
}

export class Component implements OnInit {
    constructor(public service: Service) {}

    @ViewChild('chatBody') chatBody: ElementRef;
    @ViewChild('chatInput') chatInput: ElementRef;

    public messages: ChatMessage[] = [];
    public inputText = '';
    public isLoading = false;
    public showDrawButton = false;
    private userConcern = '';

    // 카드 선택 UI
    public showCardPicker = false;
    public pickerCards: number[] = [];
    public pickerReversed: boolean[] = [];
    public pickerFlipped: boolean[] = [];
    public pickerSelected: number | null = null;

    async ngOnInit() {
        await this.service.init();
        if (!await this.service.auth.allow(true, '/login')) return;

        this.messages.push({
            role: 'bot',
            text: '안녕하세요! 저는 타로 리더 루카리오예요 🔮\n오늘은 어떤 고민이 있으신가요? 편하게 이야기해주세요.'
        });

        await this.service.render();
    }

    private scrollToBottom() {
        setTimeout(() => {
            if (this.chatBody?.nativeElement) {
                this.chatBody.nativeElement.scrollTop = this.chatBody.nativeElement.scrollHeight;
            }
        }, 100);
    }

    public async sendMessage() {
        const text = (this.inputText || '').trim();
        if (!text || this.isLoading) return;

        this.messages.push({ role: 'user', text });
        this.inputText = '';
        this.isLoading = true;
        this.showDrawButton = false;
        await this.service.render();
        if (this.chatInput?.nativeElement) this.chatInput.nativeElement.value = '';
        this.scrollToBottom();

        if (!this.userConcern) {
            this.userConcern = text;
        }

        try {
            const { code, data } = await wiz.call('chat', {
                message: text,
                history: JSON.stringify(this.messages.slice(-10))
            });

            if (code === 200 && data?.reply) {
                this.messages.push({ role: 'bot', text: data.reply });
                if (this.userConcern && this.messages.length >= 3) {
                    this.showDrawButton = true;
                }
            } else {
                this.messages.push({ role: 'bot', text: '잠시 연결이 불안정해요. 다시 시도해주세요 🌙' });
            }
        } catch (err) {
            this.messages.push({ role: 'bot', text: '죄송해요, 오류가 발생했어요. 다시 시도해주세요 💫' });
        } finally {
            this.isLoading = false;
            await this.service.render();
            this.scrollToBottom();
        }
    }

    public async drawCard() {
        if (this.isLoading) return;
        // 78장 전체 카드 셔플
        const allCards = Array.from({ length: 78 }, (_, i) => i);
        for (let i = allCards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [allCards[i], allCards[j]] = [allCards[j], allCards[i]];
        }
        this.pickerCards = allCards;
        this.pickerReversed = allCards.map(() => Math.random() < 0.5);
        this.pickerFlipped = new Array(78).fill(false);
        this.pickerSelected = null;
        this.showCardPicker = true;
        this.showDrawButton = false;

        this.messages.push({ role: 'bot', text: '78장의 카드를 펼쳤어요! 좌우로 스크롤하면서 마음이 끌리는 카드 한 장을 선택해주세요 🔮' });
        await this.service.render();
        this.scrollToBottom();
    }

    public async selectPickerCard(index: number) {
        if (this.pickerSelected !== null || this.isLoading) return;

        this.pickerFlipped[index] = true;
        this.pickerSelected = index;
        await this.service.render();

        // 잠시 뒤집힌 카드를 보여준 후 API 호출
        setTimeout(async () => {
            this.showCardPicker = false;
            this.isLoading = true;

            const cardId = this.pickerCards[index];
            const isReversed = this.pickerReversed[index];
            this.messages.push({ role: 'user', text: '🃏 카드를 선택했습니다!' });
            await this.service.render();
            this.scrollToBottom();

            try {
                const { code, data } = await wiz.call('draw_card', {
                    concern: this.userConcern,
                    history: JSON.stringify(this.messages.slice(-10)),
                    card_id: String(cardId),
                    is_reversed: String(isReversed),
                });

                if (code === 200 && data) {
                    this.messages.push({
                        role: 'bot',
                        text: data.reply,
                        card: {
                            card_id: data.card_id,
                            card_name: data.card_name,
                            is_reversed: data.is_reversed,
                            image_url: data.image_url
                        }
                    });
                } else {
                    this.messages.push({ role: 'bot', text: '카드를 뽑는 중 문제가 발생했어요. 다시 시도해주세요 🔮' });
                }
            } catch (err) {
                this.messages.push({ role: 'bot', text: '죄송해요, 오류가 발생했어요 💫' });
            } finally {
                this.isLoading = false;
                this.showDrawButton = false;
                await this.service.render();
                this.scrollToBottom();

                // 잠시 후 추가 고민 유도 메시지
                setTimeout(async () => {
                    this.messages.push({ role: 'bot', text: '또 다른 고민이 있으시면 편하게 말씀해주세요 🌙\n카드를 한 번 더 뽑고 싶으시면 카드 뽑기 버튼을 눌러주세요!' });
                    this.showDrawButton = true;
                    await this.service.render();
                    this.scrollToBottom();
                }, 1500);
            }
        }, 800);
    }
}
