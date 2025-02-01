import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { DialogService } from 'primeng/dynamicdialog';
import routes from './app.routes';
import { provideHttpClient } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { MessageService } from 'primeng/api';
import { provideToastr } from 'ngx-toastr';


export const appConfig: ApplicationConfig = {
  providers: [
    
    // provide http Client
    provideAnimations(),
    provideRouter(routes),
    provideHttpClient(),
    provideToastr(),
    
    // primeng 
    MessageService,
    DialogService,

  ],
};
