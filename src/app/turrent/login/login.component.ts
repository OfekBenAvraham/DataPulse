import { Component, inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { DynamicDialogRef } from 'primeng/dynamicdialog';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { AuthService } from '../services/auth.service';
import { PasswordModule } from 'primeng/password';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    PasswordModule,
    ButtonModule,
    InputTextModule,
  ],
  providers: [AuthService],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private ref = inject(DynamicDialogRef);
  private toastr = inject(ToastrService);
  constructor() {}

  ngOnInit(): void {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required],
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      const { email, password } = this.loginForm.value;
      this.authService.login(email, password).subscribe(
        () => {
          this.toastr.success(
            'Login Successful',
            'You have been logged in successfully.'
          );
          this.ref.close(true);
        },
        (error) => {
          if (error.status === 401) {
            this.toastr.error('Login Failed', 'Invalid email or password.');
          } else {
            this.toastr.error('Error', 'An unexpected error occurred.');
          }
        }
      );
    }
  }
}
