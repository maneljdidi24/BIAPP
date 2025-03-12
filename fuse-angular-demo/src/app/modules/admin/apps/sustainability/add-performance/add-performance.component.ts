import { Component, OnInit } from '@angular/core';
import { NotificationService } from 'app/services/notification.service';
import { FuseConfirmationService } from '@fuse/services/confirmation';
import { DataService } from 'app/service.service';


@Component({
  selector: 'app-add-performance',
  templateUrl: './add-performance.component.html',
  styleUrls: ['./add-performance.component.scss']
})
export class AddPerformanceComponent implements OnInit {

  showAlertBoolean: boolean = false;
  Type: any;
  Title: any;
  Msg: any;
  loaded: boolean
  dataUpdated: any[] = []
  topics: any[]
  plants: any[]
  month!: any;
  year!: any;
  plant!: any;
  elements: any[]
  elementsOfTopic: any[]
  months: string[] = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  years: string[] = [
    '2024','2023','2022','2021','2020'
  ];
  lastFourMonths: string[] = [];
  topic!: any;
  displaySaveButton: boolean = false;
  displayfordescription: boolean = false;

  constructor(private service: DataService) { }

  ngOnInit(): void {
    this.loadplants()
    this.loadtopics()
    this.loadelement()
    //this.setLastFourMonths();
  }

  loaddata() {
    
    if (this.loaded){
      this.onCancelDataChange()
    }
    if (this.month && this.plant && this.topic && this.year) {
      this.functiondisplayfordescription()
      this.loaded = true
      const getdata = {
        date: this.transformDateFromMonthYear(this.month, this.year),
        ID_Target: this.plant + this.year
      }

      this.LoadPerformances(getdata)
    }
    else {
      this.showAlert('info', 'Please select all informations before proceeding.', 'Missing Information');
    }
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

  loadplants() {
    this.service.GetPlantsforuser().subscribe(
      (data) => {
        this.plants = data.filter((plant: any) => !plant.plant_Description.toLowerCase().startsWith('m'));
      });
  }

functiondisplayfordescription(){
  if (this.topic == 14) this.displayfordescription=true
  else this.displayfordescription=false
}

  onTopicChange(event: any) {
    this.topic = event.value
  }

  loadelementsOfTopic(){

    this.elementsOfTopic = this.elements.filter(
      element => element.ID_Topic === this.topic
    );
  }

  
  onCancelDataChange() {
    this.dataUpdated = [];
    this.displaySaveButton = false;
  
    this.elementsOfTopic.forEach(element => {
      const matchingPerformance = this.performance.find(p => p.ID_E === element.ID_Element);
      if(this.displayfordescription){
        element.initialValue = matchingPerformance ? matchingPerformance.Description : '';
      }else{
        element.initialValue = matchingPerformance ? matchingPerformance.Qty : null;;
      }
      // Reset the 'changed' state to false
      element.changed = false; // Reset the changed state for color indication
    });
  }
  


  onMonthChange(event: any) {
    this.month = event.value; // Get the month name
  }

  onYearChange(event: any) {
// Assuming event.value is a valid date string or Date object
    this.year = event.value;
  }

  onPlantChange(event: any) {
    this.plant = event.value.plant
  }


  performance: any[]



  LoadPerformances(objct: any) {
    this.loadelementsOfTopic()
    this.service.display_performance_for_update(objct).subscribe(data => {
      if (data.code == 500) {
        this.showAlert('error', data.msg, "Error");
      } else {
        this.performance = data;

        this.elementsOfTopic.forEach(element => {

          const matchingPerformance = this.performance.find(p => p.ID_E === element.ID_Element);
          if(this.displayfordescription){
            element.initialValue = matchingPerformance ? matchingPerformance.Description : '';
          }else
          {
            element.initialValue = matchingPerformance ? matchingPerformance.Qty : null;}
        });
      }
      
    });
  }

 


/*   setLastFourMonths() {
    const currentDate = new Date();
    const currentMonthIndex = currentDate.getMonth(); // 0 = January, 11 = December
    const currentYear = currentDate.getFullYear();

    this.lastFourMonths = [];

    for (let i = 1; i <= 9; i++) {
      let monthIndex = currentMonthIndex - i;
      let year = currentYear;

      // Adjust year and month index if month index is less than 0
      if (monthIndex < 0) {
        monthIndex += 12; // Wrap around to previous year
        year--; // Decrease the year by 1
      }

      this.lastFourMonths.push(`${this.months[monthIndex]} ${year}`);
    }
  } */


  showAlert(type, msg, title) {
    this.Msg = msg;
    this.Title = title;
    this.Type = type;
    this.showAlertBoolean = true;
    setTimeout(() => {
      this.showAlertBoolean = false;
    }, 5000); // 3 seconds
  }



  transformDateFromMonthYear(monthName: string, year: number): string {


    // Get the month number (1-12) based on the month name
    const monthIndex = this.months.indexOf(monthName); // Returns -1 if not found
    const month = monthIndex + 1; // Convert 0-based index to 1-based month number

    // Ensure month is in 2 digits format
    const formattedMonth = month < 10 ? `0${month}` : `${month}`;

    // Return the date in '01/MM/YYYY' format (1st of the given month and year)
    return `${year}-${formattedMonth}-01`;
  }

  onInputChange(ID: string): void {

    // Find the element by ID and mark it as changed
    const element = this.elementsOfTopic.find(e => e.ID_Element === ID);
    if (element) {
      element.changed = true; // Set changed state to true
      this.displaySaveButton = true; // Show the save button
    }
  }
  

  onUpadetDataChange(event: Event, ID: string): void {
    const inputElement = event.target as HTMLInputElement; // Cast to HTMLInputElement
    const value = inputElement.value; // Get the value of the input field
  
    if (value) {
    // Create the common structure for newData
    const newData: any = {
      ID: ID,
      date: this.transformDateFromMonthYear(this.month, this.year),
      target: this.plant + this.year
    };

    // Add specific fields based on the condition
    if (this.displayfordescription) {
      newData.description = value;
    } else {
      newData.data = value;
    }
  
      // Find the index of the existing item
      const index = this.dataUpdated.findIndex(item =>
        item.ID === newData.ID && item.date === newData.date && item.target === newData.target
      );
  
      // If an existing item is found, update its data
      if (index !== -1) {
        this.dataUpdated[index].data = value;
      } else {
        // If no existing item is found, push the new data
        this.dataUpdated.push(newData);
        this.displaySaveButton = true;
      }
  
    }
  }

  onTopic2DataChange(event: Event){
    this.displaySaveButton = true;
    const inputElement = event.target as HTMLInputElement; // Cast to HTMLInputElement
    const value = inputElement.value; // Get the value of the input field

    if (value){
      console.log(value)
    }

  }
  



  saveupdate(): void {
    if (this.dataUpdated.length !== 0) {
      this.service.deleteInsertPerformance(this.dataUpdated).subscribe(data => {
        if (data.code == 200) {
          this.showAlert('success', data.msg, "Success");
          
          // Reset everything to normal after successful save
          this.elementsOfTopic.forEach(element => {
            element.changed = false; // Reset the 'changed' state
          });
        } else {
          this.showAlert('error', data.msg, "Error");
        }
      });
      
      this.dataUpdated = [];
      this.displaySaveButton = false;
    } else {
      this.showAlert('info', "No changes were detected. Please update the data before submitting.", "Notice");
    }
  }
  
  ondescriptionChange(element:any){
console.log(element)
  }


}
