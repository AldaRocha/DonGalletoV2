import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";

@Component({
    selector: "inicio-app",
    templateUrl: "./inicio.component.html",
    styleUrls: ["./inicio.component.scss"]
})
export class InicioComponent {
    constructor(public router: Router) {
        
    }

    Navegar(ruta: string){
        this.router.navigate([ruta]);
    }

    Salir(){
        localStorage.clear();
        this.router.navigate(["login/login"]);
    }
}