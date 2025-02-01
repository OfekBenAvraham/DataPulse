import { CommonModule } from '@angular/common';
import { Component, computed, inject, signal, effect } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { TableModule } from 'primeng/table';
import { ProgressBarModule } from 'primeng/progressbar';
import { ProgressStore } from '../progress/progress.component';
import { toSignal } from '@angular/core/rxjs-interop';
import { Download } from '../interfaces/progress';

@Component({
  selector: 'app-torrents',
  standalone: true,
  imports: [CommonModule, TableModule, ButtonModule, ProgressBarModule],
  templateUrl: './torrents.component.html',
  styleUrl: './torrents.component.scss',
})
export class TorrentsComponent {

  private progressStore = inject(ProgressStore);
  turrents$ = this.progressStore.downloads$;
  turrents = toSignal(this.turrents$, {
    initialValue: [] as Download[],
  });
  totalItems = computed(() => this.turrents().length);
  rowsPerPage = signal(10);

  calculateProgress(turrent: Download): number {
    return turrent?.status ?? 0; // Ensure status is not undefined
  }

  e = effect(() => {
    console.log('Current downloads:', this.turrents());
  });
  
}
