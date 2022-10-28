import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ReaderRoutingModule } from './reader.routing';
import { ReaderComponent } from './reader.component';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    ReaderComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReaderRoutingModule
  ]
})
export class ReaderModule { }
