import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { TicketService } from '../../services/ticket.service';
import { Ticket } from '../../models/ticket';

@Component({
  selector: 'ticket-list',
  templateUrl: './ticket-list.component.html',
  styleUrls: ['./ticket-list.component.css'],
  providers: [ AuthService ]
})
export class TicketListComponent implements OnInit {

  isLoggedIn: boolean = false;
  ticketList: [Ticket];

  constructor(private auth: AuthService, private ticket: TicketService) {}

  ngOnInit(): void {

    const token = localStorage.getItem('token');

    if (token) {

      this.ticket.getTicketList(token)
      .then((tickets) => {
        this.ticketList = tickets.json() as [Ticket];
     })
      .catch((err) => {
        console.log(err);
      });
    }


  }

  
}

