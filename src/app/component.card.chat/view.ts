import { OnInit, Input, ViewChild, ElementRef } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

interface ChatMessage {
    role: 'bot' | 'user';
    text: string;
}

export class Component implements OnInit {
    @Input() cardData: any = null;
    @ViewChild('chatBody') chatBody!: ElementRef;
    @ViewChild('chatInput') chatInput!: ElementRef;

    constructor(public service: Service) {}

    public messages: ChatMessage[] = [];
    public inputText: string = '';
    public isLoading: boolean = false;
    public isOpen: boolean = false;

    async ngOnInit() {
        await this.service.init();
        await this.service.render();
    }

    public async toggleChat() {
        this.isOpen = !this.isOpen;
        if (this.isOpen && this.messages.length === 0) {
            this.initChat();
        }
        await this.service.render();
        this.scrollToBottom();
    }

    private initChat() {
        const cards = this.cardData?.cards || [];
        const userName = this.cardData?.userName || '';
        const concern = this.cardData?.concern || '';

        let greeting = `안녕하세요 ${userName}님! 🔮 방금 뽑으신 카드에 대해 더 궁금한 점이 있으시면 편하게 물어보세요.`;

        if (cards.length === 1) {
            greeting += `\n\n뽑으신 카드: **${cards[0].card_name}** ${cards[0].is_reversed ? '(역방향)' : '(정방향)'}`;
        } else if (cards.length > 1) {
            greeting += '\n\n뽑으신 카드:';
            cards.forEach((c: any) => {
                greeting += `\n• **${c.card_name}** ${c.is_reversed ? '(역방향)' : '(정방향)'}`;
            });
        }

        this.messages.push({ role: 'bot', text: greeting });
    }

    private scrollToBottom() {
        setTimeout(() => {
            if (this.chatBody?.nativeElement) {
                this.chatBody.nativeElement.scrollTop = this.chatBody.nativeElement.scrollHeight;
            }
        }, 100);
    }

    public async sendMessage() {
        if (!this.inputText.trim() || this.isLoading) return;

        const text = this.inputText.trim();
        this.inputText = '';
        this.messages.push({ role: 'user', text });
        this.isLoading = true;
        await this.service.render();
        if (this.chatInput?.nativeElement) this.chatInput.nativeElement.value = '';
        this.scrollToBottom();

        try {
            const { code, data } = await wiz.call('chat', {
                message: text,
                history: JSON.stringify(this.messages.slice(-10)),
                card_context: JSON.stringify(this.cardData),
            });

            if (code === 200 && data?.reply) {
                this.messages.push({ role: 'bot', text: data.reply });
            } else {
                this.messages.push({ role: 'bot', text: '잠시 연결이 불안해졌어요... 다시 질문해 주세요 🔮' });
            }
        } catch {
            this.messages.push({ role: 'bot', text: '서버 오류가 발생했어요. 잠시 후 다시 시도해 주세요.' });
        } finally {
            this.isLoading = false;
            await this.service.render();
            this.scrollToBottom();
        }
    }
}
