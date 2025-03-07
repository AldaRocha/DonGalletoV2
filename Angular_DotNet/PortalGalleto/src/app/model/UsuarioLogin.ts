export class UsuarioLogin{
    Pin: string;

    constructor(val: UsuarioLogin) {
        this.Pin = val.Pin ? val.Pin : "";
    }

    toJson(){
        return {
            Pin: this.Pin
        }
    }
}