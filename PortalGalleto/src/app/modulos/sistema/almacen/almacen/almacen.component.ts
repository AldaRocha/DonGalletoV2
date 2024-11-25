import { Component, OnInit } from "@angular/core";
import { Router } from "@angular/router";

@Component({
    selector: "almacen-app",
    templateUrl: "./almacen.component.html",
    styleUrls: ["./almacen.component.scss"]
})
export class AlmacenComponent implements OnInit{

    constructor(public router: Router) {

    }

    ngOnInit(): void {
        this.DatosIniciales();
    }

    async DatosIniciales(){

    }

    Regresar(){
        this.router.navigate(["menu/inicio"]);
    }
}