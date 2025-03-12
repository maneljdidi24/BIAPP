
import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { DatePipe } from '@angular/common';

import { MatDialogRef } from '@angular/material/dialog';
import { FuseConfirmationService } from '@fuse/services/confirmation';
import { DataService } from 'app/service.service';


@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.scss']
})
export class MainPageComponent implements OnInit {
  plant: string = ''; // Variable pour stocker la valeur sélectionnée
  selectedDate1: any; // Variable pour stocker la date sélectionnée
  selectedDate2: any;
  data1:any; data:any;
  
  project: any;
  extractionForm: FormGroup;
  composeForm: FormGroup;
  loading: boolean = false;
  Title: any;
  loadingData: boolean = false;
  progressValue: number = 0;
  p: any;
  configForm!: FormGroup;

  progress: number = 0;
  msg: string;

  usertype:string;
  constructor(private route: ActivatedRoute,  private fb: FormBuilder,
    private router: Router,private dataService: DataService,
    private _formBuilder: FormBuilder,
    private _fuseConfirmationService: FuseConfirmationService) { }



  ngOnInit() {
    this.extractionForm = this.fb.group({
      plant: ['', Validators.required],
      startDate: [null, Validators.required],
      endDate: [null, Validators.required],
    });

    this.usertype = localStorage.getItem("type")
  }

  formatDate(date: Date): string {
    const datePipe = new DatePipe('en-US');
    return datePipe.transform(date, 'yyyy-MM-dd') || '';
  }
  





 

  onSubmit() {
    alert (this.formatDate(this.selectedDate1))
    const requestData = { region: this.plant, date1: this.formatDate(this.selectedDate1) , date2: this.formatDate(this.selectedDate2)};

    //manel 
   
    this.dataService.extractsales(requestData).subscribe(data=>{
      this.data = data
      alert(this.data.region + ', ' + this.data.date1);
      console.log(this.data);
    })


  }





  error(msg:any) {
    this.configForm = this._formBuilder.group({
      title: 'Error!',
      message: msg,
      icon: this._formBuilder.group({
        show: true,
        name: 'heroicons_outline:exclamation',
        color: 'error' // Red color for error
      }),
      actions: this._formBuilder.group({
        confirm: this._formBuilder.group({
          show: true,
          label: 'OK',
          color: 'primary'
        }),
        cancel: this._formBuilder.group({
          show: false, // Hide the 'Close' button for error message
          label: 'Close',
          color: 'warn'
        })
      }),
      dismissible: true
    });
  }

  success(msg:any) {
    this.configForm = this._formBuilder.group({
      title: 'Success!',
      message: msg,
      icon: this._formBuilder.group({
        show: true,
        name: 'heroicons_outline:check',
        color: 'success' // Green color for success
      }),
      actions: this._formBuilder.group({
        confirm: this._formBuilder.group({
          show: false, // Hide the 'Remove' button for success message
          label: 'Remove',
          color: 'warn'
        }),
        cancel: this._formBuilder.group({
          show: true,
          label: 'Close',
          color: 'primary' // Use a primary color for the 'Close' button
        })
      }),
      dismissible: true
    });

  }

}
