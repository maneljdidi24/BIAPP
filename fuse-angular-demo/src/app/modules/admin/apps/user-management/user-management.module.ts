import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UserManagementRoutingModule } from './user-management.routing';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatRadioModule } from '@angular/material/radio';
import { MatSelectModule } from '@angular/material/select';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { FuseAlertModule } from '@fuse/components/alert';
import { SharedModule } from 'app/shared/shared.module';
import { RouterModule } from '@angular/router';
import { UserManagementComponent } from './user-management.component';
import { AddUsersComponent } from './User/add-users/add-users.component';
import { DisplayUsersComponent } from './User/display-users/display-users.component';
import { EditUsersComponent } from './User/edit-users/edit-users.component';
import { AddProjectsComponent } from './Project/add-projects/add-projects.component';
import { EditProjectsComponent } from './Project/edit-projects/edit-projects.component';
import { DisplayProjectsComponent } from './Project/display-projects/display-projects.component';
import { AddPlantsComponent } from './Plant/add-plants/add-plants.component';
import { DisplayPlantsComponent } from './Plant/display-plants/display-plants.component';
import { EditPlantsComponent } from './Plant/edit-plants/edit-plants.component';
import { ManagePermissionsComponent } from './User/manage-permissions/manage-permissions.component';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDialogModule } from '@angular/material/dialog';
import { MatDividerModule } from '@angular/material/divider';
import { MatMenuModule } from '@angular/material/menu';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { FuseNavigationModule } from '@fuse/components/navigation';
import { FuseScrollResetModule } from '@fuse/directives/scroll-reset';
import { FuseScrollbarModule } from '@fuse/directives/scrollbar';
import { FuseFindByKeyPipeModule } from '@fuse/pipes/find-by-key';
import { QuillModule } from 'ngx-quill';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { DataService } from '../../../../service.service';
import { FuseCardModule } from "../../../../../@fuse/components/card/card.module";
import { AddUserAccessComponent } from './User/add-user-access/add-user-access.component';



@NgModule({
    declarations: [
        UserManagementComponent,
        AddUsersComponent,
        DisplayUsersComponent,
        EditUsersComponent,
        AddProjectsComponent,
        EditProjectsComponent,
        DisplayProjectsComponent,
        AddPlantsComponent,
        DisplayPlantsComponent,
        EditPlantsComponent,
        ManagePermissionsComponent,
        AddUserAccessComponent,
    ],
    providers: [DataService],
    imports: [
        CommonModule,
        RouterModule.forChild(UserManagementRoutingModule),
        MatButtonModule,
        HttpClientModule,
        FormsModule,
        MatFormFieldModule,
        MatIconModule,
        MatInputModule,
        MatRadioModule,
        MatSelectModule,
        MatSidenavModule,
        MatSlideToggleModule,
        FuseAlertModule,
        MatButtonModule,
        MatCheckboxModule,
        MatDialogModule,
        MatDividerModule,
        MatFormFieldModule,
        MatIconModule,
        MatInputModule,
        MatMenuModule,
        MatProgressBarModule,
        MatSelectModule,
        MatSidenavModule,
        FuseFindByKeyPipeModule,
        FuseNavigationModule,
        FuseScrollbarModule,
        FuseScrollResetModule,
        SharedModule,
        FuseCardModule
    ]
})
export class UserManagementModule { }
