import { Component, inject, OnInit } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SidebarComponent } from './sidebar/sidebar.component';
import { NavbarComponent } from './navbar/navbar.component';
import { AuthService } from './services/auth.service';
@Component({
  selector: 'app-turrent',
  standalone: true,
  imports: [RouterOutlet, SidebarComponent, NavbarComponent],
  templateUrl: './turrent.component.html',
  styleUrl: './turrent.component.scss',
})
export class TurrentComponent {}
