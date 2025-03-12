import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { filter, switchMap } from 'rxjs/operators';
@Component({
  selector: 'app-power-bi',
  templateUrl: './power-bi.component.html',
  styleUrls: ['./power-bi.component.scss']
})
export class PowerBIComponent implements OnInit {

  type:any;
  srct:any;
  constructor(private route: ActivatedRoute, 
    private router: Router) { }

    powerBiUrl: string = 'https://app.powerbi.com/reportEmbed?reportId=8aff600e-5959-4936-bf30-07a59e0fccd7&autoAuth=true&ctid=b03e686d-b8c3-4e98-8091-91aec9e4c02f';

    openPowerBi(b): void {
      alert(b)
      window.location.href = 'http://localhost:4200/test';
    }
    ngOnInit(): void {
      this.router.events.pipe(
        filter(event => event instanceof NavigationEnd),
        switchMap(() => this.route.snapshot.params['Powerbi'])
      ).subscribe(param => {
        this.type = param;

      });
      // Initial load
      this.type = this.route.snapshot.params['Powerbi'];

    }
  

}
