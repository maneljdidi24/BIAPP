
import { ServiceService } from '../service.service';
import { Component, AfterViewInit, ViewChild, OnInit, Inject } from '@angular/core';
import {MatPaginator} from '@angular/material/paginator';
import {MatTableDataSource} from '@angular/material/table';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSelectChange } from '@angular/material/select';
import * as XLSX from 'xlsx';
import { MatDatepickerInputEvent } from '@angular/material/datepicker';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { FuseConfirmationService } from '@fuse/services/confirmation';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { FuseAlertComponent } from '@fuse/components/alert';
import { AlertComponent } from 'app/modules/admin/ui/fuse-components/components/alert/alert.component';
import { NotificationService } from 'app/services/notification.service';
import { ReplaySubject } from 'rxjs';
import { User } from 'app/core/user/user.types';



@Component({
  selector: 'app-display',
  templateUrl: './display.component.html',
  styleUrls: ['./display.component.scss']
})
export class DisplayComponent implements OnInit {


  dataloaded!:any[];

  configForm!: FormGroup;
  reportForm: FormGroup;
  project: any;
  loadingData: boolean = false;
    constructor(private dialog: MatDialog,
       private route: ActivatedRoute, private service: ServiceService, private notificationService: NotificationService,
       private router: Router,  private _formBuilder: FormBuilder,
       private _fuseConfirmationService: FuseConfirmationService,
       private fb: FormBuilder) {}

  ngOnInit(): void {


    this.project =  this.route.snapshot.params['project'];
    this.reportForm = this._formBuilder.group({
      plant: ['', Validators.required],
      startDate: ['', Validators.required],
      endDate: ['', Validators.required]
    });
    
  }

  formatDate(date: Date): string {
    const datePipe = new DatePipe('en-US');
    return datePipe.transform(date, 'yyyy-MM-dd') || '';
  }

  onSubmit(): void {
    if (this.reportForm.valid) {

      this.loaddata(this.reportForm.get('plant').value,this.formatDate(this.reportForm.get('startDate').value),
      this.formatDate(this.reportForm.get('endDate').value));
 
    } else {
      // Handle form validation errors if needed
    }

    
    }



    loaddata(plant:any,start:any,end:any) {
      this.service.getDB(plant,start,end,this.project).subscribe((data)=>{
        this.dataloaded=data
      })
    }





    handleInput(event: any, PO_Number: any, PO_Line: any, Receipt_Number: any, Receipt_Number_Lines: any): void {
      const newValue = event.target.value; // Assuming the new value comes from the input field
      this.service.updateInvestment(PO_Number, PO_Line, Receipt_Number, Receipt_Number_Lines, newValue)
        .subscribe(data => {
          if (data.code == 200) {
            this.notificationService.success(data.msg);
            
            // Find the index of the modified row in dataloaded array
            const rowIndex = this.dataloaded.findIndex(item => 
              item.PO_Number === PO_Number && 
              item.PO_Line === PO_Line && 
              item.Receipt_Number === Receipt_Number && 
              item.Receipt_Number_Lines === Receipt_Number_Lines
            );
            
            // If the row exists in dataloaded array, update its invest value
            if (rowIndex !== -1) {
              this.dataloaded[rowIndex].invest = newValue;
            }
            
            // Optionally, you can reassign the dataloaded array to trigger change detection
            this.dataloaded = [...this.dataloaded];
            this._fuseConfirmationService.open(this.configForm.value);
          } else {
            this.notificationService.error(data.msg);
            this._fuseConfirmationService.open(this.configForm.value);
          }
        }, error => {
          console.error('Failed to update investment:', error);
          // Handle error, e.g., display an error message
        });
    }
    
   
  


   



