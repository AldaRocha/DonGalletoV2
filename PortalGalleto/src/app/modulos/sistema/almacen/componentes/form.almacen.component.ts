import { LocationStrategy } from "@angular/common";
import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";
import { AbstractControl, FormBuilder, FormGroup, Validators } from "@angular/forms";
import { InventarioViewModel } from "src/app/model/InventarioViewModel";
import { MedidaViewModel } from "src/app/model/MedidaViewModel";
import { RestService } from "src/app/services/rest.service";
import Swall from "sweetalert2";

@Component({
    selector: "form-almacen-app",
    templateUrl: "./form.almacen.component.html",
    styleUrls: ["./form.almacen.component.scss"]
})
export class FormAlmacenComponent implements OnInit{
    @Input() accion!: string;
    @Input() Almacen!: InventarioViewModel | null;
    @Output() output = new EventEmitter();

    cambio: boolean = false;
    agregar: boolean = false;
    FormGuardar!: FormGroup;
    Enviado = false;
    Medidas: MedidaViewModel[] = [];
    Compras: InventarioViewModel[] = [];
    index: number = -1;
    MostrarLimpiar: boolean = false;
    Loading: boolean = false;

    constructor(private location: LocationStrategy, private _fb: FormBuilder, private _rest: RestService){
        history.pushState(null, "", window.location.href);
        this.location.onPopState(() => {
            this.Salir();
        });
    }

    async ngOnInit() {
        this.IniciarForm();
        this.DatosIniciales();
        if (this.Almacen == null){
            this.agregar = true;
        } else{
            this.Almacen.fechaCompra = await this.ConvertirFecha(this.Almacen.fechaCompra!);
            this.Almacen.fechaVencimiento = await this.ConvertirFecha(this.Almacen.fechaVencimiento!);
            this.FormGuardar.patchValue(this.Almacen);
        }
    }

    get f(): { [key: string]: AbstractControl } { return this.FormGuardar.controls; }

    IniciarForm(){
        this.FormGuardar = this._fb.group({
            id: [0],
            nombre: [, Validators.required],
            fechaCompra: [, Validators.required],
            fechaVencimiento: [, Validators.required],
            cantidad: [, Validators.required],
            precio: [, Validators.required],
            porcentaje: [, Validators.required],
            proveedor: [, Validators.required],
            idMedida: [, Validators.required],
            activo: [1]
        });
    }

    async DatosIniciales(){
        this.Loading = true;
        const response: any = await this._rest.Get("/medida");

        if (!response.error){
            this.Medidas = response.data;
        }
        this.Loading = false;
    }

    async ConvertirFecha(fecha: string){
        const partes = fecha.split("/");
        const dia = partes[0];
        const mes = partes[1];
        const anio = partes[2];

        return `${anio}-${mes}-${dia}`;
    }

    Agregar(){
        this.Enviado = true;
        if (this.FormGuardar.invalid){
            return;
        }

        const data: InventarioViewModel = new InventarioViewModel(this.FormGuardar.value);
        if (this.index != -1){
            this.Compras[this.index] = data;
        } else{
            this.Compras.push(data);
        }
        this.Enviado = false;
        this.IniciarForm();
    }

    Editar(i: number, c: InventarioViewModel){
        this.index = i;
        this.MostrarLimpiar = true;
        this.FormGuardar.patchValue(c);
    }

    Limpiar (){
        this.index = -1;
        this.Enviado = false;
        this.MostrarLimpiar = false;
        this.IniciarForm();
    }

    Eliminar(index: number){
        this.Compras.splice(index, 1);
    }

    async Guardar(){
        this.Loading = true;
        if (this.Almacen == null){
            if (this.Compras.length == 0){
                return  Swall.fire({
                            icon: "warning",
                            title: "Error al guardar",
                            text: "No se puede registrar una lista vacia",
                            showConfirmButton: false,
                            timer: 3000
                        });
            }

            const response: any = await this._rest.Post("/almacen", this.Compras);

            if (!response.error){
                if (response.message == null){
                    Swall.fire({
                        icon: "success",
                        title: "Productos agregados",
                        text: "Datos guardados con exito",
                        showConfirmButton: false,
                        timer: 3000
                    });
                    this.cambio = true;
                    this.Salir();
                } else{
                    Swall.fire({
                        icon: "warning",
                        title: "Error al guardar",
                        text: response.message,
                        showConfirmButton: false,
                        timer: 3000
                    });
                }
            }
        } else{
            this.Enviado = true;
            if (this.FormGuardar.invalid){
                this.Loading = false;
                return Swall.fire({
                            icon: "warning",
                            title: "Error al guardar",
                            text: "Todos los datos deben de estar llenos",
                            showConfirmButton: false,
                            timer: 3000
                        });
            }

            const data: InventarioViewModel = new InventarioViewModel(this.FormGuardar.value);
            const response: any = await this._rest.Put("/almacen/" + data.id, data);

            if (!response.error){
                if (response.message == null){
                    await Swall.fire({
                        icon: "success",
                        title: "Productos agregados",
                        text: "Datos guardados con exito",
                        showConfirmButton: false,
                        timer: 3000
                    });
                    this.cambio = true;
                    this.Salir();
                } else{
                    Swall.fire({
                        icon: "warning",
                        title: "Error al guardar",
                        text: response.message,
                        showConfirmButton: false,
                        timer: 3000
                    });
                }
            }
        }
        return this.Loading = false;
    }

    Salir() {
        if (this.Almacen != null){
            const fechaCompraPartida = this.Almacen.fechaCompra?.split("-");
            const fechaVencimientoPartida = this.Almacen.fechaVencimiento?.split("-");

            this.Almacen.fechaCompra = fechaCompraPartida![2] + "/" + fechaCompraPartida![1] + "/" + fechaCompraPartida![0];
            this.Almacen.fechaVencimiento = fechaVencimientoPartida![2] + "/" + fechaVencimientoPartida![1] + "/" + fechaVencimientoPartida![0];
        }

        this.output.emit(this.cambio);
    }
}