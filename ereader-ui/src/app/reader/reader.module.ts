import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { NgAisModule } from 'angular-instantsearch';

import { ReaderRoutingModule } from './reader.routing';
import { ReaderComponent } from './reader.component';
import { InputTextModule } from 'primeng/inputtext';

@NgModule({
  declarations: [
    ReaderComponent,
  ],
  imports: [
    NgAisModule.forRoot(),
    CommonModule,
    FormsModule,
    HttpClientModule,
    ReaderRoutingModule,
    InputTextModule,
  ]
})
export class ReaderModule { }
