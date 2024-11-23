import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { AlmacenRoutingModule } from "./almacen-routing.module";
import { AlmacenComponent } from "./almacen/almacen.component";

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        FormsModule,
        AlmacenRoutingModule
    ],
    declarations: [
        AlmacenComponent
    ]
})
export class AlmacenModule {

}