
import { Component, AfterViewInit, ViewChild, OnInit, Inject, ChangeDetectorRef, ViewChildren, QueryList, ElementRef } from '@angular/core';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';
import { ActivatedRoute, Router } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { CsvDownloadService } from './../../../../../services/csv-download.service';
import { DataService } from 'app/service.service';

@Component({
  selector: 'app-salesreport',
  templateUrl: './salesreport.component.html',
  styleUrls: ['./salesreport.component.scss']
})
export class SalesreportComponent implements OnInit, AfterViewInit {


  showAlertBoolean: boolean = false;
  Type:any;
  Title:any;
  Msg:any;
  dataloaded!: any[];
  dataloadedAll!: any[];
  region:any[];
  configForm!: FormGroup;
  reportForm: FormGroup;
  project: any;
  contract: any;

  alldata!: any[];
  dataCount: any;
  totalPages: any[] = []; // Initialize totalPages
  loadingData: boolean = false;
  loadingData2: boolean = false;
  plant: any ;
  startDate: any = '2023-01-05';
  endDate: any;
  plantsObject = {
    "plants": []
  }; 

  @ViewChild(MatPaginator) paginator: MatPaginator;
  length: any;
  pageSize: any = 500;
  pageSizeOptions: number[] = [500];
  columns = [
    "Trans Type", "N° Invoice ", "Currency", "Sold To BP","Sold to",  "Item",  "Converted Quantity(KM)", "Converted Quantity unit", "Converted Price(KM)", 
    "Converted Price unit",
     "WIRE" ,"Material Exchange", 
    "Metal weight sales", "Added value", "Converted Added value" ,"Metal Rate", "N° Contract", "Shipment", 
    "Plant", 
    "Reporting Amount (Euro)",  "Reporting Amount (USD)", 

     "Invoice Date", "Client", "Client group", "Client subgroup"

]



  dropdownVisible = false;

  msg: any;
  //172.22.90.6
  checkboxes: any[] = [];

  constructor( private dataservice: DataService,
   private _formBuilder: FormBuilder,
    private fb: FormBuilder, private cdr: ChangeDetectorRef) { 
    }

    
  sortColumn: string | null = null;
  sortDirection: 'asc' | 'desc' = 'asc';

  ngOnInit(): void {
    this.reportForm = this._formBuilder.group({
      plant: ['', Validators.required],
      startDate: ['', Validators.required],
      endDate: ['', Validators.required]
    });
    this.dataservice.GetRegionforuser().subscribe(
      (data) => {
        this.region = data;
        console.log(data)
        if (this.region.length === 1) {
          const selectedRegion = this.region[0];
          this.reportForm.get('plant').setValue(selectedRegion);
          // Trigger the selection change programmatically
          this.onSelect({ value: selectedRegion });
        }
      },
      (error) => {
        console.error('Error fetching plants:', error);
      }
    );
/*     this.reportForm.valueChanges.subscribe((values) => {
      this.onSubmit();
    }); */
  }

  picker:any;

  showAlert(type,msg,title){
    this.Msg = msg;
    this.Title = title;
    this.Type = type;
    this.showAlertBoolean = true;
    setTimeout(() => {
      this.showAlertBoolean = false;
    }, 5000); // 3 seconds
  }

  sort(column: string): void {
    if (this.sortColumn === column) {
      // Toggle sort direction
      this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      // Set new column and default to ascending
      this.sortColumn = column;
      this.sortDirection = 'asc';
    }

    this.dataloaded.sort((a, b) => {
      if (a[column] < b[column]) return this.sortDirection === 'asc' ? -1 : 1;
      if (a[column] > b[column]) return this.sortDirection === 'asc' ? 1 : -1;
      return 0;
    });
  }


  ngAfterViewInit() {
    this.paginator.page.subscribe(
      (event) => console.log(event)
    );
  }





  checkboxChecked(checkboxes: any): any {
  this.checkboxes.forEach(c => { 
    if (c.plant_Description===checkboxes) {c.checked = !c.checked}});
  }


  toggleDropdown() {
    this.dropdownVisible = !this.dropdownVisible;
    this.loaddataAll(this.plant, this.startDate, this.endDate);

  }

  formatDate(date: Date): string {
    const datePipe = new DatePipe('en-US');
    return datePipe.transform(date, 'yyyy-MM-dd') || '';
  }
  onSubmit(): void {
    if (this.reportForm.valid) {
      this.startDate = this.formatDate(this.reportForm.get('startDate').value);
      this.endDate = this.formatDate(this.reportForm.get('endDate').value);
      this.plant = this.reportForm.get('plant').value;
  
      // Check if the date range is within 2 months
      const start = new Date(this.startDate);
      const end = new Date(this.endDate);
      const maxRange = 3 * 30 * 24 * 60 * 60 * 1000; // Approx 2 months in milliseconds
  
      if (end.getTime() - start.getTime() > maxRange) {
        this.showAlert(
          'error',
          "The date range should not exceed 3 months.",
          "Invalid Date Range"
        );
        return;
      }
  
      this.loadingData = true;
      this.loadcheckedplants();
      this.getcount(this.plant, this.startDate, this.endDate);
      this.loaddata(this.plant, this.startDate, this.endDate, 0);
    } else {
      this.showAlert('error', "Make sure you add all filters", "Error");
    }
  }
  



