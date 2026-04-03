import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    constructor(public service: Service) { }

    public loaded = false;
    public userName = '';
    public userEmail = '';
    public history: any[] = [];

    public tarotTypeMap: any = {
        'daily': '일일 타로',
        'today': '오늘의 타로',
        'season': 'Season 카드',
        'yearly': '연간 타로',
        'monthly': '월간 타로'
    };

    public moodOptions = ['기대', '설렘', '불안', '우울', '감사', '혼란', '평온', '호기심'];
    public editingMoodId: number | null = null;
    public editingMoodTags: string[] = [];

    public searchText = '';
    public filterType = '';
    public filteredHistory: any[] = [];
    public currentPage = 1;
    public pageSize = 5;
    public filterTypes = [
        { label: '전체', value: '' },
        { label: '일일', value: 'daily' },
        { label: '오늘', value: 'today' },
        { label: '시즌', value: 'season' },
        { label: '연간', value: 'yearly' },
        { label: '월간', value: 'monthly' }
    ];

    public viewMode = 'list';
    public calYear = new Date().getFullYear();
    public calMonth = new Date().getMonth();
    public calendarCells: any[] = [];
    public selectedCalDate: any = null;

    public statsPeriod = 'all';
    public statsLoading = false;
    public statsData: any = null;
    public suitList: any[] = [];
    public hasMoodPatterns = false;
    public moodPatternList: any[] = [];
    public statsPeriods = [
        { label: '전체', value: 'all' },
        { label: '1주', value: 'week' },
        { label: '1달', value: 'month' },
        { label: '3달', value: '3month' }
    ];

    public async ngOnInit() {
        await this.service.init();
        if (!await this.service.auth.allow(true, '/login')) return;
        await this.loadProfile();
        await this.service.render();
    }

    private async loadProfile() {
        try {
            const { code, data } = await wiz.call('profile');
            if (code === 200 && data) {
                this.userName = data.name || '';
                this.userEmail = data.email || '';
                this.history = data.history || [];
                this.loaded = true;
                this.applyFilter();
            } else {
                location.href = '/login';
            }
        } catch (e) {
            location.href = '/login';
        }
    }

    public getCardImages(cardIds: string): string[] {
        if (!cardIds) return [];
        return cardIds.split(',').map(id => `/assets/TarotCard/${id.trim()}.jpg`);
    }

    public getMoodTags(moodStr: string): string[] {
        if (!moodStr) return [];
        return moodStr.split(',').filter(t => t.trim());
    }

    public async setFilterType(type: string) {
        this.filterType = type;
        this.currentPage = 1;
        this.applyFilter();
        await this.service.render();
    }

    public applyFilter() {
        let items = this.history;
        if (this.filterType) {
            items = items.filter(item => item.tarot_type === this.filterType);
        }
        if (this.searchText.trim()) {
            const q = this.searchText.trim().toLowerCase();
            items = items.filter(item =>
                (item.cards || '').toLowerCase().includes(q) ||
                (item.result_summary || '').toLowerCase().includes(q)
            );
        }
        this.filteredHistory = items;
    }

    get totalPages(): number {
        return Math.max(1, Math.ceil(this.filteredHistory.length / this.pageSize));
    }

    get paginatedHistory(): any[] {
        const start = (this.currentPage - 1) * this.pageSize;
        return this.filteredHistory.slice(start, start + this.pageSize);
    }

    get pageNumbers(): number[] {
        const pages: number[] = [];
        for (let i = 1; i <= this.totalPages; i++) pages.push(i);
        return pages;
    }

    public async goToPage(page: number) {
        if (page < 1 || page > this.totalPages) return;
        this.currentPage = page;
        await this.service.render();
    }

    public async onSearchChange() {
        this.currentPage = 1;
        this.applyFilter();
        await this.service.render();
    }

    public async startEditMood(item: any) {
        this.editingMoodId = item.id;
        this.editingMoodTags = item.mood_tags ? item.mood_tags.split(',').filter((t: string) => t.trim()) : [];
        await this.service.render();
    }

    public async toggleMoodTag(tag: string) {
        const idx = this.editingMoodTags.indexOf(tag);
        if (idx >= 0) {
            this.editingMoodTags.splice(idx, 1);
        } else {
            this.editingMoodTags.push(tag);
        }
        await this.service.render();
    }

    public async saveMoodTags() {
        if (this.editingMoodId === null) return;
        try {
            const { code } = await wiz.call('save_mood', {
                history_id: this.editingMoodId,
                mood_tags: this.editingMoodTags.join(',')
            });
            if (code === 200) {
                const item = this.history.find(h => h.id === this.editingMoodId);
                if (item) item.mood_tags = this.editingMoodTags.join(',');
            }
        } catch (e) { }
        this.editingMoodId = null;
        await this.service.render();
    }

    public async cancelEditMood() {
        this.editingMoodId = null;
        await this.service.render();
    }

    public async setViewMode(mode: string) {
        this.viewMode = mode;
        if (mode === 'calendar') {
            this.buildCalendar();
        } else if (mode === 'stats' && !this.statsData) {
            await this.loadStats('all');
        }
        this.selectedCalDate = null;
        await this.service.render();
    }

    public async prevMonth() {
        this.calMonth--;
        if (this.calMonth < 0) { this.calMonth = 11; this.calYear--; }
        this.buildCalendar();
        this.selectedCalDate = null;
        await this.service.render();
    }

    public async nextMonth() {
        this.calMonth++;
        if (this.calMonth > 11) { this.calMonth = 0; this.calYear++; }
        this.buildCalendar();
        this.selectedCalDate = null;
        await this.service.render();
    }

    public async selectCalDate(cell: any) {
        this.selectedCalDate = cell;
        await this.service.render();
    }

    private buildCalendar() {
        const firstDay = new Date(this.calYear, this.calMonth, 1).getDay();
        const daysInMonth = new Date(this.calYear, this.calMonth + 1, 0).getDate();
        const cells: any[] = [];

        const monthStr = `${this.calYear}-${String(this.calMonth + 1).padStart(2, '0')}`;
        const recordsByDay: { [key: number]: any[] } = {};
        for (const item of this.history) {
            if (item.created_at && item.created_at.startsWith(monthStr)) {
                const day = parseInt(item.created_at.substring(8, 10));
                if (!recordsByDay[day]) recordsByDay[day] = [];
                recordsByDay[day].push(item);
            }
        }

        for (let i = 0; i < firstDay; i++) {
            cells.push({ day: null, records: [] });
        }
        for (let d = 1; d <= daysInMonth; d++) {
            cells.push({ day: d, records: recordsByDay[d] || [] });
        }
        this.calendarCells = cells;
    }

    public async loadStats(period: string) {
        this.statsPeriod = period;
        this.statsLoading = true;
        await this.service.render();

        try {
            const { code, data } = await wiz.call('stats', { period });
            if (code === 200 && data) {
                this.statsData = data;
                const dist = data.suit_distribution || {};
                const maxVal = Math.max(...Object.values(dist).map((v: any) => v || 0), 1);
                this.suitList = Object.entries(dist).map(([name, count]: [string, any]) => ({
                    name,
                    count: count || 0,
                    pct: Math.round(((count || 0) / maxVal) * 100)
                }));

                const patterns = data.mood_patterns || {};
                this.hasMoodPatterns = Object.keys(patterns).length > 0;
                this.moodPatternList = Object.entries(patterns).map(([mood, cards]: [string, any]) => ({
                    mood,
                    cards
                }));
            }
        } catch (e) { }

        this.statsLoading = false;
        await this.service.render();
    }

    // 상세 보기
    public selectedDetail: any = null;
    public detailLoading = false;

    public async logout() {
        try {
            await wiz.call('logout');
        } catch (e) { }
        location.href = '/main/user';
    }

    public async showDetail(item: any) {
        this.detailLoading = true;
        this.selectedDetail = { ...item, result: null };
        await this.service.render();

        try {
            const { code, data } = await wiz.call('detail', { history_id: item.id });
            if (code === 200 && data?.result_data) {
                this.selectedDetail.result = typeof data.result_data === 'string' ? JSON.parse(data.result_data) : data.result_data;
            }
        } catch (e) { }

        this.detailLoading = false;
        await this.service.render();
    }

    public async closeDetail() {
        this.selectedDetail = null;
        await this.service.render();
    }
}
