export class MedidaViewModel{
    id: number;
    nombre: string | null;

    constructor(val: MedidaViewModel){
        this.id = val.id ? val.id : 0;
        this.nombre = val.nombre ? val.nombre : null;
    }
}