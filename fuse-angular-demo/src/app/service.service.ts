import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, ReplaySubject } from 'rxjs';
import { environment } from 'environments/environment';
import { map, tap } from 'rxjs/operators';
import { User } from 'app/core/user/user.types';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  private baseUrl = environment.API_BASE_URL;
  

  constructor(private http: HttpClient) {}

  // User Routes
  getUsers(): Observable<any[]> {
    
    return this.http.get<any[]>(`${this.baseUrl}/users/getuser`, { headers: this.headers });
  }


  private token = localStorage.getItem('accessToken');  // Retrieve token from localStorage
  private headers = new HttpHeaders().set('Authorization', `Bearer ${this.token}`);


  addUser(user: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/users/adduser`, user, { headers: this.headers });
  }

  deleteUser(userId: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/users/deleteuser/${userId}`, { headers: this.headers });
  }

  editUser(userId: string, user: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/users/edituser/${userId}`, user, { headers: this.headers });
  }


  getemployee(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/employers/`, { headers: this.headers });
  }
  getDepartments(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/department/`, { headers: this.headers });
  }
  getJobs(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/jobs/`, { headers: this.headers });
  }
  getCostCenter(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/costCenters/`, { headers: this.headers });
  }
    /**
   * Create a single employer
   * @param employerData - The employer data object
   * @returns Observable of the created employer
   */
    createSingleEmployer(employerData: any): Observable<any> {
      const userId = JSON.parse(localStorage.getItem('user')).ID_User_Login; 
      return this.http.post<any>(`${this.baseUrl}employers/single/${userId}`,employerData, { headers: this.headers } );
    }

      /**
   * Create or update multiple employers
   * @param employersData - Array of employer data objects
   * @returns Observable of the processing result
   */
      createOrUpdateBulkEmployers(employersData: any[]): Observable<any> {
        const headers = new HttpHeaders()
          .set('Authorization', `Bearer ${this.token}`)
          .set('Content-Type', 'application/json');
          const userId = JSON.parse(localStorage.getItem('user')).ID_User_Login; 
        return this.http.post<any>(`${this.baseUrl}employers/bulk/${userId}`,employersData ,  { headers });
      }


    
      
  // Project Routes
  getProjects(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/projects/getproject`, { headers: this.headers }).pipe(
      map(res => res), // Adjust this mapping based on your API response structure
    );
  }

  addProject(project: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/projects/addproject`, project, { headers: this.headers });
  }

  deleteProject(projectId: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/projects/deleteproject/${projectId}`, { headers: this.headers });
  }

  editProject(projectId: string, project: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/projects/editproject/${projectId}`, project, { headers: this.headers });
  }

  // Plant Routes
  getPlant(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/plants/getplant`, { headers: this.headers });
  }

  getPlants(): Observable<any> {
    return this.http.get<any[]>(`${this.baseUrl}/plants/getplants`, { headers: this.headers });
  }



  GetPlantsforuser(): Observable<any> {
    const body = JSON.parse(localStorage.getItem('user')).ID_User_Login;  // Parse the JSON string into an object
    return this.http.post(`${this.baseUrl}/plants/GetPlantsforuser`, { data: body } , {headers: this.headers})
  }

  GetRegionforuser(): Observable<any> {
    const body = JSON.parse(localStorage.getItem('user')).ID_User_Login;  // Parse the JSON string into an object
    return this.http.post(`${this.baseUrl}/plants/GetRegionforuser`, { data: body } , {headers: this.headers})
  }

  getregion(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/plants/getRegions`, { headers: this.headers });
  }

  addPlant(plant: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/plants/addplant`, plant, { headers: this.headers });
  }

  deletePlant(plantId: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/plants/deleteplant/${plantId}`, { headers: this.headers });
  }

  editPlant(plantId: string, plant: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/plants/editplant/${plantId}`, plant, { headers: this.headers });
  }



  getUserAccess(): Observable<any[]> {
    const url = `${this.baseUrl}/access/getuseraccess`;
    return this.http.get<any[]>(url, { headers: this.headers });
  }

  getUserById(id:any): Observable<any[]> {   
    const url = `${this.baseUrl}/users/getUserById/${id}`;
    return this.http.get<any[]>(url, { headers: this.headers });
  }


  addUserAccess(userAccessData: any): Observable<any> {
    const url = `${this.baseUrl}/access/adduseraccess`;
    return this.http.post(url, userAccessData, { headers: this.headers });
  }

  deleteUserAccess(userId: string): Observable<any> {
    const url = `${this.baseUrl}/access/deleteuseraccess/${userId}`;
    return this.http.delete(url, { headers: this.headers });
  }

  editUserAccess(userId: string, user: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/access/edituseraccess/${userId}`, user, { headers: this.headers });
  }

  getDistinctUsers(): Observable<any[]> {
    const url = `${this.baseUrl}/access/getdistinctusers`;
    return this.http.get<any[]>(url, { headers: this.headers });
  }

  login(credentials): Observable<any> {
    return this.http.post(`${this.baseUrl}login`,credentials, { headers: this.headers });
  }


  ///////////sustainability 

    public gettopics(): Observable<any[]> {
     return this.http.get<any>(`${this.baseUrl}sustainablity/topic/gettopics`, { headers: this.headers });
    }

    public getelements(): Observable<any[]> {
     return this.http.get<any>(`${this.baseUrl}sustainablity/element/getelements`, { headers: this.headers });
    }

    public getdistinctyears(): Observable<any[]> {
     return this.http.get<any>(`${this.baseUrl}sustainablity/performance/getdistinctyears`, { headers: this.headers });
    }
 
    public getditinctdate(obj:any[]): Observable<any> {
      return this.http.post<any>(`${this.baseUrl}sustainablity/performance/getDdates`,obj, { headers: this.headers });
    }

    public fromPlantGetDate(plant:any): Observable<any[]> {
      return this.http.post<any>(`${this.baseUrl}sustainablity/performance/fromPlantGetDate/${plant}`, { headers: this.headers });
    }
    public getPerformancese(obj:any[]): Observable<any> {
     return this.http.post<any>(`${this.baseUrl}sustainablity/performance/getperformances`,obj, { headers: this.headers });
    } 

    public modifyperformance(obj:any[]): Observable<any> {
      return this.http.put(`${this.baseUrl}sustainablity/performance/modifyperformance`,obj, { headers: this.headers });
    } 

    public deleteInsertPerformance(obj:any[]): Observable<any> {
      return this.http.put(`${this.baseUrl}sustainablity/performance/deleteInsertPerformance`,obj, { headers: this.headers });
    } 

    public display_performance_for_update(obj:any[]): Observable<any> {
      return this.http.post<any>(`${this.baseUrl}sustainablity/performance/display_performance_for_update`,obj, { headers: this.headers });
     } 

    

    /////////////////sales

    getcountsalesdata(plant:any,startdate:any,endDate:any,regions:any): Observable<any> {
      return this.http.post<any>(`${this.baseUrl}sales/getcountsalesdata/${plant}/${startdate}/${endDate}`,regions, { headers: this.headers });
     }

     SelectSalesDisplay500(plant:any,startdate:any,endDate:any,offset:any,regions:any): Observable<any> {

      return this.http.post<any[]>(`${this.baseUrl}sales/SelectSalesDisplay500/${plant}/${startdate}/${endDate}/${offset}`,regions, { headers: this.headers } );
     }

/*      getSalesAll(plant:any,startdate:any,endDate:any,regions:any): Observable<any> {
      return this.http.post<any[]>(`${this.baseUrl}sales/getAll/${plant}/${startdate}/${endDate}`,regions, { headers: this.headers });
     } */

      SelectAllSalesForCSV(plant: any, startdate: any, endDate: any, regions: any) {
      return this.http.post(`${this.baseUrl}sales/SelectAllSalesForCSV/${plant}/${startdate}/${endDate}`, regions, {
        headers: this.headers,
        responseType: 'blob'
      });
    }
    
    getPlantFromRegion(plant:any): Observable<any[]> {
      return this.http.get<any[]>(`${this.baseUrl}sales/getPlantFromRegion/${plant}`);
     }

     public extractsales(obj:any): Observable<any[]> {return this.http.post<any>(`${this.baseUrl}/etlsales/extract`,obj);}
  

}



