import { Component, OnInit, ViewEncapsulation } from "@angular/core";
import { Router } from "@angular/router";

declare let $: any;

@Component({
    selector: "app-root",
    encapsulation: ViewEncapsulation.None,
    styleUrls: [],
    template: `<router-outlet></router-outlet>`
})
export class AppComponent implements OnInit{
    constructor(public router: Router){

    }

    ngOnInit() {
        window.addEventListener('beforeunload',  (e) => {
            e.preventDefault();
        });
    }
}