import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PerformanceComponent } from './performance/performance.component';
import { RouterModule } from '@angular/router';
import { sustainabilityRoutes } from './sustainability.routing';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatMenuModule } from '@angular/material/menu';
import { MatRippleModule } from '@angular/material/core';
import { MatSelectModule } from '@angular/material/select';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatTooltipModule } from '@angular/material/tooltip';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {MatExpansionModule} from '@angular/material/expansion';
import { MatListModule } from '@angular/material/list';
import { FuseAlertModule } from '@fuse/components/alert';

import { MatDividerModule } from '@angular/material/divider';
import { AddPerformanceComponent } from './add-performance/add-performance.component';
import { AddTargetsComponent } from './add-targets/add-targets.component';
import { MainComponent } from './main/main.component';


@NgModule({
    declarations: [
        PerformanceComponent,
        AddPerformanceComponent,
        AddTargetsComponent,
        MainComponent
    ],
    imports: [
        CommonModule, MatFormFieldModule,
        HttpClientModule,
        FormsModule,
        MatExpansionModule,
        ReactiveFormsModule,
        MatButtonModule,
        MatCheckboxModule,
        MatIconModule,
        MatMenuModule,
        MatListModule,
        MatButtonModule,
        MatCheckboxModule,
        MatDividerModule,
        MatFormFieldModule,
        MatIconModule,
        MatInputModule,
        MatMenuModule,
        MatSelectModule,
        MatSelectModule,
        RouterModule.forChild(sustainabilityRoutes),
        FuseAlertModule
    ]
})
export class SustainabilityModule { }
