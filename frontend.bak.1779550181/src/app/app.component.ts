import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Enterprise RAG System';
  isLoggedIn = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {
    this.authService.isLoggedIn$.subscribe(
      (loggedIn) => this.isLoggedIn = loggedIn
    );
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
