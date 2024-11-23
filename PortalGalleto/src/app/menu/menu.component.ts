import { Component, OnInit, ViewEncapsulation } from "@angular/core";
import { StorageService } from "../services/storage.service";
import { Router } from "@angular/router";

@Component({
    encapsulation: ViewEncapsulation.None,
    selector: "menu-app",
    templateUrl: "./menu.component.html",
    styleUrls: ["./menu.component.scss"]
})
export class MenuComponent implements OnInit{
    router: Router;

    constructor(public storage: StorageService, router: Router){
        this.router = router;
        if (!this.storage.getItem("dongalleto-oauth")){
            this.router.navigate(["login/login"]);
        }
    }

    ngOnInit(): void {
        
    }
}