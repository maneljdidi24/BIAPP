import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MatDatepickerInputEvent } from '@angular/material/datepicker';
import { UserService } from 'app/core/user/user.service';
import { User } from 'app/core/user/user.types';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-selection',
  templateUrl: './selection.component.html',
  styleUrls: ['./selection.component.scss']
})
export class SelectionComponent implements OnInit {
  selectedDateStart: any;
  selectedDateEnd: any;
  selectedRegion: string;
  user: any[][];
  position: any;
  type: any;

  currentUser: any;
  isAdmin: any;
  cards: any[] = [
    {
      ID:'Sales',
      title: "Sales Reports",
      description: "Explore detailed sales reports to manage and optimize your sales projects.",
      icon: "heroicons_outline:chart-pie",
      disabled: true
    },
    {
      ID:'Purchasing',
      title: "Purchasing Reports",
      description: "Explore detailed purchase reports to efficiently manage your purchase projects.",
      icon: "heroicons_outline:shopping-bag",
      disabled: true
    },
    {
      ID:'Purchasing',
      title: "Metal Purchasing Reports",
      description: "Explore detailed Metal purchase reports to efficiently manage your projects.",
      icon: "heroicons_outline:shopping-bag",
      disabled: true
    },    
    {
      ID:'LME',
      title: "Auto-bridge Reports",
      description: "Explore detailed purchase reports to efficiently manage your purchase projects.",
      icon: "heroicons_outline:chart-bar",
      disabled: true
    },
    {
      ID:'energy',
      title: "Energy Reports",
      description: "Track energy usage across Coficab production operations and identify opportunities for cost savings.",
      icon: "heroicons_outline:lightning-bolt",
      disabled: true
    },
    {
      ID:'stock',
      title: "Machines KPIs Reports",
      description: "Explore key performance indicators (KPIs) reports to track and analyze business performance metrics.",
      icon: "heroicons_outline:chart-bar",
      disabled: true
    },
    {
      ID:'stock',
      title: "Stock Reports",
      description: "Explore detailed stock reports to manage inventory levels and optimize supply chain operations.",
      icon: "heroicons_outline:cube",
      disabled: true 
    },
    {
      ID:'Manufacturing',
      title: "Manufacturing Reports",
      description: "Explore detailed manufacturing reports to analyze production processes and improve efficiency.",
      icon: "heroicons_outline:cog",
      disabled: true 
    },
    
  ];

  constructor(private router: Router, private route: ActivatedRoute, private serviceUser: UserService
  ) { }

/*   Type
admin
reports
reports
top_management
admin
Sustainability  */

  ngOnInit(): void {

    this.cardcheck()
  }

  cardcheck() {
    const u = JSON.parse(localStorage.getItem("user"))
    if (u.Type == 'admin') {
      this.cards.forEach(card => {
        card.disabled = false;
      });
    }
    else if (u.Type == 'reports') {
      
      u.Projects.forEach(e => {
        this.cards.forEach(card => {
          if (card.ID == e) {
            card.disabled = false;
          }
        });
      });
      

    }
  }
  onButtonClicked(card: any): void {
    // Navigate to the desired page based on the card information
    if (card.title === 'Purchasing Reports') {
      this.router.navigate(['/dashboards/project/report/purchase']);
    } else if (card.title === 'Metal Purchasing Reports') {
      this.router.navigate(['/dashboards/project/report/metal']);
    }else if (card.title === 'Sales Reports') {
      this.router.navigate(['/dashboards/project/sales/1']);
    }
  }

  onDateStartChange(event: MatDatepickerInputEvent<Date>): void {
    const nextDate = new Date(event.value); 
    nextDate.setDate(event.value.getDate() + 1);
    const formattedDate: string = nextDate.toISOString().substring(0, 10);
    this.selectedDateStart = formattedDate;
  }

  onDateEndChange(event: any): void {
    const nextDate = new Date(event.value); 
    nextDate.setDate(event.value.getDate() + 1);
    const formattedDate: string = nextDate.toISOString().substring(0, 10);
    this.selectedDateEnd = formattedDate;
  }

  onSelectionChange(event: any): void {
    this.selectedRegion = event.value;
  }
  redirectToDisplayPage(): void {
    if (this.selectedDateStart && this.selectedDateEnd && this.selectedRegion) {
      if (this.selectedDateStart <= this.selectedDateEnd) {
        const url = '/dashboards/project/display/' + this.selectedDateStart + '/' + this.selectedDateEnd + '/' + this.selectedRegion;
        this.router.navigateByUrl(url);
      } else {
        alert('Start date cannot be after the end date');
      }
    } else {
      let errorMessage = 'Please select ';
      if (!this.selectedRegion) {
        errorMessage += 'region';
      }
      if (!this.selectedDateStart && !this.selectedDateEnd) {
        if (!this.selectedRegion) {
          errorMessage += ', ';
        }
        errorMessage += 'start date and End date';
      } else if (!this.selectedDateStart) {
        if (!this.selectedRegion) {
          errorMessage += ', ';
        }
        errorMessage += 'start date';
      } else if (!this.selectedDateEnd) {
        if (!this.selectedRegion) {
          errorMessage += ', ';
        }
        errorMessage += 'End date';
      }
      errorMessage += ' to proceed';

      alert(errorMessage);
    }
  }

  navigateToSalesReports() {
    throw new Error('Method not implemented.');
  }

  navigateToPurchaseReports(project: any) {
    const url = '/dashboards/project/report/' + project;
    this.router.navigateByUrl(url);
  }

}