import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

export interface RAGQuery {
  query: string;
  document_ids?: string[];
  top_k?: number;
}

export interface RAGResponse {
  query: string;
  answer: string;
  results: any[];
  processing_time: number;
  model_used: string;
}

@Injectable({
  providedIn: 'root'
})
export class RagService {
  private apiUrl = `${environment.apiUrl}/rag`;

  constructor(private http: HttpClient) { }

  queryRAG(request: RAGQuery): Observable<RAGResponse> {
    return this.http.post<RAGResponse>(`${this.apiUrl}/query`, request);
  }

  chatRAG(request: RAGQuery): Observable<RAGResponse> {
    return this.http.post<RAGResponse>(`${this.apiUrl}/chat`, request);
  }

  analyzeDocument(documentId: string, query: string): Observable<RAGResponse> {
    return this.http.post<RAGResponse>(`${this.apiUrl}/analyze-document?document_id=${documentId}&query=${query}`, {});
  }

  searchDocuments(query: string, topK?: number): Observable<any[]> {
    const params = new URLSearchParams();
    params.set('query', query);
    if (topK) params.set('top_k', topK.toString());
    return this.http.get<any[]>(`${this.apiUrl}/search?${params.toString()}`);
  }
}
