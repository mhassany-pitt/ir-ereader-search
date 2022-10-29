import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

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
    HttpClientModule,
    ReaderRoutingModule
  ]
})
export class ReaderModule { }
