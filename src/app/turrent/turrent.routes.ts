import { Route } from '@angular/router';
import { TurrentComponent } from './turrent.component';

export default [
  {
    path: '',
    component: TurrentComponent,
    children: [
      {
        path: '',
        redirectTo: 'turrents',
        pathMatch: 'full',
      },
      {
        path: 'turrents',
        loadComponent: () =>
          import('./torrents/torrents.component').then(
            (c) => c.TorrentsComponent
          ),
      },
      {
        path: 'offers',
        loadComponent: () =>
          import('./offers/offers.component').then(
            (c) => c.OffersComponent
          ),
      },
    ],
  },
] as Route[];