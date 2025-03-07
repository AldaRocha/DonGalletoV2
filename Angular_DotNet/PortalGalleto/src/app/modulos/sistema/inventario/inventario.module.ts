import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { InventarioRoutingModule } from "./inventario-routing.module";
import { InventarioComponent } from "./inventario/inventario.component";

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        FormsModule,
        InventarioRoutingModule
    ],
    declarations: [
        InventarioComponent
    ]
})
export class InventarioModule{
    
}