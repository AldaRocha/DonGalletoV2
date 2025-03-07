import { GalletaViewModel } from "./GalletaViewModel";
import { InventarioViewModel } from "./InventarioViewModel";
import { MedidaViewModel } from "./MedidaViewModel";

export class RecetaViewModel{
    id: number;
    cantidad: number;
    idGalleta: number;
    galleta: GalletaViewModel | null;
    idInventario: number;
    inventario: InventarioViewModel | null;
    idMedida: number;
    medida: MedidaViewModel | null;

    constructor(val: RecetaViewModel){
        this.id = val.id ? val.id : 0;
        this.cantidad = val.cantidad ? val.cantidad : 0;
        this.idGalleta = val.idGalleta ? val.idGalleta : 0;
        this.galleta = val.galleta ? val.galleta : null;
        this.idInventario = val.idInventario ? val.idInventario : 0;
        this.inventario = val.inventario ? val.inventario : null;
        this.idMedida = val.idMedida ? val.idMedida : 0;
        this.medida = val.medida ? val.medida : null;
    }
}