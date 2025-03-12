import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { SharedModule } from 'app/shared/shared.module';
import { AnalyticsComponent } from 'app/modules/admin/dashboards/analytics/analytics.component';
import { analyticsRoutes } from 'app/modules/admin/dashboards/analytics/analytics.routing';

@NgModule({
    declarations: [
        AnalyticsComponent
    ],
    imports     : [
        RouterModule.forChild(analyticsRoutes),
        SharedModule
    ]
})
export class AnalyticsModule
{
}
