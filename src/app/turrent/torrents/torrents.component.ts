import { CommonModule } from '@angular/common';
import { Component, computed, signal } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { TableModule } from 'primeng/table';
import { ProgressBarModule } from 'primeng/progressbar';

@Component({
  selector: 'app-torrents',
  standalone: true,
  imports: [CommonModule, TableModule, ButtonModule, ProgressBarModule],
  templateUrl: './torrents.component.html',
  styleUrl: './torrents.component.scss',
})
export class TorrentsComponent {
  turrents = signal([
    { name: 'test', size: '10G', speed: '530 kB/s', value: 80 },
    { name: 'test', size: '10G', speed: '530 kB/s', value: 70 },
    { name: 'test', size: '10G', speed: '530 kB/s', value: 75 },
    { name: 'test', size: '10G', speed: '530 kB/s', value: 88 },
    { name: 'test', size: '10G', speed: '530 kB/s', value: 65 },
    { name: 'test', size: '10G', speed: '530 kB/s', value: 70 },
    { name: 'test', size: '10G', speed: '530 kB/s', value: 77 },
    { name: 'test', size: '10G', speed: '530 kB/s', value: 100 },
    { name: 'test', size: '10G', speed: '530 kB/s', value: 58 },
    { name: 'test', size: '10G', speed: '530 kB/s', value: 67 },
    { name: 'test', size: '10G', speed: '530 kB/s', value: 58 },
    { name: 'test', size: '10G', speed: '530 kB/s', value: 67 },
    { name: 'test', size: '10G', speed: '530 kB/s', value: 58 },
    { name: 'test', size: '10G', speed: '530 kB/s', value: 67 },
    { name: 'test', size: '10G', speed: '530 kB/s', value: 58 },
    { name: 'test', size: '10G', speed: '530 kB/s', value: 67 },
  ]);
  totalItems = computed(() => this.turrents().length);
  rowsPerPage = signal(10);

  calculateProgress(turrent: any): number {
    // return the progress value for the turrent, ensure it's between 0 and 100
    return turrent.value ? turrent.value : 0;
  }
  
}
