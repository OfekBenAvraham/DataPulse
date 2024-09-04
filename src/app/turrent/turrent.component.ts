import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SidebarComponent } from './sidebar/sidebar.component';
@Component({
  selector: 'app-turrent',
  standalone: true,
  imports: [RouterOutlet,SidebarComponent],
  templateUrl: './turrent.component.html',
  styleUrl: './turrent.component.scss'
})
export class TurrentComponent {

}
