import { Route } from '@angular/router';

export default [
  {
    path: '',
    redirectTo: 'turrent',
    pathMatch: 'full',
  },
  {
    path: 'turrent',
    loadChildren: () => import('./turrent/turrent.routes'),
  },
  { path: '**', redirectTo: '' },
] as Route[];
