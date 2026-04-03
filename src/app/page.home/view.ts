import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    constructor(public service: Service) {}

    async ngOnInit() {
        await this.service.init();
        this.service.href('/login');
    }
}
