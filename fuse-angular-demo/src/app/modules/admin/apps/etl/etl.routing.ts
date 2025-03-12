import { NgModule } from '@angular/core';
import { Route, RouterModule, Routes } from '@angular/router';
import { MainPageComponent } from './main-page/main-page.component';
import { SecondPageComponent } from './second-page/second-page.component';



export const Etlroutes: Route[] = [
  {
      path: 'sales',component: MainPageComponent
  },
  {
    path: 'purchasing',  component: SecondPageComponent
  }
];
