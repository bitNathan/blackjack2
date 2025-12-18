import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'landing-page',
  imports: [],
  templateUrl: './landing-page.html',
  styleUrl: './landing-page.css',
})
export class LandingPageComponent {
  constructor(private router: Router) {}

  goToGame() {
    this.router.navigate(['/game']);
  }
}
