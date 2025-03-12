import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { NotificationService } from 'app/services/notification.service';
import { FuseConfirmationService } from '@fuse/services/confirmation';
import { DataService } from 'app/service.service';



@Component({
  selector: 'app-performance',
  templateUrl: './performance.component.html',
  styleUrls: ['./performance.component.scss']
})
export class PerformanceComponent implements OnInit {

  years: number[] = [];
  months: string[] = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  reportForm: FormGroup;
  yearControl = new FormControl();
  monthControl = new FormControl();
  dataUpdated : any[] = []
  showSaveButton: boolean = false;
  showUpdateButton: boolean = true;
  panelOpenState: boolean[] = []; // This array will track the open/close state of each panel
  topics: any[]
  performance: any[] = []
  dates: any[]
  elements: any[]
  loadingData: boolean = false;
  constructor(private service: DataService, private fb: FormBuilder 
    , private notificationService: NotificationService,
    private _fuseConfirmationService: FuseConfirmationService
  ) {
    this.years = this.generateYears(2020,2024);
  }
  showAlertBoolean: boolean = false;
  Msg :any;
  Title :any;
  plants:any[]
  Type:any;
  DisplayData : boolean = false;
  defaultPlant:any
  ngOnInit(): void {

    this.reportForm = this.fb.group({
      plant: [],
      years: this.yearControl,
      months: this.monthControl
    });
    this.loadplants()

    // Preselect the year 2024
    //this.yearControl.setValue([2024]);

    // Preselect the current month
    //const currentMonth = new Date().getMonth(); // getMonth() returns 0-based month index
    //this.monthControl.setValue([this.months[0]]);

    const formValue = this.reportForm.value;

    const payload = {
      plant: formValue.plant,
      years: formValue.years,
      months: formValue.months
    }

    //alert(payload.months)

    this.loadtopics()
    this.loadelement()
    //this.loadDates(payload)
    //this.LoadPerformances(payload)
    this.panelOpenState = this.topics.map(() => false);
  }

  getSlicedPlantValue(): string {
    const plantValue = this.reportForm.get('plant')?.value || '';
    return plantValue.length > 2 ? plantValue.slice(1, -1) : '';
  }



  togglePanel(index: number) {
    this.panelOpenState[index] = !this.panelOpenState[index];
  }

  loadtopics() {
    this.service.gettopics().subscribe((data) => {
      this.topics = data
    })
  }
  
  loadelement() {
    this.service.getelements().subscribe((data) => {
      this.elements = data
    })
  }

  loadDates(obj: any) {
    this.service.getditinctdate(obj).subscribe((data) => {
      this.dates = data
    })
  }

  loadplants() {
    this.service.GetPlantsforuser().subscribe(
      (data) => {
        // Filter out plants whose descriptions start with 'M' or 'm'
        this.plants = data.filter((plant: any) => !plant.plant_Description.toLowerCase().startsWith('m'));
    
        // Initialize form with the default plant
        
      }
    );
    
  }
  
  lastPlantValue:any

