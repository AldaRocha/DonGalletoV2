import { Component } from "@angular/core";
import { Router } from "@angular/router";

@Component({
    selector: "reportes-app",
    templateUrl: "./reportes.component.html",
    styleUrls: ["./reportes.component.scss"]
})
export class ReportesComponent{
    constructor(public router: Router){
        
    }

    Regresar(){
        this.router.navigate(["menu/inicio"]);
    }
}