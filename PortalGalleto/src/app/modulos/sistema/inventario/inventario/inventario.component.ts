import { Component } from "@angular/core";
import { Router } from "@angular/router";

@Component({
    selector: "inventario-app",
    templateUrl: "./inventario.component.html",
    styleUrls: ["./inventario.component.scss"]
})
export class InventarioComponent{
    constructor(public router: Router){
        
    }

    Regresar(){
        this.router.navigate(["menu/inicio"]);
    }
}