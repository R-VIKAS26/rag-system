import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AgentService {
  private apiUrl = `${environment.apiUrl}/agents`;

  constructor(private http: HttpClient) { }

  createTask(taskData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/create-task`, taskData);
  }

  getTaskStatus(taskId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/task/${taskId}`);
  }

  getTaskResult(taskId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/task/${taskId}/result`);
  }

  cancelTask(taskId: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/task/${taskId}/cancel`, {});
  }

  getAvailableTools(): Observable<any> {
    return this.http.get(`${this.apiUrl}/available-tools`);
  }
}
