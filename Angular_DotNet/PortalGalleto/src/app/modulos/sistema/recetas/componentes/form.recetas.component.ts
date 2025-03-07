import { LocationStrategy } from "@angular/common";
import { Component, EventEmitter, Input, OnInit, Output } from "@angular/core";
import { AbstractControl, FormBuilder, FormGroup, Validators } from "@angular/forms";
import { GalletaViewModel } from "src/app/model/GalletaViewModel";
import { InventarioViewModel } from "src/app/model/InventarioViewModel";
import { MedidaViewModel } from "src/app/model/MedidaViewModel";
import { RecetaViewModel } from "src/app/model/RecetaViewModel";
import { RestService } from "src/app/services/rest.service";
import Swall from "sweetalert2";

@Component({
    selector: "form-galleta-app",
    templateUrl: "./form.recetas.component.html",
    styleUrls: ["./form.recetas.component.scss"]
})
export class FormRecetasComponent implements OnInit{
    @Input() accion!: string;
    @Input() Galleta!: GalletaViewModel | null;
    @Output() output = new EventEmitter();

    cambio: boolean = false;
    FormGalleta!: FormGroup;
    Enviado = false;
    Receta = false;
    Medidas: MedidaViewModel[] = [];
    Almacen: InventarioViewModel[] = [];
    Loading: boolean = false;
    selectedImage!: string | ArrayBuffer | null;
    RecetaList: RecetaViewModel[] = [];

    constructor(private location: LocationStrategy, private _fb: FormBuilder, private _rest: RestService){
        history.pushState(null, "", window.location.href);
        this.location.onPopState(() => {
            this.Salir();
        });
    }

    ngOnInit(): void {
        this.IniciarForm();
        this.DatosIniciales();
        if (this.Galleta != null){
            this.Receta = true;
            this.selectedImage = this.Galleta.imagen;
            this.FormGalleta.patchValue(this.Galleta);
            this.BuscarReceta();
        }
    }

    get f(): { [key: string]: AbstractControl } { return this.FormGalleta.controls; }

    IniciarForm(){
        this.FormGalleta = this._fb.group({
            id: [0],
            nombre: [, Validators.required],
            cantidad: [, Validators.required],
            precioVenta: [, Validators.required],
            precioProduccion: [, Validators.required],
            imagen: [],
            pesoGalleta: [, Validators.required],
            idMedida: [, Validators.required]
        });
    }

    async DatosIniciales(){
        this.Loading = true;
        const response: any = await this._rest.Get("/medida");

        if (!response.error){
            this.Medidas = response.data;
        }

        const response2: any = await this._rest.Get("/almacen/1");

        if (!response2.error){
            this.Almacen = response2.data;
        }
        this.Loading = false;
    }

    async BuscarReceta(){
        this.Loading = true;
        const response: any = await this._rest.Get("/receta/" + this.Galleta?.id);

        if (!response.error){
            if (response.data){
                this.RecetaList = response.data;
            }
        }
    }

    onFileSelected(event: any) {
        const file: File = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = this.handleReaderLoaded.bind(this);
            reader.readAsDataURL(file);
        }
    }

    handleReaderLoaded(e: any) {
        this.selectedImage = e.target.result;
    }

    AgregarIngrediente(id: number){
        let input = document.getElementById("Inventario" + id) as HTMLInputElement;

        if (input){
            let inventario: InventarioViewModel = this.Almacen.find(p => p.id === id)!;
            this.RecetaList.push({id: 0, cantidad: parseFloat(input.value), idGalleta: this.Galleta!.id, galleta: this.Galleta, idInventario: id, inventario: inventario, idMedida: inventario.idMedida, medida: inventario.medida});
        }
    }

    QuitarReceta(index: number){
        this.RecetaList.splice(index, 1);
    }

    async Guardar(){
        this.Enviado = true;
        this.Loading = true;

        if (this.Galleta == null){
            if (this.FormGalleta.invalid){
                return;
            }

            if (!this.selectedImage) {
                return Swall.fire({
                        icon: "warning",
                        title: "Error al guardar",
                        text: "La imagen no puede ir vacía",
                        showConfirmButton: false,
                        timer: 3000
                        });
            }

            const base64Image = this.selectedImage.toString().split(",")[1];

            const data: GalletaViewModel = new GalletaViewModel(this.FormGalleta.value);
            data.imagen = base64Image;
            const response: any = await this._rest.Post("/galleta", data);

            if (!response.error){
                Swall.fire({
                    icon: "success",
                    title: "Galleta guardada",
                    text: "Datos guardados con exito",
                    showConfirmButton: false,
                    timer: 3000
                });
                this.cambio = true;
                this.Receta = true;
                this.Galleta = response.data;
            } else{
                Swall.fire({
                    icon: "warning",
                    title: "Error al guardar",
                    text: response.message,
                    showConfirmButton: false,
                    timer: 3000
                });
            }
        } else{
            if (this.FormGalleta.invalid){
                return;
            }

            if (!this.selectedImage) {
                return Swall.fire({
                            icon: "warning",
                            title: "Error al guardar",
                            text: "La imagen no puede ir vacía",
                            showConfirmButton: false,
                            timer: 3000
                        });
            }

            const base64Image = this.selectedImage.toString().split(",")[1];

            const data: GalletaViewModel = new GalletaViewModel(this.FormGalleta.value);
            data.imagen = base64Image;
            data.recetamodel = this.RecetaList;
            const response: any = await this._rest.Put("/galleta", data);

            if (!response.error){
                if (response.message == null){
                    await Swall.fire({
                                icon: "success",
                                title: "Galleta guardada",
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
        this.output.emit(this.cambio);
    }
}