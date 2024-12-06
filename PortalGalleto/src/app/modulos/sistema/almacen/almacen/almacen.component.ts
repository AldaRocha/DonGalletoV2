import { Component, ComponentFactory, ComponentFactoryResolver, ComponentRef, OnInit, ViewChild, ViewContainerRef } from "@angular/core";
import { Router } from "@angular/router";
import { Subject } from "rxjs";
import { InventarioViewModel } from "src/app/model/InventarioViewModel";
import { RestService } from "src/app/services/rest.service";
import { FormAlmacenComponent } from "../componentes/form.almacen.component";
import Swall from "sweetalert2";

@Component({
    selector: "almacen-app",
    templateUrl: "./almacen.component.html",
    styleUrls: ["./almacen.component.scss"]
})
export class AlmacenComponent implements OnInit{
    @ViewChild("containerFormulario", {read: ViewContainerRef}) containerFormulario: any;

    consulta: boolean = false;
    dtOptions: any = {};
    dtTrigger: Subject<any> = new Subject<any>();
    Almacen: InventarioViewModel[] = [];
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
        const response: any = await this._rest.Get("/almacen/1");
        if (!response.error){
            this.Almacen = [];
            this.Almacen = response.data;
            this.Almacen.map(p => {
                let fechaCompraPartida = p.fechaCompra?.split(" ");
                let fechaVencimientoPartida = p.fechaVencimiento?.split(" ");
                p.fechaCompra = fechaCompraPartida![0];
                p.fechaVencimiento = fechaVencimientoPartida![0];
            });
            this.dtTrigger.next(null);
        }
        this.Loading = false;
    }

    Formulario(accionId: number, c: InventarioViewModel | null){
        let accion: string = "";
        switch (accionId){
            case 1:
                accion = "Agregar al";
                break;
            case 2:
                accion = "Editar";
                break;
        }
        this.CargarContenedorFormulario({accion: accion, c: c})
    }

    CargarContenedorFormulario(data: {accion: string, c: InventarioViewModel | null}){
        this.consulta = true;
        this.containerFormulario.clear();
        const factory: ComponentFactory<any> = this._cfr.resolveComponentFactory(FormAlmacenComponent);
        var ref: ComponentRef<any> = this.containerFormulario.createComponent(factory);
        ref.instance.accion = data.accion;
        ref.instance.Almacen = data.c;
        ref.instance.output.subscribe((cambio: boolean) => {
            this.consulta = false;
            ref.destroy();
            if (cambio){
                window.location.reload();
            }
        });
    }

    async Eliminar(id: number){
        let responseSwal = await Swall.fire({
            icon: "info",
            title: "¡Aviso!",
            text: "¿Estás seguro que quieres eliminar este producto?",
            showCancelButton: true,
            focusConfirm: false,
            confirmButtonText: "Si",
            confirmButtonAriaLabel: "Si",
            cancelButtonText: "No",
            cancelButtonAriaLabel: "No"
        });
        
        if (responseSwal.dismiss){
            return;
        }

        const response: any = await this._rest.Delete("/almacen/" + id);

        if (!response.error){
            await Swall.fire({
                icon: "success",
                title: "Productos eliminado",
                text: response.message,
                showConfirmButton: false,
                timer: 3000
            });
            window.location.reload();
        }
    }

    Regresar(){
        this.router.navigate(["menu/inicio"]);
    }
}