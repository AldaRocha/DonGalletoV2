import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { VentasRoutingModule } from "./ventas-routing.module";
import { VentasComponent } from "./ventas/ventas.component";

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        FormsModule,
        VentasRoutingModule
    ],
    declarations: [
        VentasComponent
    ]
})
export class VentasModule{

}