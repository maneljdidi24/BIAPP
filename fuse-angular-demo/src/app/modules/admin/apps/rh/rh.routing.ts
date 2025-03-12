import { NgModule } from '@angular/core';
import { RouterModule, Route } from '@angular/router';
import { DisplayComponent } from '../extraction/display/display.component';
import { DisplayEmployeeComponent } from './display-employee/display-employee.component';
import { AddEmployeeComponent } from './add-employee/add-employee.component';

export const RH_routes: Route[] = [
  {
    path: '', 
    children: [
      { path: 'display', component: DisplayEmployeeComponent },
      { path: 'add', component: AddEmployeeComponent }]
  }
];

/* @NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RhRoutingModule { } */

/* 
export const sustainabilityRoutes: Route[] = [
  {
  path: '', 
  children: [
    { path: 'performance', component: PerformanceComponent },
    { path: 'target', component: AddTargetsComponent },
    // Other child routes...
    { path: '', redirectTo: 'detail', pathMatch: 'full' }, // Default redirect
    { path: '**', redirectTo: 'detail' } // Handle 404
  ]
}
]; */