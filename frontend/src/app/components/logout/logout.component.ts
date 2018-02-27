import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'logout',
  templateUrl: './logout.component.html',
  styleUrls: ['./logout.component.css']
})
export class LogoutComponent implements OnInit {

  constructor(private auth: AuthService, private route: Router) { }

  ngOnInit() {
  }
  
  logMeOut() {
  	const token = localStorage.getItem('token');

    if (token) {
      this.auth.logout(token)
      .then((logoutResp) => {
      	localStorage.clear()
        this.route.navigate(['/'])
     })
      .catch((err) => {
        console.log(err);
      });
    }
  }
}
