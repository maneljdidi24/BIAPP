import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { DataService } from 'app/service.service';
import * as XLSX from 'xlsx';

@Component({
  selector: 'app-add-employee',
  templateUrl: './add-employee.component.html',
  styleUrls: ['./add-employee.component.scss']
})
export class AddEmployeeComponent implements OnInit {

  name = 'This is XLSX TO JSON CONVERTER';
  willDownload = false;
  msg:any
  employeeForm: FormGroup;
  loadingData: boolean = false;
  constructor(private service: DataService,private _formBuilder: FormBuilder) {}
  minDate: Date = new Date(1950, 0, 1); // January 1, 1950
  maxDate: Date = new Date(2024, 11, 31); // December 31, 2024

  ngOnInit(): void {
    this.employeeForm = this._formBuilder.group({
      Id_Empl: ['', Validators.required],
      name_E: ['', Validators.required],
      Gender: ['', Validators.required],
      Birth_Date: ['', Validators.required],
      ID_job: ['', Validators.required],
      HC_Type: ['', Validators.required],
      Local_Position: [''],
      Plant: ['', Validators.required],
      Scope: ['', Validators.required],
      ID_Department: ['', Validators.required],
      Cost_Center: ['', Validators.required],
      Hiring_Date: ['', Validators.required],
      Valuation_Level : [''],
      Termination_Date: [''],
      Termination_Reason: ['']
    });
    this.getDepartments()
    this.getJobs()
    this.GetPlantsforuser()
    this.getCostCenters()
  }

  // init all conbobox

  departments : any[]
  filteredJobs: any[] = [];
  jobs : any[]
  plants :any[]

  costcenters : any[]
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

    
  GetPlantsforuser() {
    this.service.GetPlantsforuser().subscribe(data => {
      this.plants = data.sort((a: any, b: any) => a.plant - b.plant); // Assuming cost center ID is 'idcc'
    });
  }
  
  



    //create code
  
