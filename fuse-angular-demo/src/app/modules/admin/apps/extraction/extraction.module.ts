import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatMenuModule } from '@angular/material/menu';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatRippleModule } from '@angular/material/core';
import { MatSortModule } from '@angular/material/sort';
import { MatSelectModule } from '@angular/material/select';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatTooltipModule } from '@angular/material/tooltip';
import { SharedModule } from 'app/shared/shared.module';
import { extractionRoutes } from './extraction.routing';
import { CreationComponent } from './creation/creation.component';
import { DisplayComponent } from './display/display.component';
import { RouterModule } from '@angular/router';
import {MatCardModule} from '@angular/material/card';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import {MatTableModule} from '@angular/material/table';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FullCalendarModule } from '@fullcalendar/angular';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import {DragDropModule} from '@angular/cdk/drag-drop';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import { SelectionComponent } from './selection/selection.component';
import {MatExpansionModule} from '@angular/material/expansion';
import { MatDialogModule } from '@angular/material/dialog';
import { ModalWindowComponent } from './modal-window/modal-window.component';
import { FuseCardModule } from "../../../../../@fuse/components/card/card.module";
import { NgxPaginationModule } from 'ngx-pagination';
import { FuseAlertModule } from '@fuse/components/alert';
import { ReportAppCardComponent } from './report-app-card/report-app-card.component';
import { SalesreportComponent } from './salesreport/salesreport.component';





@NgModule({
    declarations: [
        CreationComponent,
        DisplayComponent,
        SelectionComponent,
        ReportAppCardComponent,
        ModalWindowComponent,
        SalesreportComponent
    ],
    providers: [LiveAnnouncer],
    imports: [
        CommonModule,
        RouterModule.forChild(extractionRoutes),
        HttpClientModule,
        FormsModule,
        NgxPaginationModule,
        MatDialogModule,
        DragDropModule,
        MatCardModule,
        MatExpansionModule,
        MatDatepickerModule,
        MatNativeDateModule,
        ReactiveFormsModule,
        MatButtonModule,
        MatCheckboxModule,
        MatFormFieldModule,
        MatIconModule,
        MatInputModule,
        MatMenuModule,
        MatTableModule,
        MatPaginatorModule,
        MatProgressBarModule,
        MatRippleModule,
        MatSortModule,
        MatSelectModule,
        MatSlideToggleModule,
        MatTooltipModule,
        FullCalendarModule,
        FuseAlertModule,
        SharedModule,
        FuseCardModule
    ]
})
export class ExtractionModule { }
