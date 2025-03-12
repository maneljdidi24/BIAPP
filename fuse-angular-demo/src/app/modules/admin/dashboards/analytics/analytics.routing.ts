import { Route } from '@angular/router';
import { AnalyticsComponent } from 'app/modules/admin/dashboards/analytics/analytics.component';
import { AnalyticsResolver } from 'app/modules/admin/dashboards/analytics/analytics.resolvers';
import { PowerBIComponent } from '../power-bi/power-bi.component';

export const analyticsRoutes: Route[] = [
    {
        path     : 'BI',
        component: AnalyticsComponent,
        resolve  : {
            data: AnalyticsResolver
        }
    },
    {
        path     : ':Powerbi',
        component: PowerBIComponent,

    }
];
