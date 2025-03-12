import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { DataService } from '../../../../../../service.service';
import { FuseConfirmationService } from '@fuse/services/confirmation';

@Component({
  selector: 'app-add-projects',
  templateUrl: './add-projects.component.html',
  styleUrls: ['./add-projects.component.scss']
})
export class AddProjectsComponent implements OnInit {

  composeForm: FormGroup;
  Title: any;
  p: any;
  configForm!: FormGroup;



  constructor(private dataService: DataService,
    public matDialogRef: MatDialogRef<AddProjectsComponent>,
    private _formBuilder: FormBuilder,
    private _fuseConfirmationService: FuseConfirmationService
  ) { }

  ngOnInit(): void {
    // Create the form
    this.composeForm = this._formBuilder.group({
      Code_Project: ['', [Validators.required]],
      Description: ['']
    });
  }



  /**
   * Save and close
   */
  saveAndClose(): void {
    // Close the dialog
    this.matDialogRef.close();
  }

  /**
 * Discard the message
 */
  discard(): void {
    // Close the dialog
    this.matDialogRef.close();
  }


  /**
   * Send the message
   */
  send(): void {
    if (this.composeForm.valid) {
      this.p = {
        "Code_Project": this.composeForm.get('Code_Project').value,
        "Description": this.composeForm.get('Description').value
      }
      this.dataService.addProject(this.p).subscribe((data) => {
        if (data.code == 200) {
          this.success(data.msg)
          this._fuseConfirmationService.open(this.configForm.value);

          this.matDialogRef.close();
        }
        else {
          this.error(data.msg)
          this._fuseConfirmationService.open(this.configForm.value);
        }


      });
    }
    else{
      this.error("Please Provide a unique Project code")
      this._fuseConfirmationService.open(this.configForm.value);
    }
  }

  error(msg) {
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

  success(msg) {
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
