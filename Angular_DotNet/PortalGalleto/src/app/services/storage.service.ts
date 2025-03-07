import { Injectable } from "@angular/core";

@Injectable()
export class StorageService{
    perfix: string = 'HM0987';
    parts: any = {};

    constructor() {
        if (localStorage.getItem(this.perfix + '_MJSDUDF76dHDGFnd')){
            this.parts = JSON.parse(this.binaryToString(localStorage.getItem(this.perfix + '_MJSDUDF76dHDGFnd')));
        }
    }

    setItem(name: any, value: any){
        let parts = value.split('.');
        this.parts[name] = [];
        parts.map((part: any, i: any) => {
            if (i > 0){
                part = '.' + part;
            }
            let token = this.makeid(20);
            this.parts[name].push(this.getName(token));
            localStorage.setItem(this.getName(token), this.stringToBinary(part));
        })
        this.save();
    }

    makeid(length: any){
        var result = '';
        var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        var charactersLength = characters.length;
        for ( var i = 0; i < length; i++ ) {
           result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        return result;
    }

    getItem(name: any){
        let chunks = this.getChunk(name);
        if(!chunks){
            return "";
        }
        let binary = '';
        chunks.map((chunk: any) => {
            binary += localStorage.getItem(chunk);
        });
        return this.binaryToString(binary);
    }

    getChunk(name: any){
        if (localStorage.getItem(this.perfix + '_MJSDUDF76dHDGFnd')){
            let parse = JSON.parse(this.binaryToString(localStorage.getItem(this.perfix + '_MJSDUDF76dHDGFnd')));
            if (parse[name]){
                return parse[name];
            }
        }
        return null;
    }

    removeItem(name: any){
        let chunks = this.getChunk(name);
        if (chunks){
            delete this.parts[name];
            chunks.map((chunk: any) => {
                localStorage.removeItem(chunk);
            });
        }
        this.save();
    }

    save(){
        let data = Object.assign({}, localStorage);
        localStorage.clear();
        Object.keys(data).map((storage: any) => {
            Object.keys(this.parts).map((part: any) => {
                this.parts[part].map((key: any) => {
                    if (key == storage){
                        localStorage.setItem(storage, data[storage]);
                    }
                });
            });
        });
        localStorage.setItem(this.perfix + '_MJSDUDF76dHDGFnd', this.stringToBinary(JSON.stringify(this.parts)));
    }

    stringToBinary(input: any){
        var characters = input.split('');
        return characters.map(function (char: any){
            const binary = char.charCodeAt(0).toString(2);
            const pad = Math.max(8 - binary.length, 0);
            return '0'.repeat(pad) + binary;
        }).join('');
    }

    binaryToString(input: any){
        let bytesLeft = input;
        let result = '';
        while (bytesLeft.length){
            const byte = bytesLeft.substr(0, 8);
            bytesLeft = bytesLeft.substr(8);
            result += String.fromCharCode(parseInt(byte, 2));
        }
        return result;
    }

    getName(name: any){
        return this.perfix + '_' + name;
    }

    clear(){
        this.parts = {};
        localStorage.clear();
    }
}