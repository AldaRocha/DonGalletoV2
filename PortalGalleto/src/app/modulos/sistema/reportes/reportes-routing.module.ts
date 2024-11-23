import { RouterModule, Routes } from "@angular/router";
import { ReportesComponent } from "./reportes/reportes.component";
import { NgModule } from "@angular/core";

const routes: Routes = [
    { path: "", redirectTo: "reportes", pathMatch: "full" },
    { path: "reportes", component: ReportesComponent }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class ReportesRoutingModule{

}