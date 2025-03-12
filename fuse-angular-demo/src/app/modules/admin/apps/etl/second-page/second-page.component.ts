import { Component, NgZone,OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { DatePipe } from '@angular/common';
import { DataService } from '../service.service';
import { MatDialogRef } from '@angular/material/dialog';
import { FuseConfirmationService } from '@fuse/services/confirmation';


@Component({
  selector: 'app-second-page',
  templateUrl: './second-page.component.html',
  styleUrls: ['./second-page.component.scss']
})
export class SecondPageComponent implements OnInit {

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
    private _fuseConfirmationService: FuseConfirmationService,private zone: NgZone) { }



  ngOnInit() {
    this.extractionForm = this.fb.group({
      plant: ['', Validators.required],
      startDate: [null, Validators.required],
      endDate: [null, Validators.required],
    });

    this.usertype = JSON.parse(localStorage.getItem("user")).Type
  }

  formatDate(date: Date): string {
    const datePipe = new DatePipe('en-US');
    return datePipe.transform(date, 'yyyy-MM-dd') || '';
  }
  





 

  onSubmit() {
    if (this.extractionForm.valid) {
      this.loadingData = true; // Start the loading spinner
      this.msg = "Extracting Data. Please Wait..."
      this.dataService.Extract(
        this.extractionForm.get("plant").value,
        this.formatDate(this.extractionForm.get("startDate").value),
        this.formatDate(this.extractionForm.get("endDate").value)
      ).subscribe(data => {
        this.zone.run(() => {
          if (data.progress !== undefined) {
            this.progress = data.progress;
          }
        });
        if (data.code == 200) {
          this.loadingData = false;
          this.success(data.msg);
          this._fuseConfirmationService.open(this.configForm.value);
        } else {
          this.loadingData = false;
          this.error(data.msg);
          
          this._fuseConfirmationService.open(this.configForm.value);
        }
      });
    } else {
      // Display more specific error messages for invalid form fields
      const invalidControls = this.getInvalidControls(this.extractionForm);
      const errorMessage = `Please fill the following fields: ${invalidControls.join(", ")}`;
      this.error(errorMessage);
      this._fuseConfirmationService.open(this.configForm.value);
    }
  }

  // Helper function to get the names of invalid controls
getInvalidControls(form: FormGroup): string[] {
  const invalidControls: string[] = [];
  Object.keys(form.controls).forEach(key => {
    if (form.controls[key].invalid) {
      invalidControls.push(key);
    }
  });
  return invalidControls;
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
