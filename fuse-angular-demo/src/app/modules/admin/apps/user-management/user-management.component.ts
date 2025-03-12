import { ChangeDetectionStrategy, ChangeDetectorRef, Component, OnDestroy, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';
import { MatDrawer } from '@angular/material/sidenav';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { FuseMediaWatcherService } from '@fuse/services/media-watcher';

@Component({
    selector       : 'app-user-management',
    templateUrl    : './user-management.component.html'
})
export class UserManagementComponent implements OnInit, OnDestroy
{
    @ViewChild('drawer') drawer: MatDrawer;
    drawerMode: 'over' | 'side' = 'side';
    drawerOpened: boolean = true;
    panels: any[] = [];
    selectedPanel: string = 'usersPermissions';
    private _unsubscribeAll: Subject<any> = new Subject<any>();
    usertype :string;
    /**
     * Constructor
     */
    constructor(
        private _changeDetectorRef: ChangeDetectorRef,
        private _fuseMediaWatcherService: FuseMediaWatcherService
    )
    {
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Lifecycle hooks
    // -----------------------------------------------------------------------------------------------------

    /**
     * On init
     */
   /*  ngOnInit(): void
    {


       // this.usertype = localStorage.getItem("type")
       this.usertype = JSON.parse(localStorage.getItem("user")).Type
        // Setup available panels
        this.panels = [
            {
                id         : 'usersPermissions',
                icon       : 'heroicons_outline:lock-closed',
                title      : 'Manage Users Permissions',
                description: 'Manage COFICAB users by changing their roles/permissions'
            },
            {
                id         : 'users',
                icon       : 'heroicons_outline:user',
                title      : 'Manage Users',
                description: 'Add, delete, and update users'
            },
            {
                id         : 'projects',
                icon       : 'heroicons_outline:collection',
                title      : 'Manage Projects',
                description: 'Add, delete, and update project details'
            },
            {
                id         : 'plants',
                icon       : 'heroicons_outline:location-marker',
                title      : 'Manage Plants',
                description: 'Add, delete, and update COFICAB Plant'
            }
            
        ];

    } */
        ngOnInit(): void {
            // Retrieve the user object from localStorage
            const user = JSON.parse(localStorage.getItem("user"));
            this.usertype = user.Type;
            const userEmail = JSON.parse(localStorage.getItem("ID_User_Login")); // Assuming the user object contains an 'Email' field
        
            // Define panels
            const allPanels = [
                {
                    id         : 'usersPermissions',
                    icon       : 'heroicons_outline:lock-closed',
                    title      : 'Manage Users Permissions',
                    description: 'Manage COFICAB users by changing their roles/permissions'
                },
                {
                    id         : 'users',
                    icon       : 'heroicons_outline:user',
                    title      : 'Manage Users',
                    description: 'Add, delete, and update users'
                },
                {
                    id         : 'projects',
                    icon       : 'heroicons_outline:collection',
                    title      : 'Manage Projects',
                    description: 'Add, delete, and update project details'
                },
                {
                    id         : 'plants',
                    icon       : 'heroicons_outline:location-marker',
                    title      : 'Manage Plants',
                    description: 'Add, delete, and update COFICAB Plant'
                }
            ];
        
            // Example: Display panels based on email
            if (user.Type === 'admin') {
                // Admin gets access to all panels
                this.panels = allPanels;
            } /* else if (userEmail === 'manager@coficab.com') {
                // Manager gets access to specific panels
                this.panels = allPanels.filter(panel => 
                    panel.id === 'projects' || panel.id === 'plants'
                );
            } */ else if (user.ID_User_Login === 'mohamedkarim.bdir@coficab.com') {
                // General COFICAB users get access to limited panels
                this.panels = allPanels.filter(panel => panel.id === 'users');
            } else {
                // Default: No access or limited panels
                this.panels = [];
            }
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
      * Navigate to the panel
      *
      * @param panel
      */
     goToPanel(panel: string): void
     {

         this.selectedPanel = panel;
 
         // Close the drawer on 'over' mode
         if ( this.drawerMode === 'over' )
         {
             this.drawer.close();
         }
     }
 
     /**
      * Get the details of the panel
      *
      * @param id
      */
     getPanelInfo(id: string): any
     {
         return this.panels.find(panel => panel.id === id);
     }
 
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

}
