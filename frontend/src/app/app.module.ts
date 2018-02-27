import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app.routing';
import { HomeComponent } from './components/home/home.component';
import { LoginComponent } from './components/login/login.component';
import { TicketListComponent } from './components/ticket-list/ticket-list.component';

import { EnsureAuthenticated } from './services/ensure-authenticated.service';
import { LoginRedirect } from './services/login-redirect.service';
import { AuthService } from './services/auth.service';
import { TicketService } from './services/ticket.service';
import { LogoutComponent } from './components/logout/logout.component';



@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    LoginComponent,
    TicketListComponent,
    LogoutComponent,
  ],
  imports: [
  	AppRoutingModule,
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [
    AuthService,
    LoginRedirect,
    EnsureAuthenticated,
    TicketService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
