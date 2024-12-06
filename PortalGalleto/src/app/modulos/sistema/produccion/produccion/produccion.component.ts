import { Component } from "@angular/core";
import { Router } from "@angular/router";

@Component({
    selector: "produccion-app",
    templateUrl: "./produccion.component.html",
    styleUrls: ["./produccion.component.scss"]
})
export class ProduccionComponent{
    constructor(public router: Router){
        
    }

    Regresar(){
        this.router.navigate(["menu/inicio"]);
    }
}