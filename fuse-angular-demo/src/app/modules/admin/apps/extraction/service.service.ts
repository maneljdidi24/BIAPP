import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { from, Observable } from 'rxjs';
import { environment } from '../../../../../environments/environment';


@Injectable({
  providedIn: 'root'
})
export class ServiceService {

  private baseUrl = environment.API_BASE_URL;

  constructor(private http: HttpClient) {}
 
  public getALLDataFromDB(plant:any): Observable<any[]> {
   return this.http.get<any>(`${this.baseUrl}purchasing/get/${plant}`);
  }
  public getDB(plant:any,startdate:any,endDate:any,project:any): Observable<any[]> {
    return this.http.get<any>(`${this.baseUrl}purchasing/get/${plant}/${startdate}/${endDate}/${project}`);
   }


   CheckAzurServer(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}sales/CheckAzurServer`);
   }

   getdistinctplants(plant:any): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}sales/plants/${plant}`);
   }
  // return this.http.get<any[]>(`${this.baseUrl}/get/${plant}`);

  public verifytoken(token: any) {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `${token}`
    })
    return this.http.get<any>(`${this.baseUrl}verifytoken` , {headers : headers});
  }


  public create(plant:any,dates:any): Observable<Object> {
  return this.http.get<any[]>(`${this.baseUrl}test/${plant}`,dates)}

  public login(userData: any){
    return this.http.post(`${this.baseUrl}login`, userData);
  }

  public registerUser(userData: any): Observable<any[]> {
    return this.http.post<any[]>(`${this.baseUrl}register`, userData);
  }

  updateInvestment(Po: any, Poline: any, Receipt_Number: any, Receipt_Number_Lines: any, invest: any): Observable<any> {
    const url = `${this.baseUrl}purchasing/updateInvest/${Po}/${Poline}/${Receipt_Number}/${Receipt_Number_Lines}/${invest}`;
    return this.http.put<any>(url, {});
  }
}
