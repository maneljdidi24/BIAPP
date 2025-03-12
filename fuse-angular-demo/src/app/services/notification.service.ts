import { Injectable } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

  constructor(private _formBuilder: FormBuilder) { }

  error(msg: any): FormGroup {
    return this._formBuilder.group({
      title: 'Error!',
      message: msg,
      icon: this._formBuilder.group({
        show: true,
        name: 'heroicons_outline:exclamation',
        color: 'error' // Red color for error
      }),
      actions: this._formBuilder.group({
        confirm: this._formBuilder.group({
          show: true,
          label: 'OK',
          color: 'primary'
        }),
        cancel: this._formBuilder.group({
          show: false, // Hide the 'Close' button for error message
          label: 'Close',
          color: 'warn'
        })
      }),
      dismissible: true
    });
  }

  success(msg: any): FormGroup {
    return this._formBuilder.group({
      title: 'Success!',
      message: msg,
      icon: this._formBuilder.group({
        show: true,
        name: 'heroicons_outline:check',
        color: 'success' // Green color for success
      }),
      actions: this._formBuilder.group({
        confirm: this._formBuilder.group({
          show: false, // Hide the 'Remove' button for success message
          label: 'Remove',
          color: 'warn'
        }),
        cancel: this._formBuilder.group({
          show: true,
          label: 'Close',
          color: 'primary' // Use a primary color for the 'Close' button
        })
      }),
      dismissible: true
    });
  }

  confirmUpdate(): FormGroup {
    return this._formBuilder.group({
      title: 'Confirm Update',
      message: 'Are you sure you want to update the data?',
      icon: this._formBuilder.group({
        show: true,
        name: 'heroicons_outline:exclamation',
        color: 'warning' // Use a warning color for the icon
      }),
      actions: this._formBuilder.group({
        confirm: this._formBuilder.group({
          show: true,
          label: 'Yes, Update',
          color: 'primary' // Use a primary color for the confirmation button
        }),
        cancel: this._formBuilder.group({
          show: true,
          label: 'Cancel',
          color: 'warn' // Use a warn color for the cancel button
        })
      }),
      dismissible: false // Set to false to force user action (confirm or cancel)
    });
  }
}
