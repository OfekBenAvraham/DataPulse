import { CommonModule } from '@angular/common';
import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { DialogService, DynamicDialogRef } from 'primeng/dynamicdialog';
import { LoginComponent } from '../login/login.component';
import { RegisterComponent } from '../register/register.component';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule],
  providers: [DialogService, LoginComponent, RegisterComponent],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss',
})
export class NavbarComponent implements OnInit {
  private dialogService = inject(DialogService);
  private authService = inject(AuthService);
  isAuthenticated = inject(AuthService).isAuthenticatedSignal;
  ref: DynamicDialogRef | undefined;

  ngOnInit(): void {
    this.authService.checkAuthenticationOnInit();
  }

  openLogin() {
    this.ref = this.dialogService.open(LoginComponent, {
      header: 'Login',
      width: '30%',
    });

    this.ref.onClose.subscribe((isLoggedIn: boolean) => {
      this.authService.checkAuthenticationOnInit();
    });
  }

  openRegister() {
    this.dialogService.open(RegisterComponent, {
      header: 'Register',
      width: '30%',
    });
  }

  logout() {
    this.authService.logout().subscribe(
      () => {
        this.authService.checkAuthenticationOnInit();
      },
      (error) => {}
    );
  }
}
