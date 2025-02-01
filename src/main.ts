import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';
import { Buffer } from 'buffer';
(window as any).Buffer = Buffer;

bootstrapApplication(AppComponent, appConfig).catch((err) =>
  console.error(err)
);
