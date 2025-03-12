import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { DataService } from '../../../../../../service.service';
import { FormBuilder, FormGroup } from '@angular/forms';
import { FuseConfirmationService } from '@fuse/services/confirmation';
import { AddPlantsComponent } from '../add-plants/add-plants.component';


@Component({
  selector: 'app-display-plants',
  templateUrl: './display-plants.component.html',
  styleUrls: ['./display-plants.component.scss']
})
export class DisplayPlantsComponent implements OnInit {

  plants:any[] = [];
  roles:any[];
  
  configForm!: FormGroup;
  constructor(private _matDialog: MatDialog,private dataService: DataService,
    private _formBuilder: FormBuilder, private _fuseConfirmationService: FuseConfirmationService) { }

  ngOnInit(): void {
    this.loadData() 
  }

  loadData() {
    this.dataService.getPlants().subscribe(
      data => {
        //data.forEach(e=>console.log(e))
      //  console.log(data); // Log the response to the console for debugging
        this.plants = data;
        console.log(this.plants); // Log the projects after assignment
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
          const dialogRef = this._matDialog.open(AddPlantsComponent);
  
          dialogRef.afterClosed()
                   .subscribe((result) => {
                       console.log('Compose dialog was closed!');
                       this.loadData()
                   }); 
      }

      onRoleChange(event: any,plant:any): void {
        const newRole = event.value;
      //  alert(`Role changed to ${newRole} for plant: ${JSON.stringify(plant)}`);
        this.change(plant,event.value)
        const dialogRef = this._fuseConfirmationService.open(this.configForm.value);
       // Subscribe to afterClosed from the dialog reference
        dialogRef.afterClosed().subscribe((result) => {
          if(result=="confirmed") {
            plant.Level_=newRole;
            this.dataService.editPlant(plant.ID_plant_Login, plant).subscribe(
              data => {
                if (data.code==200){
                  this.success(data.msg)
                  this._fuseConfirmationService.open(this.configForm.value);
                  this.loadData()
                }
                else{
                  this.error(data.msg)
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
                     this.dataService.deletePlant(id).subscribe((data) => {
                       if (data.code==200){
                         this.success(data.msg)
                         this.loadData()
                       }
                       else{
                         this.error(data.msg)
                       }
                       this._fuseConfirmationService.open(this.configForm.value);
                   });  
                 }
               }); 
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

      change(plant, old) {
        this.configForm = this._formBuilder.group({
          title: 'Confirm Edit Level plant',
          message: `Are you sure you want to change the level of the '${plant.ID_plant_Login}' to '${old} '<span class="font-medium"></span>`,
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
          title      : 'Remove plant',
          message    : 'Are you sure you want to remove this plant permanently? <span class="font-medium">This action cannot be undone!</span>',
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
    
      }

