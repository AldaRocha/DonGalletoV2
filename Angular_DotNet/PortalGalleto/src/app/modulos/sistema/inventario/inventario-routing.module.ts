import { RouterModule, Routes } from "@angular/router";
import { InventarioComponent } from "./inventario/inventario.component";
import { NgModule } from "@angular/core";

const routes: Routes = [
    { path: "", redirectTo: "inventario", pathMatch: "full" },
    { path: "inventario", component: InventarioComponent }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class InventarioRoutingModule{

}