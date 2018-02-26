import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';
import { TicketItem } from '../models/ticket-item';
import 'rxjs/add/operator/toPromise';


@Injectable()
export class TicketService {
   private BASE_URL: string = 'http://localhost:8000/tickets';
   private headers: Headers = new Headers({'Content-Type': 'application/json'});
   constructor(private http: Http) {}

   getTicketList(token): Promise<any> {
     let url: string = `${this.BASE_URL}/list`;
     let headers: Headers = new Headers({
	    'Content-Type': 'application/json',
	    Authorization: `Bearer ${token}`
	  });
     return this.http.get(url, {headers: headers}).toPromise();
   }

   submitTicket(ticket: TicketItem) {
    let url: string = `${this.BASE_URL}/create`;
    return this.http.post(url, ticket, {headers: this.headers}).toPromise();
   }

}
