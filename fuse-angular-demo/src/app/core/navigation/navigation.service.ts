import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, ReplaySubject } from 'rxjs';
import { tap } from 'rxjs/operators';
import { Navigation } from 'app/core/navigation/navigation.types';

@Injectable({
    providedIn: 'root'
})
export class NavigationService
{
    private _navigation: ReplaySubject<Navigation> = new ReplaySubject<Navigation>(1);

    /**
     * Constructor
     */
    constructor(private _httpClient: HttpClient)
    {
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Accessors
    // -----------------------------------------------------------------------------------------------------

    /**
     * Getter for navigation
     */
    get navigation$(): Observable<Navigation>
    {
        return this._navigation.asObservable();
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Public methods
    // -----------------------------------------------------------------------------------------------------

    /**
     * Get all navigation data
     */
/*     get(): Observable<Navigation>
    {
        return this._httpClient.get<Navigation>('api/common/navigation').pipe(
            tap((navigation) => {
                navigation.default.forEach(p=>alert(p.title)) 
                alert(JSON.parse(localStorage.getItem("user")).type)
                this._navigation.next(navigation);
            })
        );
    } */

        get(): Observable<Navigation> {
            return this._httpClient.get<Navigation>('api/common/navigation').pipe(
              tap((navigation) => {
                // Retrieve and parse user type from localStorage
                const userType = JSON.parse(localStorage.getItem("user")).Type;
          
                // Modify navigation items based on user type
                navigation.default.forEach(item => {
                  if ((userType === 'reports') && (item.title !== 'Analytics Hub')) {
                    item.children.forEach(e => e.disabled = true);
                  } else if ((userType === 'top_management') && (item.title !== 'Configuration')) {
                    item.children.forEach(e => e.disabled = true);
                  } else if ((userType === 'Sustainability') && (item.title !== 'Sustainability Strategies')) {
                    item.children.forEach(e => e.disabled = true);
                  } else if ((userType === 'admin')) {
                    item.children.forEach(e => e.disabled = false);
                  }
                });
          
                // Function to determine if all children are enabled
                const allChildrenEnabled = (item) => item.children.every(child => !child.disabled);
          
                // Separate items into those with all enabled children and the rest
                const itemsWithAllEnabledChildren = navigation.default.filter(item => allChildrenEnabled(item));
                const otherItems = navigation.default.filter(item => !allChildrenEnabled(item));
          
                // Combine items with all enabled children first
                navigation.default = [...itemsWithAllEnabledChildren, ...otherItems];
                // Emit the modified navigation
                this._navigation.next(navigation);
              }),
            );
          }
          
          
          
}
