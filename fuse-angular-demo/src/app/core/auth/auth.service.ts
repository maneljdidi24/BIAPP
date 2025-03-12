import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, ReplaySubject, of, throwError } from 'rxjs';
import { catchError, switchMap } from 'rxjs/operators';
import { AuthUtils } from 'app/core/auth/auth.utils';
import { UserService } from 'app/core/user/user.service';
// Import environment object
import { environment } from '../../../environments/environment';
import CryptoJS from 'crypto-js';
import { CookieService } from 'ngx-cookie-service';
import { User } from '../user/user.types';
import { DataService } from 'app/service.service';


@Injectable()
export class AuthService
{
    private _authenticated: boolean = false;
    apiUrl = environment.API_BASE_URL;
    conversionOutput: string;
    private _user: ReplaySubject<User> = new ReplaySubject<User>(1);
    /**
     * Constructor
     */
    constructor(
        private _httpClient: HttpClient,private service: DataService,
        private _userService: UserService,private cookieService: CookieService
    )
    {
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Accessors
    // -----------------------------------------------------------------------------------------------------

    /**
     * Setter & getter for access token
     */
    set accessToken(token: string)
    {
        localStorage.setItem('accessToken', token);
    }

    get accessToken(): string
    {
        return localStorage.getItem('accessToken') ?? '';
    }

    set type(token: string)
    {
        localStorage.setItem('type', token);
    }

    get type(): string
    {
        return localStorage.getItem('type') ?? '';
    }
    set position(token: string)
    {
        localStorage.setItem('position', token);
    }

    get position(): string
    {
        return localStorage.getItem('position') ?? '';
    }
    // -----------------------------------------------------------------------------------------------------
    // @ Public methods
    // -----------------------------------------------------------------------------------------------------
// Use the API_BASE_URL

    /**
     * Forgot password
     *
     * @param email
     */
    forgotPassword(email: string): Observable<any>
    {
        return this._httpClient.post('api/auth/forgot-password', email);
    }

    /**
     * Reset password
     *
     * @param password
     */
    resetPassword(password: string): Observable<any>
    {
        return this._httpClient.post('api/auth/reset-password', password);
    }

    /**
     * Sign in
     *
     * @param credentials
     */
    signIn(credentials: { email: string; password: string }): Observable<any>
    {
        // Throw error, if the user is already logged in
        if ( this._authenticated )
        {
            return throwError('User is already logged in.');
        }

        return this.service.login(credentials).pipe(
            switchMap((response: any) => {
                           if (response.code==200) {
                // Store the access token in the local storage
                
                this.accessToken = response.access_token;
                //console.log(response.user)

                localStorage.setItem('user', JSON.stringify(response.user) )
/*                 this.conversionOutput = CryptoJS.AES.decrypt("msg", "password").toString(CryptoJS.enc.Utf8);

                this.textToConvert = this.cookie.get(‘key’); */

                // Set the authenticated flag to true
                this._authenticated = true;

                // Store the user on the user service
                /* this._user.next(response.user)
                this._user.asObservable().subscribe(user => {
                    alert(user.ID_User_Login);
                }); */
                this._userService.user = response.user;
                /* this._userService.get()._subscribe((user:any) =>{
                    alert(user.ID_User_Login)
                }) */
                


                //window.location.reload();

                // Return a new observable with the response
                return of(response);}
                else if (response.code==300){
                    alert()
                }
             else {
                // If response code is not 200, throw an error
                return throwError(response.msg);
            }
            }
        )
        );
    }

    /**
     * Sign in using the access token
     */
    signInUsingToken(): Observable<any>
    {
       // alert('im here')
        // Renew token
       /*  return this._httpClient.post('api/auth/refresh-access-token', {
            accessToken: this.accessToken
        }).pipe(
            catchError(() =>

                // Return false
                of(false)
            ),
            switchMap((response: any) => {

                // Store the access token in the local storage
                this.accessToken = response.accessToken;

                // Set the authenticated flag to true
                this._authenticated = true;

                // Store the user on the user service
                this._userService.user = response.user;

                // Return true
                return of(true);
            })
        ); */
        this._authenticated = true;
        return of(true);
    }

    /**
     * Sign out
     */
    signOut(): Observable<any>
    {
        // Remove the access token from the local storage
        localStorage.removeItem('accessToken');
        localStorage.removeItem('position');
        localStorage.removeItem('type');
        localStorage.removeItem('user');
        // Set the authenticated flag to false
        this._authenticated = false;

        // Return the observable
        return of(true);
    }

    /**
     * Sign up
     *
     * @param user
     */
    signUp(user: { name: string; email: string; password: string; company: string }): Observable<any>
    {
        return this._httpClient.post('api/auth/sign-up', user);
    }

    /**
     * Unlock session
     *
     * @param credentials
     */
    unlockSession(credentials: { email: string; password: string }): Observable<any>
    {
        return this._httpClient.post('api/auth/unlock-session', credentials);
    }

    /**
     * Check the authentication status
     */
    check(): Observable<boolean>
    {
        // Check if the user is logged in
        if ( this._authenticated )
        {
            return of(true);
        }

        // Check the access token availability
         if ( !this.accessToken )
        {
            return of(false);
        }

        // Check the access token expire date
        if ( AuthUtils.isTokenExpired(this.accessToken) )
        {
            return of(false);
        } 

        // If the access token exists and it didn't expire, sign in using it
        return this.signInUsingToken();
    }
}