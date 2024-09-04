import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { DialogService } from 'primeng/dynamicdialog';
import routes from './app.routes';
import { provideHttpClient } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';


export const appConfig: ApplicationConfig = {
  providers: [
    
    // provide http Client
    provideAnimations(),

    provideRouter(routes),
    provideHttpClient(),

    // primeng dialog
    DialogService,

  ],
};
