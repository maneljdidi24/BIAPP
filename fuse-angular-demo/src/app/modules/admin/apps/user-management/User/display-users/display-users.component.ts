import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { DataService } from '../../../../../../service.service';
import { FormBuilder, FormGroup } from '@angular/forms';
import { FuseConfirmationService } from '@fuse/services/confirmation';
import { AddUsersComponent } from '../add-users/add-users.component';
import { EditUsersComponent } from '../edit-users/edit-users.component';

@Component({
  selector: 'app-display-users',
  templateUrl: './display-users.component.html',
  styleUrls: ['./display-users.component.scss']
})
export class DisplayUsersComponent implements OnInit {
  users:any[] = [];
  roles:any[];
  showAlertBoolean: boolean = false;
  Type:any;
  Title:any;
  Msg:any;
  
  configForm!: FormGroup;
  constructor(private _matDialog: MatDialog,private dataService: DataService,
    private _formBuilder: FormBuilder, private _fuseConfirmationService: FuseConfirmationService) { }

  ngOnInit(): void {
    this.loadData() 
      //this.projects.forEach(e=>console.log(e))
      this.configForm = this._formBuilder.group({
        title      : 'Remove contact',
        message    : 'Are you sure you want to change this contact permanently? <span class="font-medium">This action cannot be undone!</span>',
        icon       : this._formBuilder.group({
            show : true,
            name : 'heroicons_outline:exclamation',
            color: 'warn'
        }),
        actions    : this._formBuilder.group({
            confirm: this._formBuilder.group({
                show : true,
                label: 'Remove',
                color: 'warn'
            }),
            cancel : this._formBuilder.group({
                show : true,
                label: 'Cancel'
            })
        }),
        dismissible: true
    });
    // Assuming you have a roles array in your component
    this.roles = [
  { value: 'Corporate', label: 'Corporate', description: 'Has access to all data across COFICAB.' },
  { value: 'Local', label: 'Local', description: 'Has access only to local data within their specific location.' },
  { value: 'Regional', label: 'Regional', description: 'Has access only to data within their specified region.' },
];



  }

  loadData() {
    this.dataService.getUsers().subscribe(
      data => {
        //data.forEach(e=>console.log(e))
      //  console.log(data); // Log the response to the console for debugging
        this.users = data;
      },
      error => {
        console.error(error); // Log any errors
      }
    );
  }
      /**
     * Open compose dialog
     */
      openComposeDialog(): void
      {
           // Open the dialog
          const dialogRef = this._matDialog.open(AddUsersComponent);
  
          dialogRef.afterClosed()
                   .subscribe((result) => {
                       console.log('Compose dialog was closed!');
                       this.loadData()
                   }); 
      }

      onRoleChange(event: any,user:any): void {
        const newRole = event.value;
      //  alert(`Role changed to ${newRole} for user: ${JSON.stringify(user)}`);
        this.change(user,event.value)
        const dialogRef = this._fuseConfirmationService.open(this.configForm.value);
       // Subscribe to afterClosed from the dialog reference
        dialogRef.afterClosed().subscribe((result) => {
          if(result=="confirmed") {
            user.Level_=newRole;
            this.dataService.editUser(user.ID_User_Login, user).subscribe(
              data => {
                if (data.code==200){
                  this.showAlert('success', data.msg, "Success")
                  this._fuseConfirmationService.open(this.configForm.value);
                  this.loadData()
                }
                else{
                  this.showAlert("error",data.msg,"Error")
                  this._fuseConfirmationService.open(this.configForm.value);
                }
              },
              error => {
                console.error(error); // Log any errors
              }
            );
          }
        }); 
        
      }
    
      onDeleteButtonClick(id:any): void {
              // Open the dialog and save the reference of it
              this.Delete()
              const dialogRef = this._fuseConfirmationService.open(this.configForm.value);
              // Subscribe to afterClosed from the dialog reference
               dialogRef.afterClosed().subscribe((result) => {
                 if(result=="confirmed") {
                     this.dataService.deleteUserAccess(id).subscribe((data) => {
                       if (data.code==200){
                         this.showAlert('success', data.msg, "Success")
                         this.loadData()
                       }
                       else{
                        this.showAlert("error",data.msg,"Error")
                       }
                   });  
                 }
               }); 
      }



      change(user, old) {
        this.configForm = this._formBuilder.group({
          title: 'Confirm Edit Level user',
          message: `Are you sure you want to change the level of the '${user.ID_User_Login}' to '${old} '<span class="font-medium"></span>`,
          icon: this._formBuilder.group({
            show: true,
            name: 'heroicons_outline:exclamation',
            color: 'primary'
          }),
          actions: this._formBuilder.group({
            confirm: this._formBuilder.group({
              show: true,
              label: 'Edit',
              color: 'primary'
            }),
            cancel: this._formBuilder.group({
              show: true,
              label: 'Cancel',
              color: 'primary'
            })
          }),
          dismissible: true
        });
      }
      
      Delete() {
        this.configForm = this._formBuilder.group({
          title      : 'Remove User',
          message    : 'Are you sure you want to remove this user permanently? <span class="font-medium">This action cannot be undone!</span>',
          icon       : this._formBuilder.group({
              show : true,
              name : 'heroicons_outline:exclamation',
              color: 'warn'
          }),
          actions    : this._formBuilder.group({
              confirm: this._formBuilder.group({
                  show : true,
                  label: 'Remove',
                  color: 'warn'
              }),
              cancel : this._formBuilder.group({
                  show : true,
                  label: 'Cancel'
              })
          }),
          dismissible: true
        });
      }


      onEditButtonClick(id) {
        // Open the dialog and pass the id as data
        const dialogRef = this._matDialog.open(EditUsersComponent, {
            data: { userId: id }
        });
    
        dialogRef.afterClosed().subscribe((result) => {
            console.log('Edit dialog was closed!');
            this.loadData();
        });
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


