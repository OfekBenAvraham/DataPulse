import { Component, effect, inject, OnInit, signal } from '@angular/core';
import { NavbarComponent } from './navbar/navbar.component';
import { FileService } from '../services/file.service';
import { toSignal } from '@angular/core/rxjs-interop';
import { Item } from '../interfaces/item';
import { ProgressStore } from '../progress/progress.component';
import { ToastrService } from 'ngx-toastr';
import { CardComponent } from './card/card.component';
import { DialogModule } from 'primeng/dialog';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { FormsModule } from '@angular/forms';
import bencode from 'bencode';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-offers',
  standalone: true,
  imports: [
    CommonModule,
    NavbarComponent,
    InputTextModule,
    ButtonModule,
    CardComponent,
    DialogModule,
    FormsModule,
  ],
  templateUrl: './offers.component.html',
  styleUrl: './offers.component.scss',
})
export class OffersComponent {
  selectedCategory = signal('movies');
  fileService = inject(FileService);
  private toastr = inject(ToastrService);
  private progressStore = inject(ProgressStore);
  // Dialog visibility states
  uploadDialogVisible = signal(false);
  downloadDialogVisible = signal(false);
  torrentFile: File | null = null;
  filePath = signal(''); // Input value for the file path
  torrentPath = signal('');

  items = toSignal(this.fileService.files_summary(), {
    initialValue: [] as Item[],
  });

  // Open/Close dialog handlers
  openUploadDialog() {
    this.uploadDialogVisible.set(true);
  }

  openDownloadDialog() {
    this.downloadDialogVisible.set(true);
  }

  // Handle file upload
  uploadFile() {
    // const filePath = this.filePath();

    // if (!filePath) {
    //   this.toastr.error('Please enter a valid file path');
    //   return;
    // }

    // const payload = { file_path: filePath };

    // this.toastr.info('Uploading file...');
    // this.fileService.upload_file(payload).subscribe({
    //   next: () => {
    //     this.toastr.success('File uploaded successfully');
    //     this.uploadDialogVisible.set(false); // Close the dialog
    //     this.filePath.set(''); // Reset the input field
    //   },
    //   error: (err) => {
    //     this.toastr.error('Error during file upload');
    //     console.error('Upload failed:', err);
    //   },
    // });
  }

  // Handle torrent download
  downloadTorrent() {
    const torrentPath = this.torrentPath();

    if (!torrentPath) {
      this.toastr.error('Please enter a valid torrent path');
      return;
    }

    const payload = { torrent_path: torrentPath };

    this.toastr.info('Downloading torrent...');

    this.fileService.download_torrent(payload).subscribe({
      next: () => {
        this.toastr.success('Torrent downloaded successfully');
        this.downloadDialogVisible.set(false); // Close the dialog
        this.torrentPath.set(''); // Reset the input field
      },
      error: (err) => {
        this.toastr.error('Error during torrent download');
        console.error('Download failed:', err);
      },
    });
  }

  onCategorySelected(category: string) {
    this.selectedCategory.set(category);
  }

  filteredItems() {
    return this.items()?.filter(
      (item: Item) => item.category === this.selectedCategory()
    );
  }

  startToDownload(item: Item) {
    let size = item.size + ' MB';
    this.progressStore.addDownload({
      name: item.title,
      size: size,
      type: 'Download',
      status: 0,
    });
    this.fileService.download_file(item.title, item.type).subscribe({
      next: (value) => {
        this.toastr.success('Download complete');
      },
      error: (err) => {
        this.toastr.error('Error during download');
        console.error('Observable emitted an error: ' + JSON.stringify(err));
      },
    });
  }

  torrentData: any = null;

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (!input.files || input.files.length === 0) return;

    const file = input.files[0];

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const buffer = new Uint8Array(reader.result as ArrayBuffer);
        const decodedTorrent = bencode.decode(buffer);

        // Extract necessary fields
        const decoder = new TextDecoder('utf-8'); // ✅ Create a UTF-8 decoder
        const name = decodedTorrent.info?.name ? decoder.decode(decodedTorrent.info.name) : null;
        const type = decodedTorrent.info?.type ? decoder.decode(decodedTorrent.info.type) : null;        
        const totalChunks = decodedTorrent.info?.total_chunks ? Number(decodedTorrent.info.total_chunks) : 0;

        this.torrentData = { name, type, totalChunks };
        console.log(this.torrentData);

        this.progressStore.addDownload({
          name: name || '',
          size: totalChunks * 20 + ' MB',
          type: 'Download',
          status: 0,
        });

        this.fileService.download_file(name || '', type || '').subscribe({
          next: (value) => {
            this.toastr.success('Download complete');
          },
          error: (err) => {
            this.toastr.error('Error during download');
            console.error('Observable emitted an error: ' + JSON.stringify(err));
          },
        });
        
      } catch (error) {
        console.error('Error decoding .torrent file:', error);
      }
    };

    reader.readAsArrayBuffer(file);
  }
}
