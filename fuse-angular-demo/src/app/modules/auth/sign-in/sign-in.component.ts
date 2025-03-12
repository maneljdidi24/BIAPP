import { Component, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';
import { FormBuilder, FormGroup, NgForm, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { fuseAnimations } from '@fuse/animations';
import { FuseAlertType } from '@fuse/components/alert';
import { AuthService } from 'app/core/auth/auth.service';
import { Subject, timer } from 'rxjs';
import { finalize, takeUntil, takeWhile, tap } from 'rxjs/operators';

@Component({
    selector: 'auth-sign-in',
    templateUrl: './sign-in.component.html',
    encapsulation: ViewEncapsulation.None,
    animations: fuseAnimations
})
export class AuthSignInComponent implements OnInit {
    @ViewChild('signInNgForm') signInNgForm: NgForm;
    countdown: number = 5;
    countdownMapping: any = {
        '=1': '# second',
        'other': '# seconds'
    };
    showCountdown: any
    alert: { type: FuseAlertType; message: string } = {
        type: 'success',
        message: ''
    };
    signInForm: FormGroup;
    showAlert: boolean = false;

    /**
     * Constructor
     */
    constructor(
        private _activatedRoute: ActivatedRoute,
        private _authService: AuthService,
        private _formBuilder: FormBuilder,
        private _router: Router
    ) {
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Lifecycle hooks
    // -----------------------------------------------------------------------------------------------------

    /**
     * On init
     */
    ngOnInit(): void {
        if (localStorage.getItem('Global') == "True") {
            this.showCountdown = "True"
        }
        // Redirect after the countdown
        timer(1000, 1000)
            .pipe(
                finalize(() => {
                    this.showCountdown = "True"
                    localStorage.setItem('Global', "True")
                }),
                takeWhile(() => this.countdown > 0),
                tap(() => this.countdown--)
            )
            .subscribe();

        // Create the form
        this.signInForm = this._formBuilder.group({
            email: ['', [Validators.required, Validators.email]],
            password: ['', Validators.required],
            rememberMe: [true]
        });
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Public methods
    // -----------------------------------------------------------------------------------------------------

    /**
     * Sign in
     */
    redirectURL: any
    signIn(): void {

        // Return if the form is invalid
        if (this.signInForm.invalid) {
            return;
        }

        // Disable the form
        this.signInForm.disable();

        // Hide the alert
        this.showAlert = false;

        // Sign in
        this._authService.signIn(this.signInForm.value)
            .subscribe(
                () => {

                    // Get user data from localStorage
                    const user = JSON.parse(localStorage.getItem("user"));

                    // Check if the user has reset=0 and redirect to /reset-password
                   /*  if (user && user.resetpassword === 0) {
                        this.redirectURL = this._activatedRoute.snapshot.queryParamMap.get('redirectURL') || '/reset-password';
                    }
                    else{ */
                    // Set the redirect URL
                    // The '/signed-in-redirect' is a dummy URL to catch the request and redirect the user
                    // to the correct page after a successful sign-in. This way, that URL can be set via
                    // the routing file, and we don't have to touch here.
                    this.redirectURL = this._activatedRoute.snapshot.queryParamMap.get('redirectURL') || '/signed-in-redirect';

                    // Update the redirect URL if the user's type is 'Sustainability'
                    if (user && user.Type === 'Sustainability') {
                        this.redirectURL = this._activatedRoute.snapshot.queryParamMap.get('redirectURL') || '/signed-in-redirectSus';
                    }
                     //}
                    // Navigate to the redirect URL
                    this._router.navigateByUrl(this.redirectURL);


                },
                (response) => {

                    // Re-enable the form
                    this.signInForm.enable();

                    // Reset the form
                    this.signInNgForm.resetForm();

                    // Check if response is an object
                    let message = '';
                    if (typeof response === 'object' && response.error && response.error.msg) {
                        message = response.error.msg;
                    } else {
                        message = response;
                    }

                    // Set the alert
                    this.alert = {
                        type: 'error',
                        message: message
                    };

                    // Show the alert
                    this.showAlert = true;
                }

            );
    }
}
