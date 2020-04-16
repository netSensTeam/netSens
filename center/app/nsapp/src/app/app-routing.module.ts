import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { NetworksComponent } from './networks/networks.component';
import { AboutComponent } from './about/about.component';

const routes: Routes = [
  {path:'', component:NetworksComponent},
  {path: 'about', component:AboutComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
