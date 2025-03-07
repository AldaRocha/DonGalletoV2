export class AuthData{
    Nombre!: string;
    Bearer!: string;

    constructor(data?: any) {
        if (data){
            this.Nombre = data.Nombre;
            this.Bearer = data.Bearer;
        }
    }
}