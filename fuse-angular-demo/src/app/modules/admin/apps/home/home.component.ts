import { SocketService } from '../extraction/socket.service';
import {LiveAnnouncer} from '@angular/cdk/a11y';
import { ServiceService } from '../extraction/service.service';
import { Component, AfterViewInit, ViewChild, OnInit } from '@angular/core';
import {MatPaginator} from '@angular/material/paginator';
import {MatSort, Sort} from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';
import { ActivatedRoute, Router } from '@angular/router';
import { MatSelectChange } from '@angular/material/select';
import * as XLSX from 'xlsx';
import { MatDatepickerInputEvent } from '@angular/material/datepicker';

declare const google: any;
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  displayedColumns:any[] = ['PO_Number','PO_Line','Old_Po','Old_POLines','Order_Date','Discount_Amount','Net_Order_Amount',
  'Unit_Price','Exchange_Rate_EUR','Unit','Currency','Ordered_Quantity','Item_ID','Item_family','Description','Business_PartnerID',
  'Business_Partner','BusinessPartner_Country', 'Department_ID', 'Department', 'leadSite_ID', 'leadSite', 'Region_ID', 
  'Region_Name', 'Cost_center', 'IVG', 'RFQ', 'RFQ_Line', 'Purchase_Requisition', 'PR_Line', 'PR_Creation_Date', 'PR_Accepting_Date', 
  'PR_Final_Approval_Date', 'PR_Processed_Date', 'Receipt_Number','Receipt_Number_Lines', 'Actual_Receipt_Date', 'Receipt_Amount', 
  'Received_Quantity', 'Payment_terms', 'Credit_note', 'CostSaving', 'warehouse'];
  dataSource!: MatTableDataSource<any>;
  dataloaded!:any[][];

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  constructor(private route: ActivatedRoute, private service: ServiceService,  private router: Router,private liveAnnouncer: LiveAnnouncer) { 
    
  }
  ngOnInit() {
    this.loaddata();
  }

  loaddata(){
    this.service.getALLDataFromDB("102").subscribe((data)=>{
      this.dataloaded=data
      this.dataSource=new MatTableDataSource(this.dataloaded);
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;
    })
  }
// Component class
columnVisibility = {
  Old_Po: true,
  Old_POLines: true,
  Order_Date: true
};

  loadMap(): void {
    const mapOptions = {
      center: new google.maps.LatLng(0, 0),
      zoom: 2,
      disableDefaultUI: true,
      backgroundColor: 'black'
    };

    const map = new google.maps.Map(document.getElementById('map'), mapOptions);
    
    // Highlight small places on the map
    this.highlightPlaces(map);
  }

  highlightPlaces(map: any): void {
    // Add your code here to highlight specific places on the map
  }
}
