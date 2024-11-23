import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { RecetasRoutingModule } from "./recetas-routing.module";
import { RecetasComponent } from "./recetas/recetas.component";

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        FormsModule,
        RecetasRoutingModule
    ],
    declarations: [
        RecetasComponent
    ]
})
export class RecetasModule{
    
}