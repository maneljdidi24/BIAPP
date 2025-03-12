import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {

  constructor( private _router: Router) { }

  items = [
    {
      type: '0',
      image: '../../../../../assets/images/logo/la-saisie-des-donnees.png',
      title: 'Data Entry & Updates',
      description: 'Easily input and update sustainability metrics.',
    }, 
    {
      type: '1',
      image: '../../../../../assets/images/reports_14967872.png',
      title: 'Data Visualisation',
      description: 'Track sustainability metrics and progress.',
    },
    {
      type: '2',
      image: '../../../../../assets/images/reach_4730948.png',
      title: 'Performance Dashboard',
      description: 'Analyze performance with Power Bi dashboards.',
    }
  ];
  
  
  Sutainability : string = 'https://app.powerbi.com/reportEmbed?reportId=3f689bcd-331f-4061-afce-3a2019612367&autoAuth=true&ctid=b03e686d-b8c3-4e98-8091-91aec9e4c02f';

  ngOnInit(): void {
  }

  navigateTo(url) {
    this._router.navigateByUrl(url);
  }

  click(type){
    if(type==1){
      this.navigateTo('/sustainability/main/performance')
    }
    if(type==0){
      this.navigateTo('/sustainability/main/addP')
    }
    else if(type==2){
      this.openPowerBi("Sutainability")
    }
  }
  

  openPowerBi(project: string): void {
      const url = this[project];
      if (url) {
        const windowName = `powerbi_${project}`;
        let win = window.open(url, windowName);
  
        // If the window is already open, focus on it
        if (win) {
          win.focus();
        }
      } else {
        console.error('Invalid project name');
      }
    }
}
