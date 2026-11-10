import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);

  list<T>(endpoint: string): Observable<T[]> {
    return this.http.get<T[]>(`${API_BASE_URL}/${endpoint}/`);
  }

  get<T>(endpoint: string, id: string): Observable<T> {
    return this.http.get<T>(`${API_BASE_URL}/${endpoint}/${encodeURIComponent(id)}`);
  }

  create<T>(endpoint: string, payload: Record<string, unknown>): Observable<T> {
    return this.http.post<T>(`${API_BASE_URL}/${endpoint}/`, payload);
  }

  update<T>(endpoint: string, id: string, payload: Record<string, unknown>): Observable<T> {
    return this.http.put<T>(`${API_BASE_URL}/${endpoint}/${encodeURIComponent(id)}`, payload);
  }

  delete(endpoint: string, id: string): Observable<void> {
    return this.http.delete<void>(`${API_BASE_URL}/${endpoint}/${encodeURIComponent(id)}`);
  }
}
