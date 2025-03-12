import { Component, OnInit ,Inject} from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { DataService } from 'app/service.service';
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';
import { of } from 'rxjs';
import { FuseConfirmationService } from '@fuse/services/confirmation';

@Component({
  selector: 'app-edit-users',
  templateUrl: './edit-users.component.html',
  styleUrls: ['./edit-users.component.scss']
})
export class EditUsersComponent implements OnInit {

userId: any;
showPasswordInput: boolean = false;  // Flag to control visibility
projects: any[];
level: any;
allSelected: boolean = false;

togglePasswordInput(): void {
  this.showPasswordInput = !this.showPasswordInput;  // Toggle the flag
}
user : any
signInForm: FormGroup;

  constructor(@Inject(MAT_DIALOG_DATA) public data: any ,private dataService: DataService,  public matDialogRef: MatDialogRef<EditUsersComponent>,
  private _fuseConfirmationService: FuseConfirmationService,
  private _formBuilder: FormBuilder,) {
    this.userId = data.userId;
  }

  ngOnInit(): void {
    this.signInForm = this._formBuilder.group({
      Password: ['', [Validators.required]],
      Position: [''],
      Type: [''],
      projects: [[]],
      Level_: [''],
      plant: [[]]
  });
  this.load()
  this.loaddataofuser()
  }



  toggleAllSelection() {
    if (this.allSelected) {
      this.signInForm.controls.projects.setValue([]);
    } else {
      this.signInForm.controls.projects.setValue([...this.projects]);
    }
    this.allSelected = !this.allSelected;
  }


toggleUserProject(project) {
  if (this.allSelected) {
    this.signInForm.controls.projects.setValue([]);
  } else {
    this.signInForm.controls.projects.setValue([...project]);
  }
  this.allSelected = !this.allSelected;
}


  loaddataofuser(){
    this.dataService.getUserById(this.userId).subscribe(data=>{
      
      this.user = data
      this.level=this.user['Level_']
     this.signInForm = this._formBuilder.group({
      Password: [''],
      Position: [this.user['Position']],
      Type: [this.user['Type']],
      projects: [[]],
      Level_: [this.user['Level_']],
      plant: [[]]
      
  });

  const filteredProjects = this.projects.filter((project: any) =>
    this.user['Projects'].some((p: any) => 
      project.Description.includes(p.Description)
    )
  );

  this.signInForm.controls.projects.setValue([...filteredProjects]);

    const filteredPlants = this.localAreas.filter((l: any) =>
      this.user['Plants'].some((p: any) => 
        l.plant.includes(p)
      )
    );
  
    this.signInForm.controls.plant.setValue([...filteredPlants]); 
  



  this.onAccessLevelChange(this.user['Level_'])

    } 
   
  )

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



  onAccessLevelChange(arg0: any) {
    this.level = arg0
  }


  Title: any;
  u: any;
  u2: any;
  configForm!: FormGroup;

  regions: any[];

  localAreas: any[];




  load(){
    this.dataService.GetPlantsforuser().subscribe((data: any[]) => {
      this.localAreas = data
    })
      this.dataService.getregion().subscribe((data) => {
        this.regions = data;
      });
      this.dataService.getProjects().subscribe(
        data => {
          this.projects = data;
        }
      );
  }


  send() {
    const userDetails = {
      "Password": this.signInForm.get('Password').value || this.user['Password'],
      "Position": this.signInForm.get('Position').value,
      "Type": this.signInForm.get('Type').value,
      "Level_": this.level
    };
    
    // Close the dialog
    this.matDialogRef.close();
    
    // Reset error/success messages
    let errors = [];
    let successMessage = null;
  
    // Call editUser API
    this.dataService.editUser(this.user['ID_User_Login'], userDetails).subscribe(
      data => {
        if (data.code === 200) {
          // Proceed to editUserAccess if editUser is successful
          const accessDetails = {
            "project": this.signInForm.get('projects').value,
            "plant": this.signInForm.get('plant').value,
            "expiration_date": "2070-10-10"
          };
  
          this.dataService.editUserAccess(this.user['ID_User_Login'], accessDetails).subscribe(
            accessData => {
              if (accessData.code === 200) {
                successMessage = accessData.msg;
              } else {
                errors.push(accessData.msg);
              }
  
              // Show final status after both operations
              this.showFinalStatus(successMessage, errors);
            },
            error => {
              errors.push('Failed to update user access. Please try again.');
              this.showFinalStatus(null, errors);
            }
          );
        } else {
          errors.push(data.msg);
          this.showFinalStatus(null, errors);
        }
      },
      error => {
        errors.push('Failed to update user details. Please try again.');
        this.showFinalStatus(null, errors);
      }
    );
  }
  
  // Function to display success or error messages and open the confirmation form
  showFinalStatus(successMessage: string | null, errors: string[]) {
    if (successMessage) {
      this.success(successMessage);
    }
  
    if (errors.length > 0) {
      this.error(errors.join('\n'));
    }
  
    // Open the confirmation form regardless of success or errors
    this._fuseConfirmationService.open(this.configForm.value);
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
  adduserPlant() {

  }

  adduserAcc() {

  }









}
