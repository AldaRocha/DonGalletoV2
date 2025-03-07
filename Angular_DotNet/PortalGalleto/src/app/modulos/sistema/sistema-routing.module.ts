import { RouterModule, Routes } from "@angular/router";
import { AlmacenModule } from "./almacen/almacen.module";
import { NgModule } from "@angular/core";
import { InventarioModule } from "./inventario/inventario.module";
import { ProduccionModule } from "./produccion/produccion.module";
import { RecetasModule } from "./recetas/recetas.module";
import { ReportesModule } from "./reportes/reportes.module";
import { VentasModule } from "./ventas/ventas.module";

const routes: Routes = [
    { path: "", redirectTo: "almacen", pathMatch: "full" },
    { path: "almacen", loadChildren: () => AlmacenModule },
    { path: "inventario", loadChildren: () => InventarioModule },
    { path: "produccion", loadChildren: () => ProduccionModule },
    { path: "recetas", loadChildren: () => RecetasModule },
    { path: "reportes", loadChildren: () => ReportesModule },
    { path: "ventas", loadChildren: () => VentasModule }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class SistemaRoutingModule {
    
}