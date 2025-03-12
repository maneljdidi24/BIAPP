import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSort } from '@angular/material/sort';
import { MatDialog } from '@angular/material/dialog';
import { MatTableDataSource } from '@angular/material/table';
import { DataService } from 'app/service.service';
import * as XLSX from 'xlsx';
import { FilterEmployeeComponent } from '../filter-employee/filter-employee.component';

/* import {
  IColumn,
  IItem
} from '@coreui/angular'; */
@Component({
  selector: 'app-display-employee',
  templateUrl: './display-employee.component.html',
  styleUrls: ['./display-employee.component.scss']
})
export class DisplayEmployeeComponent implements OnInit {
  willDownload = false;
  plants:any;
  displayedColumns: string[] = ['name_E', 'plant.Plant', 'Department.Nom_Department', 'Local_Position', 'HC_Type', 'Scope', 'Cost_Center', 'Hiring_Date', 'Termination_Date', 'Termination_Reason', 'Job.job_description'];
  columns = [
    
    { id: 'Id_Empl', header: 'Id Employee' },
    { id: 'name_E', header: 'Name' },
    { id: 'plant.Plant', header: 'Plant' },
    { id: 'Department.Nom_Department', header: 'Department'},
    { id: 'Local_Position', header: 'Local Position' },
    { id: 'HC_Type', header: 'HC Type' },
    { id: 'Scope', header: 'Scope' },
    { id: 'Cost_Center', header: 'Cost Center' },
    { id: 'Hiring_Date', header: 'Hiring Date' },
    { id: 'Termination_Date', header: 'Termination Date' },
    { id: 'Termination_Reason', header: 'Termination Reason' },
    { id: 'Job.job_description', header: 'Job' }
  ];
  dataSource = new MatTableDataSource<any>();
  loadingData: boolean = false;
  msg:any
  isList: number;
  isMenu: boolean = false;
  region:any;
  isSearch: boolean = false;
  @ViewChild(MatSort) sort: MatSort;
  searchTerm = {}; // To store search terms for each column
  reportForm: FormGroup;

  constructor(private service: DataService,private _matDialog: MatDialog,private _formBuilder: FormBuilder) {}

  ngOnInit(): void {
    this.loadEmployee();

  }

      /**
     * Open compose dialog
     */
      openComposeDialog(): void
      {
          // Open the dialog
          const dialogRef = this._matDialog.open(FilterEmployeeComponent);
  
          dialogRef.afterClosed()
                   .subscribe((result) => {
                       console.log('Compose dialog was closed!');
                   });
      }


  loadEmployee() {
    this.loadingData=true;
    this.msg="loading";
        this.service.getemployee().subscribe((data) => {
      this.dataSource.data = data;
      this.dataSource.sort = this.sort; // Set the sort after data is loaded
      this.loadingData=false;
    });
  }





    // Function to apply filtering for each column
    applyFilter(columnId: string): void {
      const filterValue = this.searchTerm[columnId]?.trim().toLowerCase() || '';
      
      this.dataSource.filterPredicate = (data, filter) => {
        const value = this.getNestedValue(data, columnId)?.toString().toLowerCase() || '';
        return value.includes(filter);
      };
  
      this.dataSource.filter = filterValue;
    }

  getNestedValue(element: any, property: string): any {
    const value = property.split('.').reduce((acc, key) => acc && acc[key], element);
  
    // Check if the value is a date and format it
    if (value && !isNaN(Date.parse(value))) {
      const date = new Date(value);
      return date.toISOString().split('T')[0]; // Formats as 'YYYY-MM-DD'
    }
  
    return value;
  }
  

  click(vari:any){
    alert(vari)
  }




  showAlertBoolean: boolean = false;
  Type:any;
  Title:any;
  Msg:any;
  
  showAlert(type,msg,title){
    this.Msg = msg;
    this.Title = title;
    this.Type = type;
    this.showAlertBoolean = true;
    setTimeout(() => {
      this.showAlertBoolean = false;
    }, 5000); // 3 seconds
  }
  
  onSubmit(){

  }
}

