import { OnInit } from '@angular/core';

export class Component implements OnInit {
    public isLoggedIn: boolean = false;
    public userName: string = '';

    constructor() { }

    async ngOnInit() {
        try {
            const { code, data } = await wiz.call('check');
            if (code === 200 && data?.logged_in) {
                this.isLoggedIn = true;
                this.userName = data.name || '';
            }
        } catch (e) { }
    }
}