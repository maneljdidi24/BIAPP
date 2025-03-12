import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';


import { MainPageComponent } from './main-page/main-page.component';
import { RouterModule } from '@angular/router';
import { Etlroutes } from './etl.routing';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatRadioModule } from '@angular/material/radio';
import { MatSelectModule } from '@angular/material/select';
import { MatStepperModule } from '@angular/material/stepper';
import { SharedModule } from 'app/shared/shared.module';
import { FuseCardModule } from "../../../../../@fuse/components/card/card.module";
import { SecondPageComponent } from './second-page/second-page.component';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';



@NgModule({
    declarations: [
        MainPageComponent,
        SecondPageComponent
    ],
    imports: [
        CommonModule,
        RouterModule.forChild(Etlroutes),
        MatButtonModule,
        MatCheckboxModule,
        MatFormFieldModule,
        ReactiveFormsModule,
        FormsModule,
        MatProgressSpinnerModule,
        MatIconModule,
        MatInputModule,
        MatRadioModule,
        MatSelectModule,
        MatDatepickerModule,
        MatNativeDateModule,
        MatStepperModule,
        SharedModule,
        FuseCardModule
    ]
})
export class ETLModule { }


