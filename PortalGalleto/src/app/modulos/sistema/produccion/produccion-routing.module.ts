import { RouterModule, Routes } from "@angular/router";
import { ProduccionComponent } from "./produccion/produccion.component";
import { NgModule } from "@angular/core";

const routes: Routes = [
    { path: "", redirectTo: "produccion", pathMatch: "full" },
    { path: "produccion", component: ProduccionComponent }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class ProduccionRoutingModule{

}