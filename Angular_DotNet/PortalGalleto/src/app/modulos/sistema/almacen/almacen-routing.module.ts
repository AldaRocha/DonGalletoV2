import { RouterModule, Routes } from "@angular/router";
import { AlmacenComponent } from "./almacen/almacen.component";
import { NgModule } from "@angular/core";

const routes: Routes = [
    { path: "", redirectTo: "almacen", pathMatch: "full" },
    { path: "almacen", component: AlmacenComponent }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class AlmacenRoutingModule {
    
}