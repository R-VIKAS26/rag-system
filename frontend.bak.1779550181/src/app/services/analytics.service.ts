import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
  private apiUrl = `${environment.apiUrl}/analytics`;

  constructor(private http: HttpClient) { }

  getUserStats(): Observable<any> {
    return this.http.get(`${this.apiUrl}/user-stats`);
  }

  getSystemMetrics(metric: string, periodHours: number = 24): Observable<any> {
    return this.http.get(`${this.apiUrl}/system-metrics?metric=${metric}&period_hours=${periodHours}`);
  }

  getRagPerformance(): Observable<any> {
    return this.http.get(`${this.apiUrl}/rag-performance`);
  }

  getDocumentAnalytics(documentId?: string): Observable<any> {
    const url = documentId 
      ? `${this.apiUrl}/document-analytics?document_id=${documentId}`
      : `${this.apiUrl}/document-analytics`;
    return this.http.get(url);
  }

  generateUsageReport(startDate?: Date, endDate?: Date): Observable<any> {
    let url = `${this.apiUrl}/usage-report`;
    const params: string[] = [];
    
    if (startDate) params.push(`start_date=${startDate.toISOString()}`);
    if (endDate) params.push(`end_date=${endDate.toISOString()}`);
    
    if (params.length > 0) url += '?' + params.join('&');
    
    return this.http.get(url);
  }
}
