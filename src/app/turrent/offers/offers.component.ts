import { Component, signal } from '@angular/core';
import { NavbarComponent } from './navbar/navbar.component';

@Component({
  selector: 'app-offers',
  standalone: true,
  imports: [NavbarComponent],
  templateUrl: './offers.component.html',
  styleUrl: './offers.component.scss'
})
export class OffersComponent {
  selectedCategory = signal('movies');

  items = signal([
    { title: 'Garfild', image: '../../../assets/images/garfild.jpg', category: 'movies' },
    { title: 'Deadpool', image: '../../../assets/images/deadpool.jpg', category: 'movies' },
    { title: 'Vampire diaries', image: '../../../assets/images/vampire-diaries.jpg', category: 'tvshows' },
    { title: 'CS2', image: '../../../assets/images/cs2.jpg', category: 'games' },
    { title: 'Zoom', image: '../../../assets/images/zoom.png', category: 'programs' },
    // Add more items as needed
  ]);

  onCategorySelected(category: string) {
    this.selectedCategory.set(category);
  }

  filteredItems() {
    return this.items().filter(item => item.category === this.selectedCategory());
  }
}
