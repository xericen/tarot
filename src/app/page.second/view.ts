import { OnInit, Input } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    constructor(public service: Service) {}
    @Input() title: any;

    public async ngOnInit() {
        await this.service.init();
        if (!await this.service.auth.allow(true, '/login')) return;
        await this.service.render();
    }
}