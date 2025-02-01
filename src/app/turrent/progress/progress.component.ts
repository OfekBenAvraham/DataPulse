import { inject, Injectable } from '@angular/core';
import { ComponentStore } from '@ngrx/component-store';
import { Download, ProgressState, Upload } from '../interfaces/progress';
import { Observable } from 'rxjs';
import { SocketService } from '../services/socket.service';

@Injectable({
  providedIn: 'root',
})
export class ProgressStore extends ComponentStore<ProgressState> {
  constructor(private socketService: SocketService) {
    super({ downloads: [], uploads: [] });

    // Listen to download progress updates
    this.socketService.listen('download_progress').subscribe((data) => {
      console.log('Download progress received:', data); // Debugging
      this.updateDownloadProgress(data);
    });
  }

  readonly downloads$: Observable<Download[]> = this.select(
    (state) => state.downloads
  );

  readonly uploads$: Observable<Upload[]> = this.select(
    (state) => state.uploads
  );

  readonly addDownload = this.updater((state, download: Download) => ({
    ...state,
    downloads: [...state.downloads, download],
  }));

  readonly addUpload = this.updater((state, upload: Upload) => ({
    ...state,
    uploads: [...state.uploads, upload],
  }));

  // Update the progress of a specific download
  readonly updateDownloadProgress = this.updater(
    (state, payload: { name: string; progress: number }) => {
      console.log('Updating download progress for:', payload); // Debugging
      return {
        ...state,
        downloads: state.downloads.map((download) =>
          download.name === payload.name
            ? { ...download, status: payload.progress }
            : download
        ),
      };
    }
  );
}
