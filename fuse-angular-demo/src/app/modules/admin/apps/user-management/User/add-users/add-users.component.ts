import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { DataService } from '../../../../../../service.service';
import { FuseConfirmationService } from '@fuse/services/confirmation';

@Component({
  selector: 'app-add-users',
  templateUrl: './add-users.component.html',
  styleUrls: ['./add-users.component.scss']
})
export class AddUsersComponent implements OnInit {
  onAccessLevelChange(arg0: any) {
    this.level = arg0
  }

  projects: any[];
  level: any;
  allSelected: boolean = false;
  showAlertBoolean: boolean = false;
  Type:any;
  Title:any;
  Msg:any;
  composeForm: FormGroup;

  u: any;
  u2: any;
  configForm!: FormGroup;

  regions: any[];

  localAreas: any[];

  constructor(private dataService: DataService,
    public matDialogRef: MatDialogRef<AddUsersComponent>,
    private _formBuilder: FormBuilder,
    private _fuseConfirmationService: FuseConfirmationService
  ) { }

  ngOnInit(): void {
    this.loadProjects()
    // Create the form

    this.composeForm = this._formBuilder.group({
      ID_User_Login: ['', [Validators.required]],
      Password: ['', [Validators.required]],
      Position: [''],
      Type: [''],
      projects: [[]],
      Level_: [''],
      plant: [[]]
    });

    this.dataService.getregion().subscribe((data: any[]) => {
      this.regions = data;
    });

    // Fetch local areas
    this.dataService.getPlants().subscribe((data: any[]) => {
      this.localAreas = data;
    });
  }


  //new table project by plant 
  name = 'Angular ';
  dynamicArray = [];
  newDynamic;
  addRow() {
    this.dynamicArray.push({ firstName: '', lastName: '', emailAddress: '' });
    console.log('New row added successfully', 'New Row');
  }
  deleteRow(index) {
    this.dynamicArray.splice(index, 1);
  }
  getValues() {
    console.log(this.dynamicArray);
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

  loadProjects() {
    this.dataService.getProjects().subscribe(
      data => {
        this.projects = data;

      }
    );
  }
  /**
   * Send the message
   */
  message:any
  send(): void {
    if (!this.composeForm.valid) {
      this.message = "Please Provide Information of the user";
      this.showInfo(this.message, false);
      return;
    }
  
    // Prepare user data
    this.u = {
      "ID_User_Login": this.composeForm.get('ID_User_Login').value,
      "Password": this.composeForm.get('Password').value,
      "Position": this.composeForm.get('Position').value,
      "Type": this.composeForm.get('Type').value,
      "Level_": this.composeForm.get('Level_').value
    };
  
    // Add user
    this.dataService.addUser(this.u).subscribe(
      (data) => {
        if (data.code !== 200) {
          this.message = data.msg;
          this.showInfo(this.message, false);
        } else {
          this.addUserPlant().then(() => {
            this.message = "User and access have been added successfully!";
            this.showInfo(this.message, true);
          }).catch((errorMsg) => {
            this.message = errorMsg;
            this.showInfo(this.message, false);
          });
        }
      },
      (error) => {
        this.message = "Failed to add user.";
        this.showAlert('error', this.message, "Error");
      }
    );
  }
  
  async addUserPlant(): Promise<void> {
    const level = this.composeForm.get('Level_').value;
    const userId = this.composeForm.get('ID_User_Login').value;
    const projects = this.composeForm.get('projects').value;
    const plants = this.composeForm.get('plant').value;
  
    // Corporate Level Access
    if (level === "Corporate") {
      return new Promise<void>((resolve, reject) => {
        this.dataService.getPlants().subscribe(
          (data) => {
             data.forEach((d) => {
              projects.forEach((p) => {
                const u2 = this.createUserAccess(userId, d.plant_Description, p.Description);
                this.addUserAccess(u2).catch(reject);
              });
            });
            resolve(); 
          },
          () => reject("Failed to fetch corporate plants.")
        );
      });
    }
  
    // Regional Level Access
    if (level === "Regional") {
      return new Promise<void>((resolve, reject) => {
        this.dataService.getPlantFromRegion(plants).subscribe(
          (data) => {
            data.forEach((d) => {
              projects.forEach((p) => {
                const u2 = this.createUserAccess(userId, d.Plant, p.Description);
                this.addUserAccess(u2).catch(reject);
              });
            });
            resolve();
          },
          () => reject("Failed to fetch regional plants.")
        );
      });
    }
  
    // Other Level Access
    return new Promise<void>((resolve, reject) => {
      plants.forEach((plant) => {
        projects.forEach((p) => {
          const u2 = this.createUserAccess(userId, plant, p.Description);
          this.addUserAccess(u2).catch(reject);
        });
      });
      resolve();
    });
  }
  
  createUserAccess(user: string, plant: string, project: string) {
    return {
      "user": user,
      "plant": plant,
      "project": project,
      "expiration_date": "2070-10-10"
    };
  }
  
  addUserAccess(u2: any): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      this.dataService.addUserAccess(u2).subscribe(
        (data) => {
          if (data.code === 200) {
            resolve();
          } else {
            reject(data.msg);
          }
        },
        () => reject("Failed to add user access.")
      );
    });
  }
  
  showInfo(msg: string, success: boolean) {
    this.configForm = this._formBuilder.group({
      title: success ? 'Success!' : 'Error!',
      message: msg,
      icon: this._formBuilder.group({
        show: true,
        name: success ? 'heroicons_outline:check' : 'heroicons_outline:x',
        color: success ? 'info' : 'warn' // Green for success, Red for error
      }),
      actions: this._formBuilder.group({
        confirm: this._formBuilder.group({
          show: false,
          label: 'Remove',
          color: 'warn'
        }),
        cancel: this._formBuilder.group({
          show: true,
          label: 'Close',
          color: 'primary'
        })
      }),
      dismissible: true
    });
  
    this._fuseConfirmationService.open(this.configForm.value);
    this.matDialogRef.close();
  }
  




  toggleAllSelection() {
    if (this.allSelected) {
      this.composeForm.controls.projects.setValue([]);
    } else {
      this.composeForm.controls.projects.setValue([...this.projects]);
    }
    this.allSelected = !this.allSelected;
    
  }

  toggleSelection(project: string) {
    const projects = this.composeForm.controls.projects.value as string[];
    const index = projects.indexOf(project);
    if (index === -1) {
      projects.push(project);
    } else {
      projects.splice(index, 1);
    }
    this.composeForm.controls.projects.setValue(projects);
    this.allSelected = projects.length === this.projects.length;
  }

  isSelected(project: string): boolean {
    return this.composeForm.controls.projects.value.includes(project);
    
  }

  showAlert(type,msg,title){
    this.Msg = msg;
    this.Title = title;
    this.Type = type;
    this.showAlertBoolean = true;
    setTimeout(() => {
      this.showAlertBoolean = false;
    }, 5000); // 3 seconds
  }

}
