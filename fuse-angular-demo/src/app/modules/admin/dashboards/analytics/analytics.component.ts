import { ChangeDetectionStrategy, Component, OnDestroy, OnInit, ViewEncapsulation } from '@angular/core';
import { Router } from '@angular/router';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { ApexOptions } from 'ng-apexcharts';
import { ActivatedRoute } from '@angular/router';
import { AnalyticsService } from 'app/modules/admin/dashboards/analytics/analytics.service';

@Component({
    selector       : 'analytics',
    templateUrl    : './analytics.component.html',
    encapsulation  : ViewEncapsulation.None,
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class AnalyticsComponent implements OnInit, OnDestroy
{
    chartVisitors: ApexOptions;
    chartConversions: ApexOptions;
    chartImpressions: ApexOptions;
    chartVisits: ApexOptions;
    chartVisitorsVsPageViews: ApexOptions;
    chartNewVsReturning: ApexOptions;
    chartGender: ApexOptions;
    chartAge: ApexOptions;
    chartLanguage: ApexOptions;
    data: any;
    items = [
        {
          type: 'LME',
          image: '../../../../../assets/images/2.png',
          title: 'Auto Bridge',
          description: 'London Metal Exchange dashboards',
          disabled: true
        },
        {
          type: 'Purchasing',
          image: '../../../../../assets/images/3.png',
          title: 'Metal Purchasing Dashboards',
          description: 'Metal purchasing data insights',
          disabled: true
        },
        {
          type: 'Commodities',
          image: '../../../../../assets/images/4.png',
          title: 'Commodities & Forex Market Outlook 2024',
          description: 'Procurement analytics',
          disabled: true
        },
        {
          type: 'Sales',
          image: '../../../../../assets/images/1.png',
          title: 'Sales Dashboards',
          description: 'Sales performance analysis',
          disabled: true
        },
        {
          type: 'energy',
          image: '../../../../../assets/images/5.png',
          title: 'Energy Dashboards',
          description: 'Energy consumption monitoring',
          disabled: true
        }
      ];

    private _unsubscribeAll: Subject<any> = new Subject<any>();

    /**
     * Constructor
     */
    constructor(
        private _analyticsService: AnalyticsService,
        private _router: Router
    )
    {
    }


    Sales: string = 'https://app.powerbi.com/reportEmbed?reportId=2d70ea3a-4772-4f0d-9c6d-829fcaee960b&autoAuth=true&ctid=b03e686d-b8c3-4e98-8091-91aec9e4c02f';
    LME: string = 'https://app.powerbi.com/reportEmbed?reportId=8aff600e-5959-4936-bf30-07a59e0fccd7&autoAuth=true&ctid=b03e686d-b8c3-4e98-8091-91aec9e4c02f';
    Sutainability : string = 'https://app.powerbi.com/reportEmbed?reportId=3f689bcd-331f-4061-afce-3a2019612367&autoAuth=true&ctid=b03e686d-b8c3-4e98-8091-91aec9e4c02f';
    Commodities : string = 'https://app.powerbi.com/reportEmbed?reportId=2c42d4de-1ceb-457f-8205-a6a1d8e33939&autoAuth=true&ctid=b03e686d-b8c3-4e98-8091-91aec9e4c02f'
    energy : string = ''

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
    // -----------------------------------------------------------------------------------------------------
    // @ Lifecycle hooks
    // -----------------------------------------------------------------------------------------------------

    navigateTo(project: any) {
        const url = '/dashboards/analytics/' + project;
        this._router.navigateByUrl(url);
      }
    /**
     * On init
     */
    ngOnInit(): void
    {
       this.check()
       this.sortItems()
        // Get the data
   /*      this._analyticsService.data$
            .pipe(takeUntil(this._unsubscribeAll))
            .subscribe((data) => {

                // Store the data
                this.data = data;

                // Prepare the chart data
                this._prepareChartData();
            });

        // Attach SVG fill fixer to all ApexCharts
        window['Apex'] = {
            chart: {
                events: {
                    mounted: (chart: any, options?: any): void => {
                        this._fixSvgFill(chart.el);
                    },
                    updated: (chart: any, options?: any): void => {
                        this._fixSvgFill(chart.el);
                    }
                }
            }
        }; */
    }

    check(){
        const u = JSON.parse(localStorage.getItem("user"))

        if (u.Type == 'admin') {
          this.items.forEach(card => {
            card.disabled = false;
          });
        }
        else if (u.Type == 'reports') {
    
          u.Projects.forEach(e => {
            
            this.items.forEach(card => {
              if (card.type === e) {
                card.disabled = false;
              }
            });
          });
          
    
        }
    }

    sortItems() {
        this.items.sort((a, b) => {
          // Sort by disabled status first, then by original index if disabled status is the same
          if (a.disabled === b.disabled) {
            return 0; // maintain original order if both are the same
          }
          return a.disabled ? 1 : -1; // enabled items come before disabled items
        });
      }

    /**
     * On destroy
     */
    ngOnDestroy(): void
    {
        // Unsubscribe from all subscriptions
        this._unsubscribeAll.next();
        this._unsubscribeAll.complete();
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Public methods
    // -----------------------------------------------------------------------------------------------------

    /**
     * Track by function for ngFor loops
     *
     * @param index
     * @param item
     */
    trackByFn(index: number, item: any): any
    {
        return item.id || index;
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Private methods
    // -----------------------------------------------------------------------------------------------------

    /**
     * Fix the SVG fill references. This fix must be applied to all ApexCharts
     * charts in order to fix 'black color on gradient fills on certain browsers'
     * issue caused by the '<base>' tag.
     *
     * Fix based on https://gist.github.com/Kamshak/c84cdc175209d1a30f711abd6a81d472
     *
     * @param element
     * @private
     */
/*     private _fixSvgFill(element: Element): void
    {
        // Current URL
        const currentURL = this._router.url;

        // 1. Find all elements with 'fill' attribute within the element
        // 2. Filter out the ones that doesn't have cross reference so we only left with the ones that use the 'url(#id)' syntax
        // 3. Insert the 'currentURL' at the front of the 'fill' attribute value
        Array.from(element.querySelectorAll('*[fill]'))
             .filter(el => el.getAttribute('fill').indexOf('url(') !== -1)
             .forEach((el) => {
                 const attrVal = el.getAttribute('fill');
                 el.setAttribute('fill', `url(${currentURL}${attrVal.slice(attrVal.indexOf('#'))}`);
             });
    } */

    /**
     * Prepare the chart data from the data
     *
     * @private
     */
/*     private _prepareChartData(): void
    {
        // Visitors
        this.chartVisitors = {
            chart     : {
                animations: {
                    speed           : 400,
                    animateGradually: {
                        enabled: false
                    }
                },
                fontFamily: 'inherit',
                foreColor : 'inherit',
                width     : '100%',
                height    : '100%',
                type      : 'area',
                toolbar   : {
                    show: false
                },
                zoom      : {
                    enabled: false
                }
            },
            colors    : ['#818CF8'],
            dataLabels: {
                enabled: false
            },
            fill      : {
                colors: ['#312E81']
            },
            grid      : {
                show       : true,
                borderColor: '#334155',
                padding    : {
                    top   : 10,
                    bottom: -40,
                    left  : 0,
                    right : 0
                },
                position   : 'back',
                xaxis      : {
                    lines: {
                        show: true
                    }
                }
            },
            series    : this.data.visitors.series,
            stroke    : {
                width: 2
            },
            tooltip   : {
                followCursor: true,
                theme       : 'dark',
                x           : {
                    format: 'MMM dd, yyyy'
                },
                y           : {
                    formatter: (value: number): string => `${value}`
                }
            },
            xaxis     : {
                axisBorder: {
                    show: false
                },
                axisTicks : {
                    show: false
                },
                crosshairs: {
                    stroke: {
                        color    : '#475569',
                        dashArray: 0,
                        width    : 2
                    }
                },
                labels    : {
                    offsetY: -20,
                    style  : {
                        colors: '#CBD5E1'
                    }
                },
                tickAmount: 20,
                tooltip   : {
                    enabled: false
                },
                type      : 'datetime'
            },
            yaxis     : {
                axisTicks : {
                    show: false
                },
                axisBorder: {
                    show: false
                },
                min       : (min): number => min - 750,
                max       : (max): number => max + 250,
                tickAmount: 5,
                show      : false
            }
        };

        // Conversions
        this.chartConversions = {
            chart  : {
                animations: {
                    enabled: false
                },
                fontFamily: 'inherit',
                foreColor : 'inherit',
                height    : '100%',
                type      : 'area',
                sparkline : {
                    enabled: true
                }
            },
            colors : ['#38BDF8'],
            fill   : {
                colors : ['#38BDF8'],
                opacity: 0.5
            },
            series : this.data.conversions.series,
            stroke : {
                curve: 'smooth'
            },
            tooltip: {
                followCursor: true,
                theme       : 'dark'
            },
            xaxis  : {
                type      : 'category',
                categories: this.data.conversions.labels
            },
            yaxis  : {
                labels: {
                    formatter: (val): string => val.toString()
                }
            }
        };

        // Impressions
        this.chartImpressions = {
            chart  : {
                animations: {
                    enabled: false
                },
                fontFamily: 'inherit',
                foreColor : 'inherit',
                height    : '100%',
                type      : 'area',
                sparkline : {
                    enabled: true
                }
            },
            colors : ['#34D399'],
            fill   : {
                colors : ['#34D399'],
                opacity: 0.5
            },
            series : this.data.impressions.series,
            stroke : {
                curve: 'smooth'
            },
            tooltip: {
                followCursor: true,
                theme       : 'dark'
            },
            xaxis  : {
                type      : 'category',
                categories: this.data.impressions.labels
            },
            yaxis  : {
                labels: {
                    formatter: (val): string => val.toString()
                }
            }
        };

        // Visits
        this.chartVisits = {
            chart  : {
                animations: {
                    enabled: false
                },
                fontFamily: 'inherit',
                foreColor : 'inherit',
                height    : '100%',
                type      : 'area',
                sparkline : {
                    enabled: true
                }
            },
            colors : ['#FB7185'],
            fill   : {
                colors : ['#FB7185'],
                opacity: 0.5
            },
            series : this.data.visits.series,
            stroke : {
                curve: 'smooth'
            },
            tooltip: {
                followCursor: true,
                theme       : 'dark'
            },
            xaxis  : {
                type      : 'category',
                categories: this.data.visits.labels
            },
            yaxis  : {
                labels: {
                    formatter: (val): string => val.toString()
                }
            }
        };

        // Visitors vs Page Views
        this.chartVisitorsVsPageViews = {
            chart     : {
                animations: {
                    enabled: false
                },
                fontFamily: 'inherit',
                foreColor : 'inherit',
                height    : '100%',
                type      : 'area',
                toolbar   : {
                    show: false
                },
                zoom      : {
                    enabled: false
                }
            },
            colors    : ['#64748B', '#94A3B8'],
            dataLabels: {
                enabled: false
            },
            fill      : {
                colors : ['#64748B', '#94A3B8'],
                opacity: 0.5
            },
            grid      : {
                show   : false,
                padding: {
                    bottom: -40,
                    left  : 0,
                    right : 0
                }
            },
            legend    : {
                show: false
            },
            series    : this.data.visitorsVsPageViews.series,
            stroke    : {
                curve: 'smooth',
                width: 2
            },
            tooltip   : {
                followCursor: true,
                theme       : 'dark',
                x           : {
                    format: 'MMM dd, yyyy'
                }
            },
            xaxis     : {
                axisBorder: {
                    show: false
                },
                labels    : {
                    offsetY: -20,
                    rotate : 0,
                    style  : {
                        colors: 'var(--fuse-text-secondary)'
                    }
                },
                tickAmount: 3,
                tooltip   : {
                    enabled: false
                },
                type      : 'datetime'
            },
            yaxis     : {
                labels    : {
                    style: {
                        colors: 'var(--fuse-text-secondary)'
                    }
                },
                max       : (max): number => max + 250,
                min       : (min): number => min - 250,
                show      : false,
                tickAmount: 5
            }
        };

        // New vs. returning
        this.chartNewVsReturning = {
            chart      : {
                animations: {
                    speed           : 400,
                    animateGradually: {
                        enabled: false
                    }
                },
                fontFamily: 'inherit',
                foreColor : 'inherit',
                height    : '100%',
                type      : 'donut',
                sparkline : {
                    enabled: true
                }
            },
            colors     : ['#3182CE', '#63B3ED'],
            labels     : this.data.newVsReturning.labels,
            plotOptions: {
                pie: {
                    customScale  : 0.9,
                    expandOnClick: false,
                    donut        : {
                        size: '70%'
                    }
                }
            },
            series     : this.data.newVsReturning.series,
            states     : {
                hover : {
                    filter: {
                        type: 'none'
                    }
                },
                active: {
                    filter: {
                        type: 'none'
                    }
                }
            },
            tooltip    : {
                enabled        : true,
                fillSeriesColor: false,
                theme          : 'dark',
                custom         : ({
                                      seriesIndex,
                                      w
                                  }): string => `<div class="flex items-center h-8 min-h-8 max-h-8 px-3">
                                                    <div class="w-3 h-3 rounded-full" style="background-color: ${w.config.colors[seriesIndex]};"></div>
                                                    <div class="ml-2 text-md leading-none">${w.config.labels[seriesIndex]}:</div>
                                                    <div class="ml-2 text-md font-bold leading-none">${w.config.series[seriesIndex]}%</div>
                                                </div>`
            }
        };

        // Gender
        this.chartGender = {
            chart      : {
                animations: {
                    speed           : 400,
                    animateGradually: {
                        enabled: false
                    }
                },
                fontFamily: 'inherit',
                foreColor : 'inherit',
                height    : '100%',
                type      : 'donut',
                sparkline : {
                    enabled: true
                }
            },
            colors     : ['#319795', '#4FD1C5'],
            labels     : this.data.gender.labels,
            plotOptions: {
                pie: {
                    customScale  : 0.9,
                    expandOnClick: false,
                    donut        : {
                        size: '70%'
                    }
                }
            },
            series     : this.data.gender.series,
            states     : {
                hover : {
                    filter: {
                        type: 'none'
                    }
                },
                active: {
                    filter: {
                        type: 'none'
                    }
                }
            },
            tooltip    : {
                enabled        : true,
                fillSeriesColor: false,
                theme          : 'dark',
                custom         : ({
                                      seriesIndex,
                                      w
                                  }): string => `<div class="flex items-center h-8 min-h-8 max-h-8 px-3">
                                                     <div class="w-3 h-3 rounded-full" style="background-color: ${w.config.colors[seriesIndex]};"></div>
                                                     <div class="ml-2 text-md leading-none">${w.config.labels[seriesIndex]}:</div>
                                                     <div class="ml-2 text-md font-bold leading-none">${w.config.series[seriesIndex]}%</div>
                                                 </div>`
            }
        };

        // Age
        this.chartAge = {
            chart      : {
                animations: {
                    speed           : 400,
                    animateGradually: {
                        enabled: false
                    }
                },
                fontFamily: 'inherit',
                foreColor : 'inherit',
                height    : '100%',
                type      : 'donut',
                sparkline : {
                    enabled: true
                }
            },
            colors     : ['#DD6B20', '#F6AD55'],
            labels     : this.data.age.labels,
            plotOptions: {
                pie: {
                    customScale  : 0.9,
                    expandOnClick: false,
                    donut        : {
                        size: '70%'
                    }
                }
            },
            series     : this.data.age.series,
            states     : {
                hover : {
                    filter: {
                        type: 'none'
                    }
                },
                active: {
                    filter: {
                        type: 'none'
                    }
                }
            },
            tooltip    : {
                enabled        : true,
                fillSeriesColor: false,
                theme          : 'dark',
                custom         : ({
                                      seriesIndex,
                                      w
                                  }): string => `<div class="flex items-center h-8 min-h-8 max-h-8 px-3">
                                                    <div class="w-3 h-3 rounded-full" style="background-color: ${w.config.colors[seriesIndex]};"></div>
                                                    <div class="ml-2 text-md leading-none">${w.config.labels[seriesIndex]}:</div>
                                                    <div class="ml-2 text-md font-bold leading-none">${w.config.series[seriesIndex]}%</div>
                                                </div>`
            }
        };

        // Language
        this.chartLanguage = {
            chart      : {
                animations: {
                    speed           : 400,
                    animateGradually: {
                        enabled: false
                    }
                },
                fontFamily: 'inherit',
                foreColor : 'inherit',
                height    : '100%',
                type      : 'donut',
                sparkline : {
                    enabled: true
                }
            },
            colors     : ['#805AD5', '#B794F4'],
            labels     : this.data.language.labels,
            plotOptions: {
                pie: {
                    customScale  : 0.9,
                    expandOnClick: false,
                    donut        : {
                        size: '70%'
                    }
                }
            },
            series     : this.data.language.series,
            states     : {
                hover : {
                    filter: {
                        type: 'none'
                    }
                },
                active: {
                    filter: {
                        type: 'none'
                    }
                }
            },
            tooltip    : {
                enabled        : true,
                fillSeriesColor: false,
                theme          : 'dark',
                custom         : ({
                                      seriesIndex,
                                      w
                                  }): string => `<div class="flex items-center h-8 min-h-8 max-h-8 px-3">
                                                    <div class="w-3 h-3 rounded-full" style="background-color: ${w.config.colors[seriesIndex]};"></div>
                                                    <div class="ml-2 text-md leading-none">${w.config.labels[seriesIndex]}:</div>
                                                    <div class="ml-2 text-md font-bold leading-none">${w.config.series[seriesIndex]}%</div>
                                                </div>`
            }
        };
    } */
}
