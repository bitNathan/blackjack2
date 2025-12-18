import { Routes } from '@angular/router';
import {LandingPageComponent} from './landing-page/landing-page';
import {GameComponent} from './game-page/game-page';

export const routes: Routes = [
  { path: '', component: LandingPageComponent },
  { path: 'game', component: GameComponent }
];
