import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Router } from "@angular/router";
import { JwtHelperService } from "@auth0/angular-jwt";
import { environment } from "src/environments/environment";
import { StorageService } from "./storage.service";
import { AuthData } from "../model/AuthData";
import * as CryptoJS from 'crypto-js';

export interface Response {
    message?: string;
    token?: any;
    error?: boolean;
}

@Injectable()
export class RestService{
    RestApi: string = environment.url;
    Version: string = 'v1';
    Secret: string = 'DonGalleto2024';
    SVP: any = '';
    headers: HttpHeaders;

    constructor(private _http: HttpClient, private jwt: JwtHelperService, public router: Router, public storage: StorageService){
        this.headers = new HttpHeaders();
        if (this.storage.getItem('dongalleto-oauth')){
            let data: AuthData = new AuthData(this.jwt.decodeToken(this.storage.getItem('dongalleto-oauth')));
            this.headers = this.headers.set('Authorization', data.Bearer);
        }
    }

    setHeaders(){
        this.headers = new HttpHeaders();
        if (this.storage.getItem('dongalleto-oauth')) {
            let data: AuthData = new AuthData(this.jwt.decodeToken(this.storage.getItem('dongalleto-oauth')));
            this.headers = this.headers.set('Authorization', data.Bearer);
        }
    }

    JsonToParams(json: any){
        return Object.keys(json).map(function (k){
            return encodeURIComponent(k) + '=' + encodeURIComponent(json[k]);
        }).join('&');
    }

    Decode(token: any){
        return this.jwt.decodeToken(token);
    }

    Post(route: any, data: any, version = true, decode = true){
        this.setHeaders();
        return new Promise((resolve, reject) => {
            let token = this.sign(data, this.Secret);
            let v = '';
            if (version){
                v = this.Version;
            }
            this._http.post<Response>(this.RestApi + v + route, {token: token}, {
                headers: this.headers,
                observe: 'response'
            }).subscribe((data) => {
                let message = data.body?.message;
                let token = data.body?.token;
                if (data.status == 200){
                    if (!decode){
                        if (message != null){
                            resolve({message: message, error: true, data: null});
                        } else{
                            resolve(token);
                        }
                    } else{
                        resolve({message: message, data: this.Decode(token)});
                    }
                } else{
                    resolve({error: true, message: message});
                }
            }, err => {
                if (err.status == 401){
                    this.storage.clear();
                    this.router.navigate(['login/login']);
                    resolve({error: true, message: "No tienes permiso para realizar esta petición"});
                } else{
                    console.log(err);
                    resolve({error: true, message: err});
                }
            });
        });
    }

    Put(route: any, data: any, version = true, decode = true){
        this.setHeaders();
        return new Promise((resolve, reject) => {
            let token = this.sign(data, this.Secret);
            let v = '';
            if (version) {
                v = this.Version;
            }
            this._http.put<Response>(this.RestApi + v + route, {token: token}, {
                headers: this.headers,
                observe: 'response'
            }).subscribe((data) => {
                let message = data.body?.message;
                let token = data.body?.token;
                if (data.status == 200){
                    if (!decode){
                        resolve(token);
                    } else{
                        resolve({message: message, data: this.Decode(token)});
                    }
                } else{
                    resolve({error: true, message: message});
                }
            }, err => {
                if (err.status == 401){
                    this.storage.clear();
                    this.router.navigate(['login/login']);
                    resolve({error: true, message: "No tienes permiso para realizar esta petición"});
                } else if (err.status == 409){
                    resolve({error: true, message: err.error.message});
                } else{
                    console.log(err);
                    resolve({error: true, message: err});
                }
            });
        });
    }

    Delete(route: any, version = true, decode = true){
        this.setHeaders();
        return new Promise((resolve, reject) => {
            let v = '';
            if (version) {
                v = this.Version;
            }
            this._http.delete<Response>(this.RestApi + v + route, {
                headers: this.headers,
                observe: 'response'
            }).subscribe((data) => {
                let message = data.body?.message;
                let token = data.body?.token;
                if (data.status == 200){
                    if (!decode){
                        resolve(token);
                    } else{
                        resolve({message: message, data: this.Decode(token)});
                    }
                } else{
                    resolve({error: true, message: message});
                }
            }, err => {
                if (err.status == 401){
                    this.storage.clear();
                    this.router.navigate(['login/login']);
                    resolve({error: true, message: "No tienes permiso para realizar esta petición"});
                } else{
                    console.log(err);
                    resolve({error: true, message: err});
                }
            });
        });
    }

    Get(route: any, version = true){
        this.setHeaders();
        return new Promise((resolve, reject) => {
            let v = '';
            if (version) {
                v = this.Version;
            }
            this._http.get<Response>(this.RestApi + v + route, {
                headers: this.headers,
                observe: 'response'
            }).pipe().subscribe((data) => {
                let message = data.body?.message;
                let token = data.body?.token;
                if (data.status == 200){
                    resolve({message: message, data: this.Decode(token)});
                } else{
                    resolve({error: true, message: message});
                }
            }, err => {
                if (err.status == 401){
                    this.storage.clear();
                    this.router.navigate(['login/login']);
                    resolve({error: true, message: "No tienes permiso para realizar esta petición"});
                } else{
                    console.log(err);
                    resolve({error: true, message: err});
                }
            });
        });
    }

    sign(data: any, secret: any): string {
        const header = {
            alg: 'HS256',
            typ: 'JWT',
        };
    
        const stringifiedHeader = CryptoJS.enc.Utf8.parse(JSON.stringify(header));
        const encodedHeader = this.base64url(stringifiedHeader);
    
        const stringifiedData = CryptoJS.enc.Utf8.parse(JSON.stringify(data));
        const encodedData = this.base64url(stringifiedData);
    
        const token = `${encodedHeader}.${encodedData}`;
    
        const signature = CryptoJS.HmacSHA256(token, secret);
        const encodedSignature = this.base64url(signature);
    
        return `${token}.${encodedSignature}`;
    }

    base64url(source: CryptoJS.lib.WordArray): string {
        let encodedSource = CryptoJS.enc.Base64.stringify(source);
        encodedSource = encodedSource.replace(/=+$/, '');
        encodedSource = encodedSource.replace(/\+/g, '-');
        encodedSource = encodedSource.replace(/\//g, '_');
        return encodedSource;
    }
}
