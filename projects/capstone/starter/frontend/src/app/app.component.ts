import { Component, OnInit } from '@angular/core';
import { AuthService } from './services/auth.service';
import { Router } from "@angular/router";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'SMADD Casting Agency';
  loginURL: string;

  constructor( public auth: AuthService,
                private router: Router ) {
      this.initializeApp();
      this.loginURL = this.auth.build_login_link('');
  }

  initializeApp() {
      this.auth.load_jwts();
      this.auth.check_token_fragment();
      this.auth.getUserProfile();
  }

  ngOnInit() {

  }

  goLogin(){
    window.location.href = this.loginURL;
  }

  logout() {
      this.auth.logout();
  }

}
