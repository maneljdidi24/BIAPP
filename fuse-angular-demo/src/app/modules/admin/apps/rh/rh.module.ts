import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RH_routes } from './rh.routing';
import { AddEmployeeComponent } from './add-employee/add-employee.component';
import { DisplayEmployeeComponent } from './display-employee/display-employee.component';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatSelectModule } from '@angular/material/select';

import { FuseScrollResetModule } from '@fuse/directives/scroll-reset';
import { FuseScrollbarModule } from '@fuse/directives/scrollbar';
import { FuseAlertModule } from '@fuse/components/alert';

import {MatTableModule} from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator/paginator-module';
import { MatSortModule } from '@angular/material/sort';
import { MatRadioModule } from '@angular/material/radio';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatChipsModule } from '@angular/material/chips';
import { MatDividerModule } from '@angular/material/divider';
import { MatInputModule } from '@angular/material/input';
import { MatMomentDateModule } from '@angular/material-moment-adapter';
import { FuseHighlightModule } from '@fuse/components/highlight';
import { FilterEmployeeComponent } from './filter-employee/filter-employee.component';
import { OverlayModule } from '@angular/cdk/overlay';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatDialogModule } from '@angular/material/dialog';

@NgModule({
  declarations: [
    AddEmployeeComponent,
    DisplayEmployeeComponent,
    FilterEmployeeComponent
  ],
  imports: [
    CommonModule, RouterModule.forChild(RH_routes),HttpClientModule, MatFormFieldModule,
    FormsModule,MatTableModule,
    MatExpansionModule,
    ReactiveFormsModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatButtonModule,MatSortModule,
    MatCheckboxModule,
    MatIconModule,
    OverlayModule,
    MatSidenavModule,
        MatSlideToggleModule,
    MatMenuModule,MatDialogModule,
            MatButtonModule,
        MatButtonToggleModule,
        MatChipsModule,
        MatDatepickerModule,
        FuseScrollResetModule,
        FuseScrollbarModule,
        MatDividerModule,
        MatFormFieldModule,
        MatIconModule,
        MatInputModule,
        MatMomentDateModule,
        FuseHighlightModule,
    MatListModule, 
    MatSelectModule,
    MatRadioModule,
/*     NgClass, NgSwitch, NgSwitchCase, BadgeComponent, NgSwitchDefault
    MatSelectModule, */
    FuseAlertModule
  ]
})
export class RhModule { }
