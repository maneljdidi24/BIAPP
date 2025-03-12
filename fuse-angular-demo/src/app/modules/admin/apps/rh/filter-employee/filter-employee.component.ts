import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';
import { AddEmployeeComponent } from '../add-employee/add-employee.component';
import { DataService } from 'app/service.service';


@Component({
  selector: 'app-filter-employee',
  templateUrl: './filter-employee.component.html',
  styleUrls: ['./filter-employee.component.scss']
})
export class FilterEmployeeComponent implements OnInit {

    regions:any[]
    plants:any[]
    departments:any[]
    jobs:any[]
    costcenters:any[]
    
  composeForm: FormGroup;
  reportForm: FormGroup;


  checkboxItems = [
    { label: 'Company News', checked: true },
    { label: 'Featured Products', checked: false },
    { label: 'Messages', checked: true },
    { label: 'Updates', checked: false },
    { label: 'Promotions', checked: false },
    { label: 'Announcements', checked: true },
    { label: 'Events', checked: false },
    { label: 'Surveys', checked: false },
    { label: 'Promotions2', checked: false },
    { label: 'Announcements2', checked: true },
    { label: 'Events2', checked: false },
    { label: 'Surveys2', checked: false },
  ];
  
    /**
     * Constructor
     */
    constructor(
        private service: DataService,
        public matDialogRef: MatDialogRef<AddEmployeeComponent>,
        private _formBuilder: FormBuilder
    )
    {
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Lifecycle hooks
    // -----------------------------------------------------------------------------------------------------

    /**
     * On init
     */
    ngOnInit(): void
    {
      this.loadregion();
      this.loadplants();
        this.reportForm = this._formBuilder.group({
            Plant: [[], Validators.required],
            Gender: [''],
            Scope:[''],
            HC_Type:[''],
            ID_Department:[''],
            Cost_Center:['']
          });

    }


    // -----------------------------------------------------------------------------------------------------
    // @ Public methods
    // -----------------------------------------------------------------------------------------------------

 

    /**
     * Save and close
     */
    saveAndClose(): void
    {
        // Save the message as a draft
        this.saveAsDraft();

        // Close the dialog
        this.matDialogRef.close();
    }

    /**
     * Discard the message
     */
    discard(): void
    {

    }

    /**
     * Save the message as a draft
     */
    saveAsDraft(): void
    {

    }

    /**
     * Send the message
     */
    send(): void
    {

    }


    /**
     * LoadRegion
     */
    loadregion(){
        this.service.GetRegionforuser().subscribe(
          (data) => {
            this.regions = data;
            if (this.regions.length === 1) {
              const selectedRegion = this.regions[0];
              this.reportForm.get('region').setValue(selectedRegion);
            }
          },
          (error) => {
            console.error('Error fetching plants:', error);
          }
        );
      }

      loadplants(){
        this.service.GetPlantsforuser().subscribe(
          (data) => {
            console.log(data)
            this.plants = data;
          },
          (error) => {
            console.error('Error fetching plants:', error);
          }
        );
      }  
      getDepartments() {
        this.service.getDepartments().subscribe(data => {
          this.departments = data.sort((a: any, b: any) => a.ID - b.ID);
        });
      }
      
      getJobs() {
        this.service.getJobs().subscribe(data => {
          this.jobs = data.sort((a: any, b: any) => a.ID - b.ID); // Assuming job ID is 'ID'
        });
      }
      
      getCostCenters() {
        this.service.getCostCenter().subscribe(data => {
          this.costcenters = data.sort((a: any, b: any) => a.idcc - b.idcc); // Assuming cost center ID is 'idcc'
        });
      }


      /* {
        "plants": [
          "COF MA","COF TN"
        ],
        "start_date": "10/10/2024",
        "end_date": "12/12/2024"
      } */
}
