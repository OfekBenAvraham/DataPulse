import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Item } from '../interfaces/item';

@Injectable({
  providedIn: 'root',
})
export class FileService {
  private apiUrl = 'http://127.0.0.1:8001';
  private http = inject(HttpClient);

  files_summary(): Observable<any> {
    const url = `${this.apiUrl}/files_summary`;
    return this.http.get<Item[]>(url);
  }

  download_file(name: string, type: string): Observable<any> {
    const url = `${this.apiUrl}/download_from_select`;
    return this.http.post(url, { name: name, type: type });
  }

  upload_file(payload: { file_path: string }): Observable<any> {
    const url = `${this.apiUrl}/upload`;
    return this.http.post(url, payload); // Sends the file path payload to the backend
  }

  download_torrent(payload: { torrent_path: string }): Observable<any> {
    const url = `${this.apiUrl}/download`;
    return this.http.post(url, payload);
  }
  
}
