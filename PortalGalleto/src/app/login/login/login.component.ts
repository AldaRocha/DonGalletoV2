import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { UsuarioLogin } from 'src/app/model/UsuarioLogin';
import { RestService } from 'src/app/services/rest.service';
import { StorageService } from 'src/app/services/storage.service';
import Swall from "sweetalert2";

@Component({
  selector: 'login-root',
  templateUrl: './login.component.html',
  styleUrls: ['.//login.component.scss']
})
export class LoginComponent implements OnInit {
  FormLogin!: FormGroup;
  Loading: boolean = false;

  constructor(private _fb: FormBuilder, public _rest: RestService, public storage: StorageService, private _router: Router){

  }

  ngOnInit(): void {
      this.FormLogin = this._fb.group({
        Pin: ["", Validators.required]
      })
  }

  ModificarPin(Accion: number, Caracter: string){
    let valor = this.FormLogin.get("Pin")?.value.toString();
    switch (Accion){
      case 0:
        if (valor.length > 0){
          this.FormLogin.get("Pin")?.setValue(valor.substring(0, valor.length -1));
        }
        break;
      case 1:
        if (valor.length < 4){
          this.FormLogin.get("Pin")?.setValue(valor + Caracter);
        }
        break;
      default:
        break;
    }
  }

  async Ingresar(){
    this.Loading = true;
    const data: UsuarioLogin = new UsuarioLogin(this.FormLogin.value);
    let datos = data.toJson();
    const response: any = await this._rest.Post("auth/login", datos, false, false);
    if (!response.error){
      this.storage.setItem('dongalleto-oauth', response);
      this._router.navigate(['/menu/inicio']);
    } else{
      Swall.fire({
        icon: "warning",
        title: "Error al ingresar",
        text: "Pin incorrecto",
        showConfirmButton: false,
        timer: 3000
    });
    }
    this.Loading = false;
  }
}
