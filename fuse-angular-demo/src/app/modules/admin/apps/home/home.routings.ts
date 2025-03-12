import { NgModule } from '@angular/core';
import { Route } from '@angular/router';
import { HomeComponent } from './home.component';


export const homeRoutes: Route[] = [
    {
        path      : '',
        pathMatch : 'full',
        redirectTo: 'h'
    },
    {
        path     : 'h',
        component: HomeComponent
    }
];