import { NgModule } from "@angular/core";
import { MenuComponent } from "./menu.component";
import { InicioComponent } from "../modulos/inicio/inicio.component";
import { CommonModule } from "@angular/common";
import { MenuRoutingModule } from "./menu-routing.module";
import { FormsModule } from "@angular/forms";

@NgModule({
    imports: [
        CommonModule,
        MenuRoutingModule,
        FormsModule,
    ],
    providers: [

    ],
    declarations: [
        MenuComponent, InicioComponent
    ]
})
export class MenuModule{

}