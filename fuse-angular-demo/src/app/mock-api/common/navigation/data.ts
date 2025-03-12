/* eslint-disable */
import { FuseNavigationItem } from '@fuse/components/navigation';
import { user } from '../user/data';



export const defaultNavigation: FuseNavigationItem[] = [
    {
        id: "Sustainability",
        title: "Sustainability Strategies",
        subtitle: "Environmental and Social Impact Projects",
        type: "group",
        children: [
            /* {
                id: "Sustainability.rh",
                title: "Human Resources Projects",
                type: "basic",
                icon: "heroicons_solid:briefcase",  // Professional icon representing human resources projects
                link: "/dashboards/rh"
            }, */
            {
                id: "Sustainability.performance",
                //title: "Performance Metrics",
                title: "Performance Data",
                type: "basic",
                icon: "heroicons_solid:chart-bar",  // Professional icon representing performance metrics
                link: "/sustainability/main",
                
            },
           /*  {
                id: "Sustainability.target",
                //title: "Performance Metrics",
                title: "Performance Targets",
                type: "basic",
                icon: "heroicons_solid:chart-bar",  // Professional icon representing performance metrics
                link: "/sustainability/target"
            }, */
            {
                id: "Sustainability.governance",
                //title: "Governance Projects",
                title: "Governance Data",
                type: "basic",
                icon: "heroicons_solid:users",  // Professional icon representing social initiatives
                link: "/sustainability/m"
            }
        ]
    },    
    {
        id: "human-resources",
        title: "Human Resources",
        subtitle: "Manage your HR tasks",
        type: "group",
        children: [
            {
                id: "manage-employee",
                title: "Manage Employees",
                type: 'collapsable',
                icon: "heroicons_solid:briefcase",  // Icon representing employee management
                link: "/HR/employee/display",
                children: [
                    {
                        id: 'display-employee',
                        title: 'Display Employees',
                        type: 'basic',
                        link: '/HR/employee/display',
                        exactMatch: true
                    },
                    {
                        id: 'add-employee',
                        title: 'Add Employee',
                        type: 'basic',
                        link: '/HR/employee/add',
                        exactMatch: true
                    },
                    {
                        id: 'edit-employee',
                        title: 'Edit Employee',
                        type: 'basic',
                        link: '/HR/employee/edit',
                        exactMatch: true
                    }
                ]
            }
            ,
            
            {
                id: "manage-training",
                title: "Manage Training",
                type: "basic",
                icon: "heroicons_solid:academic-cap",  // Icon representing training
                link: "/human-resources/manage-training"
            }
        ]
    }
,    
    {
        id: "Analytics Center",
        title: "Analytics Hub",
        subtitle: "COFICAB Data Insights",
        type: "group",
        icon: "heroicons_solid:chart-bar",
        children: [
            {
                id: "Analytics Center.project",
                title: "Comprehensive Reports",
                type: "basic",
                icon: "heroicons_solid:clipboard-list",
                link: "/dashboards/project"
            },
            {
                id: "Analytics Center.analytics",
                title: "Power BI Dashboards",
                type: "basic",
                icon: "heroicons_solid:chart-pie",
                link: "/dashboards/analytics/BI"
            }/* ,
            {
                id: "Analytics Center.dataprediction",
                title: "Market Outlook",
                type: "basic",
                icon: "heroicons_solid:trending-up",
                link: "/dashboards/analytics/d"
            } */
        ]
    }
    ,
    
    {
        id      : 'pages',
        title   : 'Configuration',
        subtitle: '',
        type    : 'group',
        icon    : 'heroicons_solid:cog',
        children: [
            {
                id      : 'apps.ecommerce.inventory',
                title   : 'Purchasing Data Extraction',
                type    : 'basic',
                icon    : 'heroicons_solid:shopping-bag',
                link    : '/apps/tasks/purchasing',
            },
            {
                id      : 'apps.ecommerce.inventory',
                title   : 'Sales Data Extraction',
                type    : 'basic',
                icon    : 'heroicons_solid:chart-square-bar',
                link    : '/apps/tasks/sales',
            },
            {
                id       : 'apps.contacts',
                title    : 'Account Management',
                type     : 'basic',
                icon     : 'heroicons_solid:user-group',
                link     : '/pages/settings',
            }
        ]
    }
    
    
];


export const horizontalNavigation: FuseNavigationItem[] = [
    {
        id   : 'Detailed Reports',
        title: 'Detailed Reports',
        type : 'group',
        icon : 'heroicons_outline:clipboard-check',
        link : '/dashboards/analytics'
    } ,
    {
        id      : 'pages',
        title   : 'Pages',
        type : 'group',
        icon    : 'heroicons_outline:document-duplicate'} 
];
