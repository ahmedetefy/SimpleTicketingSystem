import { Component, OnInit } from '@angular/core';

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

  constructor(private auth: AuthService) { }

  ngOnInit(): void {
    let sampleUser: any = {
      email: 'michael@realpython.com' as string,
      password: 'michael' as string
    };
    this.auth.register(sampleUser)
    .then((user) => {
      console.log(user.json());
    })
    .catch((err) => {
      console.log(err);
    });
  }

  login(): void {
  	this.auth.login(this.user)
    .then((user) => {
      localStorage.setItem('token', user.json().auth_token);
      console.log(user.json());
    })
    .catch((err) => {
      console.log(err);
    });
  }

}
