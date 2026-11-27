import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);

  list<T>(endpoint: string): Observable<T[]> {
    return this.http.get<T[]>(`${environment.apiBaseUrl}/${endpoint}`);
  }

  get<T>(endpoint: string, id: string): Observable<T> {
    return this.http.get<T>(`${environment.apiBaseUrl}/${endpoint}/${encodeURIComponent(id)}`);
  }

  create<T>(endpoint: string, payload: Record<string, unknown>): Observable<T> {
    return this.http.post<T>(`${environment.apiBaseUrl}/${endpoint}`, payload);
  }

  update<T>(endpoint: string, id: string, payload: Record<string, unknown>): Observable<T> {
    return this.http.put<T>(
      `${environment.apiBaseUrl}/${endpoint}/${encodeURIComponent(id)}`,
      payload,
    );
  }

  delete(endpoint: string, id: string): Observable<void> {
    return this.http.delete<void>(`${environment.apiBaseUrl}/${endpoint}/${encodeURIComponent(id)}`);
  }
}
