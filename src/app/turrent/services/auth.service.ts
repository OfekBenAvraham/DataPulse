import { HttpClient } from '@angular/common/http';
import { inject, Injectable, OnInit, signal } from '@angular/core';
import { Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService{

  isAuthenticatedSignal = signal(false);
  private apiUrl = 'http://127.0.0.1:8001';
  private http = inject(HttpClient)


  // isAuthenticated() {
  //   return this.isAuthenticatedSignal.asReadonly();
  // }

  login(email: string, password: string): Observable<any> {
    const url = `${this.apiUrl}/login`;
    return this.http.post(url, { email, password }).pipe(
      tap((response: any) => {
        localStorage.setItem('authToken', response.token);
        this.isAuthenticatedSignal.set(true);
      })
    );
  }

  register(email: string, password: string): Observable<any> {
    const url = `${this.apiUrl}/register`;
    return this.http.post(url, { email, password }).pipe(
      tap(() => {
        this.isAuthenticatedSignal.set(true);
      })
    );
  }

  logout(): Observable<any> {
    const url = `${this.apiUrl}/logout`;
    return this.http.post(url, {}).pipe(
      tap(() => {
        localStorage.removeItem('authToken');
        this.isAuthenticatedSignal.set(false);
      })
    );
  }

  checkAuthenticationOnInit() {
    const token = localStorage.getItem('authToken');
    if (token) {
      this.isAuthenticatedSignal.set(true);
    }
  }
}
