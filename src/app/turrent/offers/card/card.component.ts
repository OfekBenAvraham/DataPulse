import { Component, Input, Output, EventEmitter, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './card.component.html',
  styleUrl: './card.component.scss',
})
export class CardComponent {
  @Input() item!: { title: string; image: string; category: string };
  @Output() downloadClicked = new EventEmitter<void>();

  isLoading = signal(false);
  isSuccess = signal(false);

  onDownload() {
    this.isLoading.set(true);
    this.downloadClicked.emit();

    // Simulate success after 1.5 seconds
    setTimeout(() => {
      this.isLoading.set(false);
      this.isSuccess.set(true);

      // Reset to "Download" button after 2 seconds
      setTimeout(() => {
        this.isSuccess.set(false);
      }, 2000);
    }, 1500);
  }
}
