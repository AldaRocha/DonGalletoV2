import { Component } from "@angular/core";
import { Router } from "@angular/router";

@Component({
    selector: "ventas-app",
    templateUrl: "./ventas.component.html",
    styleUrls: ["./ventas.component.scss"]
})
export class VentasComponent{
    constructor(public router: Router) {

    }

    Regresar(){
        this.router.navigate(["menu/inicio"]);
    }
}