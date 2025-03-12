import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, CanActivateChild, CanLoad, Route, Router, RouterStateSnapshot, UrlSegment, UrlTree } from '@angular/router';
import { Observable, of } from 'rxjs';
import { AuthService } from 'app/core/auth/auth.service';
import { map, switchMap } from 'rxjs/operators';

@Injectable({
    providedIn: 'root'
})
export class AuthGuard implements CanActivate, CanActivateChild, CanLoad
{
    /**
     * Constructor
     */
    constructor(
        private _authService: AuthService,
        private _router: Router
    )
    {
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Public methods
    // -----------------------------------------------------------------------------------------------------

    /**
     * Can activate
     *
     * @param route
     * @param state
     */
/*     canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean
    {
        const redirectUrl = state.url === '/sign-out' ? '/' : state.url;
        return this._check(redirectUrl);
    } */
/* 
        canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean {
            const redirectUrl = state.url === '/sign-out' ? '/' : state.url;
            


            return this._check(redirectUrl).pipe(
                map((isAuthenticated: boolean) => {
                    if (isAuthenticated) {
                        const user = JSON.parse(localStorage.getItem("user"));
                    alert(user.Type)
                    if (user.Type=='admin'){
                        return true;
                    }
                     
                     // Grant access if the user is an admin
                    }
        
                    this._router.navigate(['/not-authorized']); // You can change this path as needed
                    return false;
                }
            )
            );
        }
         */

        canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> | boolean {
            const redirectUrl = state.url === '/sign-out' ? '/' : state.url;
      
            return this._check(redirectUrl).pipe(
                map((isAuthenticated: boolean) => {
                    if (isAuthenticated) {
                        const user = JSON.parse(localStorage.getItem("user"));
                        console.log(user)

                        // Allow logout action
                if (state.url === '/sign-out') {
                    return true; // Always allow logout
                }

                        // Admin can access everything
                        if (user.Type === 'admin') {
                            return true;
                        }
      
                        // Reports users can only access report-related routes
                        if (user.Type === 'reports' && state.url.startsWith('/dashboards')) {
                            return true;
                        }
      
                        // Sustainability users can only access sustainability routes
                        if (user.Type === 'Sustainability' && state.url.startsWith('/sustainability') ) {
                            return true;
                        }

                        if (user.Type === 'RH' && state.url.startsWith('/RH') ) {
                            return true;
                        }
      
                        // If none of the conditions match, redirect to a not-authorized page
                        this._router.navigate(['/']);
                        return false;
                    }
      
                    // Redirect to login if not authenticated
                    this._router.navigate(['/sign-in']);
                    return false;
                })
            );
        }


    /**
     * Can activate child
     *
     * @param childRoute
     * @param state
     */
    canActivateChild(childRoute: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree
    {
        const redirectUrl = state.url === '/sign-out' ? '/' : state.url;
        return this._check(redirectUrl);
    }

    /**
     * Can load
     *
     * @param route
     * @param segments
     */
    canLoad(route: Route, segments: UrlSegment[]): Observable<boolean> | Promise<boolean> | boolean
    {
        return this._check('/');
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Private methods
    // -----------------------------------------------------------------------------------------------------

    /**
     * Check the authenticated status
     *
     * @param redirectURL
     * @private
     */
    private _check(redirectURL: string): Observable<boolean>
    {
        
        // Check the authentication status
        return this._authService.check()
                   .pipe(
                       switchMap((authenticated) => {
                           // If the user is not authenticated...
                           if ( !authenticated )
                           {
                               // Redirect to the sign-in page
                               this._router.navigate(['sign-in']);
                               // Prevent the access
                               return of(false);
                           }
                           // Allow the access
                           return of(true);
                       })
                   );
    }
}