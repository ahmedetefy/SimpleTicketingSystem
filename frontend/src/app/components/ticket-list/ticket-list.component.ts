import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { TicketService } from '../../services/ticket.service';
import { TicketItem } from '../../models/ticket-item';

@Component({
  selector: 'ticket-list',
  templateUrl: './ticket-list.component.html',
  styleUrls: ['./ticket-list.component.css'],
  providers: [ AuthService ]
})
export class TicketListComponent implements OnInit {

  isLoggedIn: boolean = false;
  ticketList: [TicketItem];

  constructor(private auth: AuthService, private ticket: TicketService) {}

  ngOnInit(): void {

    const token = localStorage.getItem('token');

    if (token) {

      this.ticket.getTicketList(token)
      .then((tickets) => {
        this.ticketList = tickets.json() as [TicketItem];
     })
      .catch((err) => {
        console.log(err);
      });
    }


  }

  
}

