import { MedidaViewModel } from "./MedidaViewModel";
import { RecetaViewModel } from "./RecetaViewModel";

export class GalletaViewModel{
    id: number;
    nombre: string | null;
    cantidad: number;
    precioVenta: number;
    precioProduccion: number;
    imagen: string | null;
    pesoGalleta: number;
    idMedida: number;
    medida: MedidaViewModel | null;

    recetamodel: RecetaViewModel[];

    constructor(val: GalletaViewModel){
        this.id = val.id ? val.id : 0;
        this.nombre = val.nombre ? val.nombre : null;
        this.cantidad = val.cantidad ? val.cantidad : 0;
        this.precioVenta = val.precioVenta ? val.precioVenta : 0;
        this.precioProduccion = val.precioProduccion ? val.precioProduccion : 0;
        this.imagen = val.imagen ? val.imagen : null;
        this.pesoGalleta = val.pesoGalleta ? val.pesoGalleta : 0;
        this.idMedida = val.idMedida ? val.idMedida : 0;
        this.medida = val.medida ? val.medida : null;

        this.recetamodel = [];
    }
}