   /* applyFilter(event: Event) {
      const filterValue = (event.target as HTMLInputElement).value;
      this.dataSource.filter = filterValue.trim().toLowerCase();
  
      if (this.dataSource.paginator) {
        this.dataSource.paginator.firstPage();
      }
    }*/
/*     clearFilter(){
      this.loaddata();
    }
    applyFilterBYPO(event: Event) {
      const filterValue = (event.target as HTMLInputElement).value;
      this.dataSource.filterPredicate = (data: any) => {
        const purchaseOrder = data[0].toLowerCase(); // Replace 'YourDataType' with the actual type of your data
        return purchaseOrder.includes(filterValue.trim().toLowerCase());
      };
      
      this.dataSource.filter = filterValue.trim().toLowerCase();
    
      if (this.dataSource.paginator) {
        this.dataSource.paginator.firstPage();
      }
    }
    applyFilterBYitem(event: Event) {
      const filterValue = (event.target as HTMLInputElement).value;
      this.dataSource.filterPredicate = (data: any) => {
        const purchaseOrder = data[12].toLowerCase(); // Replace 'YourDataType' with the actual type of your data
        return purchaseOrder.includes(filterValue.trim().toLowerCase());
      };
      
      this.dataSource.filter = filterValue.trim().toLowerCase();
    
      if (this.dataSource.paginator) {
        this.dataSource.paginator.firstPage();
      }
    }
    applyFilterBYDepart(event: Event) {
      const filterValue = (event.target as HTMLInputElement).value;
      this.dataSource.filterPredicate = (data: any) => {
        const purchaseOrder = data[19].toLowerCase(); // Replace 'YourDataType' with the actual type of your data
        return purchaseOrder.includes(filterValue.trim().toLowerCase());
      };
      
      this.dataSource.filter = filterValue.trim().toLowerCase();
    
      if (this.dataSource.paginator) {
        this.dataSource.paginator.firstPage();
      }
    }
    applyFilterBYCountry(event: Event) {
      const filterValue = (event.target as HTMLInputElement).value;
      this.dataSource.filterPredicate = (data: any) => {
        const purchaseOrder = data[17].toLowerCase(); // Replace 'YourDataType' with the actual type of your data
        return purchaseOrder.includes(filterValue.trim().toLowerCase());
      };
      
      this.dataSource.filter = filterValue.trim().toLowerCase();

      if (this.dataSource.paginator) {
        this.dataSource.paginator.firstPage();
      }
    }
    applyFilterBYBP(event: Event) {
      const filterValue = (event.target as HTMLInputElement).value;
      this.dataSource.filterPredicate = (data: any) => {
        const purchaseOrder = data[16].toLowerCase(); // Replace 'YourDataType' with the actual type of your data
        return purchaseOrder.includes(filterValue.trim().toLowerCase());
      };
      
      this.dataSource.filter = filterValue.trim().toLowerCase();
    
      if (this.dataSource.paginator) {
        this.dataSource.paginator.firstPage();
      }
    }

    
    
    onSelectionChangePlant(event: MatSelectChange) {
      const filterValue = event.value;
      this.dataSource.filterPredicate = (data: any) => {
        const purchaseOrder = data[23].toLowerCase(); // Replace 'YourDataType' with the actual type of your data
        return purchaseOrder.includes(filterValue.trim().toLowerCase());
      };
      
      this.dataSource.filter = filterValue.trim().toLowerCase();
    
      if (this.dataSource.paginator) {
        this.dataSource.paginator.firstPage();
      }
    }

      onSelectionChange(event: MatSelectChange) {
        const filterValue = event.value;
        this.dataSource.filterPredicate = (data: any) => {
          const purchaseOrder = data[10].toLowerCase(); // Replace 'YourDataType' with the actual type of your data
          return purchaseOrder.includes(filterValue.trim().toLowerCase());
        };
        
        this.dataSource.filter = filterValue.trim().toLowerCase();
      
        if (this.dataSource.paginator) {
          this.dataSource.paginator.firstPage();
        }
      }
      onDateChange(event: MatDatepickerInputEvent<Date>) {
        
        // Access the selected date
        const filterValue: Date = event.value;
        const nextDate = new Date(filterValue); // Create a new date object with the current date
        nextDate.setDate(filterValue.getDate() + 1);
        const formattedDate: string = nextDate.toISOString().substring(0, 10);
        alert(formattedDate)
        this.dataSource.filterPredicate = (data: any) => {
          const purchaseOrder = data[4]; // Replace 'YourDataType' with the actual type of your data
          if (purchaseOrder== formattedDate)
          alert(formattedDate)
          return purchaseOrder== formattedDate;
        };
        
        this.dataSource.filter = formattedDate.toString();
      
        if (this.dataSource.paginator) {
          this.dataSource.paginator.firstPage();
        }
      }


      exportToExcel() {
        const filename = "PurchaseOrderRepport.xlsx";
        const data = this.dataloaded;
      
        // Define the header names
        const headerNames = ['PO_Number','PO_Line','Old_Po','Old_POLines','Order_Date','Discount_Amount','Net_Order_Amount',
        'Unit_Price','Exchange_Rate_EUR','Unit','Currency','Ordered_Quantity','Item_ID','Item_family','Description','Business_PartnerID',
        'Business_Partner','BusinessPartner_Country', 'Department_ID', 'Department', 'leadSite_ID', 'leadSite', 'Region_ID', 
        'Region_Name', 'Cost_center', 'IVG', 'RFQ', 'RFQ_Line', 'Purchase_Requisition', 'PR_Line', 'PR_Creation_Date', 'PR_Accepting_Date', 
        'PR_Final_Approval_Date', 'PR_Processed_Date', 'Receipt_Number','Receipt_Number_Lines', 'Actual_Receipt_Date', 'Receipt_Amount', 
        'Received_Quantity', 'Payment_terms', 'Credit_note', 'CostSaving', 'warehouse'];
      
        // Create an array that includes the header row and the data rows
        const excelData = [headerNames, ...data];
      
        // Convert the data into an Excel worksheet
        const worksheet: XLSX.WorkSheet = XLSX.utils.aoa_to_sheet(excelData);
      
        // Create the workbook
        const workbook: XLSX.WorkBook = { Sheets: { 'Sheet1': worksheet }, SheetNames: ['Sheet1'] };
      
        // Convert the workbook to an array buffer
        const excelBuffer: any = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
      
        // Save the file
        this.saveAsExcelFile(excelBuffer, filename);
      }
      
      private saveAsExcelFile(buffer: any, filename: string) {
        alert("Excel file ready")
        const data: Blob = new Blob([buffer], { type: 'application/octet-stream' });
        const url: string = window.URL.createObjectURL(data);
        const link: HTMLAnchorElement = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.click();
      
        setTimeout(() => {
          window.URL.revokeObjectURL(url);
        }, 100);
      }
       */
     
      /*   openDialog(): void {
    const dialogRef: MatDialogRef<ModalWindowComponent> = this.dialog.open(ModalWindowComponent, {
      data:{displayedColumns : this.displayedColumns ,
        columnVisibility : this.columnVisibility}// If you need to pass data to the dialog, you can add it here
    });

    // After the dialog is closed, get the selected item
    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.displayedColumns = result.displayedColumns;
        this.columnVisibility = result.columnVisibility;
      }
    });} */
    /* toggleColumnVisibility(column) {
  const columnDef = this.columnVisibility.find((col) => col.columnName === column);
  if (columnDef) {
    const index = this.displayedColumns.indexOf(columnDef.columnName);
    if (index !== -1) {
      // Remove the column if it exists in the displayedColumns array
      this.displayedColumns.splice(index, 1);
    } else {
      alert(columnDef.columnName);

      // Insert the column at the desired position in the displayedColumns array
      const insertIndex = 2; // Specify the desired position here
      this.displayedColumns.splice(columnDef.where, 0, columnDef.columnName);
    }
  }
} */

}
