import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';

import { User } from '../../models/user';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  providers: [ AuthService ]
})
export class LoginComponent implements OnInit {
  user: User = new User();

  constructor(private auth: AuthService, private router:Router) { }

  ngOnInit(): void {}

  login(): void {
  	this.auth.login(this.user)
    .then((user) => {
      localStorage.setItem('token', user.json().auth_token);
      this.router.navigateByUrl('/tickets');
    })
    .catch((err) => {
      console.log(err);
    });
  }

}