  LoadPerformances(objct: any) {
    
    this.service.getPerformancese(objct).subscribe(data => {
      if (data.code == 500) {
        this.loadingData = false;
        this.showAlert('error', data.msg, "Error");
        this.reportForm.patchValue({ plant: this.lastPlantValue });
      } else {
        const formValue = this.reportForm.value;
        this.performance = data;
        this.loadingData = false;
        this.lastPlantValue=formValue.plant
      }
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




  getPerformanceValue(element: string, date: string): string {
    const performanceItem = this.performance.find(p => p.Name_Element === element);
    if (performanceItem) {
      return performanceItem[date];
    } else {
      return "  0  ";
    }
  }

  transformDate(input: string): string {
    const months: { [key: string]: string } = {
      "January": "01",
      "February": "02",
      "March": "03",
      "April": "04",
      "May": "05",
      "June": "06",
      "July": "07",
      "August": "08",
      "September": "09",
      "October": "10",
      "November": "11",
      "December": "12"
    };
  
    // Split the input string to get the month and year
    const [month, year] = input.split(" ");
  
    // Get the corresponding month number
    const monthNumber = months[month];
  
    // Construct the date string in the format YYYY-MM-DD
    const formattedDate = `${year}-${monthNumber}-01`;
  
    return formattedDate;
  }

  onDataChange(event: Event, ID: string, date: string): void {
    const newName = (event.target as HTMLElement).innerText;
    const newNumber = parseInt(newName, 10);

    if (isNaN(newNumber)) {
     
        //return; // Exit the function early if input is not a valid integer
    }
    else {
      
      const newData = {
        data: newName,
        ID: ID,
        date: this.transformDate(date),
        plant: this.reportForm.value.plant
      };
    
      // Find the index of the existing item
      const index = this.dataUpdated.findIndex(item => 
        item.ID === newData.ID && item.date === newData.date && item.plant === newData.plant
      );
    
      // If an existing item is found, update its data
      if (index !== -1) {
        this.dataUpdated[index].data = newName;
      } else {
        // If no existing item is found, push the new data
        this.dataUpdated.push(newData);
      }
    }
    
  }
  
  

  total(element: string): any {
    const performanceItem = this.performance.find(p => p.Name_Element === element);
    if (performanceItem) {
      let somme = 0;
      this.dates.forEach(d => {
        somme = somme + performanceItem[d.Date]
      });
      return somme;
    } else {
      return "  0  ";
    }

  }
  
  total2(topic: string, d: any): any {
    let somme = 0;
    this.elements.forEach(e => {
      if (e.ID_Topic == topic) {
        const performanceItem = this.performance.find(p => p.Name_Element === e.Name_Element);
        if (performanceItem) {


          somme = somme + performanceItem[d.Date]

        }
      }
    })

    return somme;
  }

  generateYears(startYear: number, endYear: number): number[] {
    const years = [];
    for (let year = startYear; year <= endYear; year++) {
      years.push(year);
    }
    return years;
  }

  toggleMonths(year: number, event: MouseEvent) {
    event.stopPropagation();
    const selectedYears = this.yearControl.value as number[];
    if (selectedYears.includes(year)) {
      this.yearControl.setValue(selectedYears.filter(y => y !== year));
    } else {
      this.yearControl.setValue([...selectedYears, year]);
    }
  }

  onSubmit() {
    this.DisplayData= true;
    if (this.reportForm.valid) {
      this.loadingData = true;
      const formValue = this.reportForm.value;
      const payload = {
        plant: formValue.plant,
        years: formValue.years,
        months: formValue.months
      }

      this.loadDates(payload)
     this.LoadPerformances(payload)
    }
  }

  plantchanged : boolean = false;
  updatedMonth: any[] = [];
  updatedYear: any[] = [];

  plantchangedfunction(){
    this.service.fromPlantGetDate(this.reportForm.value.plant).subscribe(data => {
      // Filter unique years
      this.updatedYear = [...new Set(data.map(item => item.year))];
      
      // Map month numbers to their names
      this.updatedMonth = data.map(item => this.getMonthName(item.month));
     // Set default selections if only one option exists
     if (this.updatedYear.length === 1) {
      this.yearControl.setValue(this.updatedYear);
    }

    if (this.updatedMonth.length === 1) {
      this.monthControl.setValue(this.updatedMonth);
    }
     // Set plantchanged to true if there is at least one month
     if (this.updatedMonth.length > 0) {
      this.plantchanged = true;
    }else {
      this.showAlert('info', 'No data available for the selected plant.', 'Alert');
      this.plantchanged = false;  // Optionally set plantchanged to false
    }

    });
  }

    getMonthName(monthNumber: number): string {
      const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
      ];
      return monthNames[monthNumber - 1];
    }

}
