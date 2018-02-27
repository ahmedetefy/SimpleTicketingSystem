import { Component, OnInit, Input } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { TicketService } from '../../services/ticket.service';

import { TicketItem } from '../../models/ticket-item';
import { Comment } from '../../models/comment';

@Component({
  selector: 'ticket-list',
  templateUrl: './ticket-list.component.html',
  styleUrls: ['./ticket-list.component.css'],
  providers: [ AuthService ]
})
export class TicketListComponent implements OnInit {

  toUpdate: boolean = false;
  toAddComment: boolean= false;
  ticketList: [TicketItem];
  updatedTicket: TicketItem = new TicketItem();
  @Input()
  relIndex: number;
  @Input()
  commentIndex: number;
  userEmail:string;
  commentAddition: Comment = new Comment();

  constructor(private auth: AuthService, private ticket: TicketService) {
  }

  ngOnInit(): void {
    this.getList()
    const token = localStorage.getItem('token');
    // console.log(token)
    if (token) {
      this.auth.ensureAuthenticated(token)
      .then((user) => {
        if (user.json().status === 'success') {
          this.userEmail = user.json().data['email'];
        }
      })
      .catch((err) => {
        console.log(err);
      }); 
    }
  }

  getList() {
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

  updateTicket(ticketForm) {
    let ticket: TicketItem = new TicketItem()
    ticket.subject = ticketForm.value['subject']
    ticket.type = ticketForm.value['type']
    ticket.urgency = ticketForm.value['urgency']
    ticket.status = ticketForm.value['status']
    ticket.name = ticketForm.value['name']
    ticket.email = ticketForm.value['email']
    ticket.message = ticketForm.value['message']
    ticket.id = ticketForm.value['id']
    const token = localStorage.getItem('token');
    this.ticket.updateTicket(token, ticket)
      .then((resp) => {
        alert("Your ticket has been updated successfully!")
        this.toUpdate = false
        this.getList()
     })
      .catch((err) => {
        console.log(err);
     });


  }

  delete(ticketID) {
    this.ticket.deleteTicket(localStorage.getItem('token'), ticketID)
    .then((ticketRes) => {
      alert("Your ticket has been deleted successfully!")
    })
    .catch((err) => {
      console.log(err);
    });

  }
  addCommentTicket(form) {
    const token = localStorage.getItem('token');
    this.ticket.addComment(token, form.value['ticket_id'], this.commentAddition)
      .then((resp) => {
        alert("Your comment has been updated successfully!")
        this.toAddComment = false
        form.reset()
        this.getList()
     })
      .catch((err) => {
        console.log(err);
     });

  }
  toUpdateTrigger(i) {
    this.relIndex = i;
    if(this.toUpdate) {
      this.toUpdate = false;
      this.getList()
    }
    else {
      this.toUpdate = true;
    }
  }

  toCommentTrigger(i) {
    this.commentIndex = i;
    if(this.toAddComment) {
      this.toAddComment = false;
      this.getList()
    }
    else {
      this.toAddComment = true;
    }
  }

  
}

