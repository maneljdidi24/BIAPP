import { NgModule } from '@angular/core';
import { Route } from '@angular/router';
import { PerformanceComponent } from './performance/performance.component';
import { AddTargetsComponent } from './add-targets/add-targets.component';
import { MainComponent } from './main/main.component';
import { AddPerformanceComponent } from './add-performance/add-performance.component';



export const sustainabilityRoutes: Route[] = [
    {
    path: '', 
    children: [
      { path: 'main', component: MainComponent },
      { path: 'main/performance', component: PerformanceComponent },
      { path: 'main/addP', component: AddPerformanceComponent },
      { path: 'target', component: AddTargetsComponent },
      // Other child routes...
      { path: '', redirectTo: 'detail', pathMatch: 'full' }, // Default redirect
      { path: '**', redirectTo: 'detail' } // Handle 404
    ]
}
];
