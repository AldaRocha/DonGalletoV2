import { RouterModule, Routes } from "@angular/router";
import { VentasComponent } from "./ventas/ventas.component";
import { NgModule } from "@angular/core";

const routes: Routes = [
    { path: "", redirectTo: "ventas", pathMatch: "full" },
    { path: "ventas", component: VentasComponent }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class VentasRoutingModule{

}