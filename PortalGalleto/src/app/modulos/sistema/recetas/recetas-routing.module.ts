import { RouterModule, Routes } from "@angular/router";
import { RecetasComponent } from "./recetas/recetas.component";
import { NgModule } from "@angular/core";

const routes: Routes = [
    { path: "", redirectTo: "recetas", pathMatch: "full" },
    { path: "recetas", component: RecetasComponent }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class RecetasRoutingModule{

}