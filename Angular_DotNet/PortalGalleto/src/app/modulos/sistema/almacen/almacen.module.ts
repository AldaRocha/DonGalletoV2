import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { DataTablesModule } from "angular-datatables";
import { AlmacenRoutingModule } from "./almacen-routing.module";
import { AlmacenComponent } from "./almacen/almacen.component";
import { FormAlmacenComponent } from "./componentes/form.almacen.component";

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        FormsModule,
        DataTablesModule,
        AlmacenRoutingModule
    ],
    declarations: [
        AlmacenComponent,

        FormAlmacenComponent
    ]
})
export class AlmacenModule {

}