import { Route } from '@angular/router';
import { UserManagementComponent } from './user-management.component';


export const UserManagementRoutingModule: Route[] = [
    {
        path     : '',
        component: UserManagementComponent
    }
];