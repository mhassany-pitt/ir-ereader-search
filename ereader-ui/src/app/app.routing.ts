import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: '', loadChildren: () => import('./dashboard/dashboard.module').then(m => m.DashboardModule) },
  { path: 'reader', loadChildren: () => import('./reader/reader.module').then(m => m.ReaderModule) },
  { path: 'manage', loadChildren: () => import('./manage/manage.module').then(m => m.ManageModule) },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
