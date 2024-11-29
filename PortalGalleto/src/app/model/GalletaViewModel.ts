import { MedidaViewModel } from "./MedidaViewModel";

export class GalletaViewModel{
    id: number;
    nombre: string | null;
    cantidad: number;
    precioVenta: number;
    precioProduccion: number;
    imagen: string | null;
    idMedida: number;
    medida: MedidaViewModel | null;

    constructor(val: GalletaViewModel){
        this.id = val.id ? val.id : 0;
        this.nombre = val.nombre ? val.nombre : null;
        this.cantidad = val.cantidad ? val.cantidad : 0;
        this.precioVenta = val.precioVenta ? val.precioVenta : 0;
        this.precioProduccion = val.precioProduccion ? val.precioProduccion : 0;
        this.imagen = val.imagen ? val.imagen : null;
        this.idMedida = val.idMedida ? val.idMedida : 0;
        this.medida = val.medida ? val.medida : null;
    }
}