import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { HomeComponent } from './home.component';
import { homeRoutes } from './home.routings';



@NgModule({
  declarations: [
    HomeComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(homeRoutes),
    HttpClientModule
    
  ],
  providers: [LiveAnnouncer],
})
export class homeModule { }
