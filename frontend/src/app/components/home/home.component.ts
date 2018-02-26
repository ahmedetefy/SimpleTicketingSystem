import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { TicketService } from '../../services/ticket.service';

import { TicketItem } from '../../models/ticket-item';

@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  ticketSubmitted: TicketItem = new TicketItem();

  constructor(private ticket: TicketService, private router:Router) { }

  ngOnInit() {
  }
  
  submitTicket(ticketForm) {
  	this.ticket.submitTicket(this.ticketSubmitted)
    .then((ticketRes) => {
      ticketForm.reset()
      alert("Your ticket has been submitted successfully!")

    })
    .catch((err) => {
      console.log(err);
    });
  	
  }

}
