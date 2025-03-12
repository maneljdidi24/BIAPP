import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../../../environments/environment.prod';


@Injectable({
  providedIn: 'root',
})
export class DataService {
  private baseUrl = environment.API_BASE_URL;

  constructor(private http: HttpClient) {}
  
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}` // Retrieve token from local storage
    })
  };

  // User Routes
  getUsers(): Observable<any> {
    return this.http.get(`${this.baseUrl}/users/getuser`);
  }

  addUser(user: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/users/adduser`, user);
  }

  deleteUser(userId: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/users/deleteuser/${userId}`);
  }

  editUser(userId: string, user: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/users/edituser/${userId}`, user);
  }

  // Project Routes
  getProjects(): Observable<any> {
    return this.http.get(`${this.baseUrl}/projects/getproject`);
  }

  addProject(project: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/projects/addproject`, project);
  }

  deleteProject(projectId: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/projects/deleteproject/${projectId}`);
  }

  editProject(projectId: string, project: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/projects/editproject/${projectId}`, project);
  }

  // Plant Routes
  getPlants(): Observable<any> {
    return this.http.get(`${this.baseUrl}/plants/getplant`);
  }

  addPlant(plant: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/plants/addplant`, plant);
  }

  deletePlant(plantId: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/plants/deleteplant/${plantId}`);
  }

  editPlant(plantId: string, plant: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/plants/editplant/${plantId}`, plant);
  }


  Extract(plant: any, start: any, end: any): Observable<any> {
    const url = `${this.baseUrl}/purchasing/extract/${plant}/${start}/${end}`;
    return this.http.get<any>(url);
  }
}
