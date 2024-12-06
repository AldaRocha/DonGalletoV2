import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { DataTablesModule } from "angular-datatables";
import { RecetasRoutingModule } from "./recetas-routing.module";
import { RecetasComponent } from "./recetas/recetas.component";
import { FormRecetasComponent } from "./componentes/form.recetas.component";

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        FormsModule,
        DataTablesModule,
        RecetasRoutingModule
    ],
    declarations: [
        RecetasComponent,

        FormRecetasComponent
    ]
})
export class RecetasModule{
    
}