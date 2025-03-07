import { RouterModule, Routes } from "@angular/router";
import { MenuComponent } from "./menu.component";
import { InicioComponent } from "../modulos/inicio/inicio.component";
import { NgModule } from "@angular/core";
import { SistemaModule } from "../modulos/sistema/sistema.module";

const routes: Routes = [
    {
        path: "", component: MenuComponent, children: [
            {path: "inicio", component: InicioComponent},
            {path: "sistema", loadChildren: () => SistemaModule}
        ]
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class MenuRoutingModule{

}