  onSelect(event: any) {

    this.loadingData = true; // Start the loading spinner
    this.msg = "Getting plants list...";
  
    // Retrieve the user's plants from localStorage (assuming it's stored as a stringified array)
    const userPlants = JSON.parse(localStorage.getItem('user') || '{}').Plant || [];

    
  
    // Fetch the distinct plants from the service
    this.dataservice.getPlantFromRegion(event.value).subscribe(data => {
       this.loadingData = false;
      
      // Filter the data to only include plants that are in the user's plant list
      const filteredPlants = data.filter((plant: any) => userPlants.includes(plant.plant_Description));
      

      // Add 'checked' property to each object and set it to false
      this.checkboxes = filteredPlants.map((c: any) => ({
        ...c,
        checked: false // default is false
      }));
  
      if (filteredPlants.length === 0) {
        this.msg = "No plants available for your selection.";
      } 
    }); 
  }
  
  

  pageChanged(event: any) {
    const pageNumber = event.pageIndex + 1; // Adding 1 to get the current page number
    this.loaddata(this.plant, this.startDate, this.endDate, pageNumber)

  }



  getcount(plant: any, start: any, end: any): void {
    this.dataservice.getcountsalesdata(plant, start, end, this.plantsObject).subscribe(data => {
      this.dataCount = data;
      const totalPages = Math.ceil(this.dataCount / 500); // Calculate total pages
      this.length = this.dataCount
      //this.updateLength(totalPages);
    });
  }

  loaddata(plant: any, start: any, end: any, offset: any): void {
     this.msg = "Loading..."
    this.loadingData = true; // Start the loading spinner
    //this.loadcheckedplants()

  this.dataservice.SelectSalesDisplay500(plant, start, end, offset, this.plantsObject).subscribe(data => {
    if (data.msg) {
      this.dataloaded = []
      this.loadingData = false;
      if (data.code==404){
        this.showAlert('info', data.msg, "Alert")
      }
      else {
        this.showAlert('error', data.msg, "Error")
      }
    } else {
      this.dataloaded = data;
      this.loadingData = false; // Stop the loading spinner
    }
  }); 
     
  }

loaddataAll(plant: any, start: any, end: any): void {
    this.msg = "Creating file...";
    this.loadingData = true; // Start the loading spinner
    this.loadcheckedplants(); // Load selected plants

/*     this.dataservice.getSalesAll(this.plant, this.startDate, this.endDate, this.plantsObject)
        .subscribe({
            next: (data) => {
                //console.log('Full Response:', data);
                console.log('Response Code:', data.code);
                //console.log('Message Length:', data.msg?.length);

                if (data.code ==200){
                    this.dataloadedAll = data.msg;
                    //console.log('Data Loaded:', this.dataloadedAll);
                    this.loadingData = false; // Stop the loading spinner

                    // Successful download
                    //console.log(`Data for ${plant} region from ${start} to ${end} successfully downloaded as a CSV file.`);
                    this.csvDownloadService.downloadCsv(this.dataloadedAll, `${plant}_${start}_${end}`);
                    //alert(`Your data for ${plant} region from ${start} to ${end} has been successfully downloaded as a CSV file.`);
                }
                else {
                  console.error('Error with Code:', data.code);
                  console.error('Error occurred while fetching data:', data.error);
                  this.loadingData = false;
              }  
            },
            error: (error) => {
                // Log any error that occurs during the API call
                console.error('Error occurred while fetching data:', error);
                this.loadingData = false; // Stop the loading spinner in case of error
                //alert(`Failed to load data: ${error.message}`);
            },
            complete: () => {
                // Log when the request is complete
                console.log('Request completed.');
            }
        }); */
    this.dataservice.SelectAllSalesForCSV(this.plant, this.startDate, this.endDate, this.plantsObject).subscribe(blob => {
      this.loadingData = false; // Stop the loading spinner
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${this.plant}_data_${this.startDate}_to_${this.endDate}.csv`; // Adjust the filename as needed
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url); 
      
      this.showAlert('success', 'File downloaded successfully!.', "Success")

    }, error => {
      this.showAlert('error', 'Error downloading the file', "Error")
    }); 
}




  loadcheckedplants(){
    const checkedBoxes = this.checkboxes
    .filter(c => c.checked)
    .map(c => c.Plant);
    
  // Alert the checked boxes
  if (checkedBoxes.length > 0) {
    this.plantsObject.plants = []
    checkedBoxes.forEach(c=> this.plantsObject.plants.push(c))
  } else {  
      this.plantsObject.plants = []
    // If no checkboxes are checked, gather the unchecked checkboxes
    const uncheckedBoxes = this.checkboxes
      .filter(c => !c.checked)
      .map(c => c.Plant);
      uncheckedBoxes.forEach(c=> this.plantsObject.plants.push(c))
  }

  }




}

