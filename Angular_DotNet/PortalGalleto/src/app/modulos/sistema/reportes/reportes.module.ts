import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { ReportesRoutingModule } from "./reportes-routing.module";
import { ReportesComponent } from "./reportes/reportes.component";

@NgModule({
    imports: [
        CommonModule,
        ReactiveFormsModule,
        FormsModule,
        ReportesRoutingModule
    ],
    declarations: [
        ReportesComponent
    ]
})
export class ReportesModule{
    
}