import { Component, ComponentFactory, ComponentFactoryResolver, ComponentRef, OnInit, ViewChild, ViewContainerRef } from "@angular/core";
import { Router } from "@angular/router";
import { Subject } from "rxjs";
import { GalletaViewModel } from "src/app/model/GalletaViewModel";
import { RestService } from "src/app/services/rest.service";
import { FormRecetasComponent } from "../componentes/form.recetas.component";

@Component({
    selector: "recetas-app",
    templateUrl: "./recetas.component.html",
    styleUrls: ["./recetas.component.scss"]
})
export class RecetasComponent implements OnInit{
    @ViewChild("containerFormulario", {read: ViewContainerRef}) containerFormulario: any;

    consulta: boolean = false;
    dtOptions: any = {};
    dtTrigger: Subject<any> = new Subject<any>();
    Galletas: GalletaViewModel[] = [];
    Loading: boolean = false;

    constructor(public router: Router, private _rest: RestService, public _cfr: ComponentFactoryResolver) {
        
    }

    ngOnInit(): void {
        this.dtOptions = {
            language: {url: "./assets/datatable/Spanish.json"}
        }
        this.DatosIniciales();
    }

    async DatosIniciales(){
        this.Loading = true;
        const response: any = await this._rest.Get("/galleta");
        if (!response.error){
            this.Galletas = [];
            this.Galletas = response.data;
            this.dtTrigger.next(null);
        }
        this.Loading = false;
    }

    Formulario(accionId: number, c: GalletaViewModel | null){
        let accion: string = "";
        switch (accionId){
            case 1:
                accion = "Agregar";
                break;
            case 2:
                accion = "Editar";
                break;
        }
        this.CargarContenedorFormulario({accion: accion, c: c});
    }

    CargarContenedorFormulario(data: {accion: string, c: GalletaViewModel | null}){
        this.consulta = true;
        this.containerFormulario.clear();
        const factory: ComponentFactory<any> = this._cfr.resolveComponentFactory(FormRecetasComponent);
        var ref: ComponentRef<any> = this.containerFormulario.createComponent(factory);
        ref.instance.accion = data.accion;
        ref.instance.Galleta = data.c;
        ref.instance.output.subscribe((cambio: boolean) => {
            this.consulta = false;
            ref.destroy();
            if (cambio){
                window.location.reload();
            }
        });
    }

    Regresar(){
        this.router.navigate(["menu/inicio"]);
    }
}