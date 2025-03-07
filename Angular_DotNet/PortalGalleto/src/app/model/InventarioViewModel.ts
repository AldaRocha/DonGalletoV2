import { MedidaViewModel } from "./MedidaViewModel";

export class InventarioViewModel{
    id: number;
    nombre: string | null;
    fechaCompra: string | null;
    fechaVencimiento: string | null;
    activo: number | null;
    cantidad: number;
    precio: number;
    porcentaje: number;
    proveedor: string | null;
    idMedida: number;
    medida: MedidaViewModel | null;

    constructor(val: InventarioViewModel){
        this.id = val.id ? val.id : 0;
        this.nombre = val.nombre ? val.nombre : null;
        this.fechaCompra = val.fechaCompra ? val.fechaCompra : null;
        this.fechaVencimiento = val.fechaVencimiento ? val.fechaVencimiento : null;
        this.activo = val.activo ? (val.activo ? 1 : 0) : null;
        this.cantidad = val.cantidad ? val.cantidad : 0;
        this.precio = val.precio ? val.precio : 0;
        this.porcentaje = val.porcentaje ? val.porcentaje : 0;
        this.proveedor = val.proveedor ? val.proveedor : null;
        this.idMedida = val.idMedida ? val.idMedida : 0;
        this.medida = val.medida ? val.medida : null;
    }
}