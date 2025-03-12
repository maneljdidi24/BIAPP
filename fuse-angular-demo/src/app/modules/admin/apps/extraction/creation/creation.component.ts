import { Component, OnInit } from '@angular/core';
import { ServiceService } from '../service.service';

@Component({
  selector: 'app-creation',
  templateUrl: './creation.component.html',
  styleUrls: ['./creation.component.scss']
})
export class CreationComponent implements OnInit {

  data: any | undefined;
  constructor(private projet: ServiceService) { }

  ngOnInit(): void {
    this.loadData()
 
  }

 
  loadData(){
    this.projet.getALLDataFromDB("102").subscribe((data: any) => {
        this.data = data
    })
  }
}