    onFileChange(ev) {
      let workBook = null;
      let jsonData = null;
      const reader = new FileReader();
      const file = ev.target.files[0];
      reader.onload = (event) => {
        const data = reader.result;
        workBook = XLSX.read(data, { type: 'binary' });
        jsonData = workBook.SheetNames.reduce((initial, name) => {
          const sheet = workBook.Sheets[name];
    
          // Parse the sheet into JSON and convert dates
          initial[name] = XLSX.utils.sheet_to_json(sheet, {
            raw: false, // Enables parsing of dates into strings
          }).map(row => {
            // Transform each row to format dates as 'YYYY-MM-DD'
            Object.keys(row).forEach(key => {
              if (typeof row[key] === 'number' && row[key] > 59) {
                // Handle Excel serial numbers to convert to 'YYYY-MM-DD'
                const date = new Date((row[key] - 25569) * 86400 * 1000); // Convert Excel serial to JS Date
                row[key] = date.toISOString().split('T')[0]; // Format as 'YYYY-MM-DD'
              } else if (typeof row[key] === 'string' && /^\d{1,2}\/\d{1,2}\/\d{2,4}$/.test(row[key])) {
                // Convert string dates like '5/20/90' to 'YYYY-MM-DD'
                const [month, day, year] = row[key].split('/');
                const fullYear = year.length === 2 ? `19${year}` : year; // Add '19' prefix if year is 2 digits
                row[key] = `${fullYear.padStart(4, '0')}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
              }
            });
            return row;
          });
    
          return initial;
        }, {});
    
        const dataString = JSON.stringify(jsonData);
  
  // Parse the string to a JSON object
  const parsedData = JSON.parse(dataString);
  console.log(parsedData)
  
  // Get the first feuille (assuming it's the first key of the parsed object)
  const firstFeuilleKey = Object.keys(parsedData)[0]; // Get the first key
  const firstFeuille = parsedData[firstFeuilleKey];  // Get the corresponding object
  console.log(firstFeuille)
  // Ensure firstFeuille is an array and pass it to mapToEmployerModel
  if (Array.isArray(firstFeuille)) {
    //this.processBulkEmployers(firstFeuille);
  } else {
    console.error("The first feuille is not an array. Unable to process.");
  }
  
  
  // Pass it to the processBulkEmployers method
  //;
  
        document.getElementById('output').innerHTML = dataString.slice(0, 300).concat("...");
        this.setDownload(dataString);
      };
      reader.readAsBinaryString(file);
    }
  
    setDownload(data) {
      this.willDownload = true;
      setTimeout(() => {
        const el = document.querySelector("#download");
        el.setAttribute("href", `data:text/json;charset=utf-8,${encodeURIComponent(data)}`);
        el.setAttribute("download", 'xlsxtojson.json');
      }, 1000)
    }
  
    selectedFileName: string | null = null;
  
    // Trigger the hidden file input
    triggerFileInput(): void {
      const fileInput = document.getElementById('fileInput') as HTMLInputElement;
      fileInput.value = '';  // Reset file input value to allow re-selection
      fileInput.click();
    }
  
    processBulkEmployers(employersData: any[]): void {
      // Ensure the data is passed as an array
      if (!Array.isArray(employersData) || employersData.length === 0) {
        this.showAlert('error', 'Invalid employer data. Please provide a non-empty array.', 'Validation Error');
        return;
      }
    
      this.loadingData = true;
      this.msg = "Uploading file...";
    
       this.service.createOrUpdateBulkEmployers(this.mapToEmployerModel(employersData)).subscribe({
        next: (response) => {
          // Success: Display success message and handle response
          this.showAlert('success', response.message || 'Employers processed successfully.', 'Success');
          this.loadingData = false;
        },
        error: (error) => {
          // Error: Display error message based on the error status
          if (error.status === 400) {
            this.showAlert('error', error.error?.message || 'Invalid input data.', 'Bad Request');
          } else if (error.status === 404) {
            this.showAlert('error', error.error?.message || 'No matching user.', 'User Not Found');
          } else if (error.status === 500) {
            this.showAlert('error', error.error?.message || 'Internal server error.', 'Server Error');
          } else {
            this.showAlert('error', error.message || 'An unknown error occurred.', 'Unexpected Error');
          }
          this.loadingData = false;
        },
      }); 
    }
    
    mapToEmployerModel(feuilleData: any[]): any[] {
      return feuilleData.map((item: any) => {
        return {
          Id_Empl: item['ID Employee'],
          name_E: item['Emp Full Name'],
          Gender: item['Gender'],
          Birth_Date: item['Birthdate'],
          ID_job: this.extractCode(item['JOB']),
          HC_Type: item['HC Type'],
          Local_Position: item['Local Position Title'],
          Plant: item['Company'],
          Scope: item['Scope'],
          ID_Department: this.extractCode(item['Department']),
          Cost_Center: item['Cost Center'],
          Hiring_Date: item['Hiring Date'],
          Termination_Date: item['Termination Date'],
          Termination_Reason: item['Termination Reason'],
        };
      });
    }
    
    
    // Utility method to extract the code before the first space or colon
    extractCode(value: string): string {
      if (!value) return ''; // Handle empty or undefined values
      return value.split(/[:\s]/)[0]; // Split by colon or space and take the first part
    }
    
  
    convertStringToDate(dateString: string): Date {
      const [year, month, day] = dateString.split('-').map((part: string) => parseInt(part, 10));
      return new Date(year, month - 1, day);
    }
    onSubmit(): void {
      if (this.employeeForm.valid) {
        const formData = this.employeeForm.value;
    
        // Convert dates (if valid) to 'YYYY-MM-DD' format
        ['Birth_Date', 'Hiring_Date', 'Termination_Date'].forEach(dateField => {
          if (formData[dateField] && formData[dateField].isValid()) {
            formData[dateField] = formData[dateField].format('YYYY-MM-DD');
          }
        });
    
        // Call the service to create the employer
        this.service.createSingleEmployer(formData).subscribe(
          data => {
            // Show success alert if the employer is created successfully
            this.showAlert('success', 'Employer created successfully!', 'Success');
          },
          error => {
            // Show error alert if there's an error during submission
            this.showAlert('error', 'There was an error creating the employer. Please try again.', 'Error');
          }
        );
    
      } else {
        console.error('Form is invalid');
        this.employeeForm.markAllAsTouched(); // Highlight invalid fields
      
        // Generate a list of invalid fields
        const invalidFields = Object.keys(this.employeeForm.controls)
          .filter(field => this.employeeForm.controls[field].invalid);
      
        let errorMessage: string;
      
        if (invalidFields.length > 3) {
          errorMessage = 'There are too many invalid fields. Please check the form and try again.';
        } else if (invalidFields.length > 0) {
          errorMessage = `The following fields are invalid: ${invalidFields.join(', ')}. Please correct them and try again.`;
        } else {
          errorMessage = 'Form is invalid. Please check the fields and try again.';
        }
      
        this.showAlert('error', errorMessage, 'Error');
      }
      
      
    }
    
    

  onCancel(): void {
    // Reset the form to its initial state
    this.employeeForm.reset();
    console.log('Form has been reset');
  }
//alert
    
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
  

}
