import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { AddProjectsComponent } from '../add-projects/add-projects.component';
import { DataService } from '../../../../../../service.service';
import { FormBuilder, FormGroup } from '@angular/forms';
import { FuseConfirmationService } from '@fuse/services/confirmation';

@Component({
  selector: 'app-display-projects',
  templateUrl: './display-projects.component.html',
  styleUrls: ['./display-projects.component.scss'],
})
export class DisplayProjectsComponent implements OnInit {
  projects:any[] = [];
  
  configForm!: FormGroup;


  constructor(private _matDialog: MatDialog,private dataService: DataService,
    private _formBuilder: FormBuilder, private _fuseConfirmationService: FuseConfirmationService) { }

    ngOnInit(): void {

    this.loadData() 
      //this.projects.forEach(e=>console.log(e))
      this.configForm = this._formBuilder.group({
        title      : 'Remove Project',
        message    : 'Are you sure you want to remove this project permanently? <span class="font-medium">This action cannot be undone!</span>',
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
    
    loadData() {
      this.dataService.getProjects().subscribe(
        data => {
          //data.forEach(e=>console.log(e))
        //  console.log(data); // Log the response to the console for debugging
          this.projects = data;

          console.log(this.projects); // Log the projects after assignment
        },
        error => {
          console.error(error); // Log any errors
        }
      );
    }

    

/*   loadData() {
    this.dataService.getProjects().subscribe((data) => {
     //this.projects = data
     data.forEach(d => {
      alert(d.Code_Project)
      this.projects.push(d)
      this.projects.forEach(e=>alert(e))
     });
    });

  } */


  

  refrech() {
    this.dataService.getProjects().subscribe((data) => {
      this.projects = data;
      console.log(this.projects);
    });
  }

      /**
     * Open compose dialog
     */
      openComposeDialog(): void
      {
           // Open the dialog
          const dialogRef = this._matDialog.open(AddProjectsComponent);
  
          dialogRef.afterClosed()
                   .subscribe((result) => {
                       console.log('Compose dialog was closed!');
                       this.loadData()
                   }); 
      }

          /**
     * Open confirmation dialog
     */
    openConfirmationDialog(project:any): void
    {
        // Open the dialog and save the reference of it
      const dialogRef = this._fuseConfirmationService.open(this.configForm.value);
       // Subscribe to afterClosed from the dialog reference
        dialogRef.afterClosed().subscribe((result) => {
          if(result=="confirmed") {
              this.dataService.deleteProject(project).subscribe((data) => {
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
  
}
