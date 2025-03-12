import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { DataService } from '../../../../../../service.service';
import { FormBuilder, FormGroup } from '@angular/forms';
import { FuseConfirmationService } from '@fuse/services/confirmation';
import { AddUsersComponent } from '../add-users/add-users.component';

@Component({
  selector: 'app-manage-permissions',
  templateUrl: './manage-permissions.component.html',
  styleUrls: ['./manage-permissions.component.scss']
})
export class ManagePermissionsComponent implements OnInit {

  distinctUsers: string[] = [];
  projectsAndPlants: any[] = [];
  access:any[][] = [];
  constructor(private _matDialog: MatDialog,private dataService: DataService,
    private _formBuilder: FormBuilder, private _fuseConfirmationService: FuseConfirmationService) { }

  ngOnInit(): void {
    this.loadData()
    this.getDistinctUsers()

  }

  loadData() {
    this.dataService.getUserAccess().subscribe(
      data => {
        //data.forEach(e=>console.log(e))
         // Log the response to the console for debugging
        this.access = data;
      },
      error => {
        console.error(error); // Log any errors
      }
    );
    console.log(this.access);
  }

  getVisiblePlants(plants: string[]): string[] {
    return plants.slice(0, 3); // Show first 3 items
  }

  toggleShowMore(user: any): void {
    user.showMore = !user.showMore;
  }
  isContentEditable = false
  makeited(){
    this.isContentEditable = true
  }
 
  getDistinctUsers() {
    this.dataService.getDistinctUsers().subscribe(
      (data) => {
        this.distinctUsers = data;
      },
      (error) => {
        console.error('Error fetching distinct users', error);
      }
    );
  }


}
