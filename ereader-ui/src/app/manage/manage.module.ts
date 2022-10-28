import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ManageRoutingModule } from './manage.routing';
import { ManageComponent } from './manage.component';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { AccordionModule } from 'primeng/accordion';

import { CourseComponent } from './course/course.component';

@NgModule({
  declarations: [
    ManageComponent,
    CourseComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ManageRoutingModule,
    InputTextModule,
    ButtonModule,
    AccordionModule,
  ]
})
export class ManageModule { }
