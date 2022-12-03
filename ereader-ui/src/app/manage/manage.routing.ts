import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CourseComponent } from './course/course.component';
import { ManageComponent } from './manage.component';

const routes: Routes = [
  { path: '', component: ManageComponent },
  { path: 'new', component: CourseComponent },
  { path: ':id', component: CourseComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ManageRoutingModule { }
