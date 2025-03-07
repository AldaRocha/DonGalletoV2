import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { ProduccionRoutingModule } from "./produccion-routing.module";
import { ProduccionComponent } from "./produccion/produccion.component";

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        FormsModule,
        ProduccionRoutingModule
    ],
    declarations: [
        ProduccionComponent
    ]
})
export class ProduccionModule{
    
}