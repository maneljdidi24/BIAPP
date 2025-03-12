import { NgModule } from '@angular/core';
import { Route } from '@angular/router';
import { DisplayComponent } from './display/display.component';
import { SelectionComponent } from './selection/selection.component';
import { SalesreportComponent } from './salesreport/salesreport.component';


export const extractionRoutes: Route[] = [
    
    {
        path: '',pathMatch : 'full',component: SelectionComponent
    },
    {
        path: 'report/:project',  component: DisplayComponent
    },
    {
        path: 'sales/:id',  component: SalesreportComponent
    }

];
