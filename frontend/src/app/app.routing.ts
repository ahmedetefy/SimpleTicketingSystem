import {NgModule} 			   from '@angular/core';
import {RouterModule, Routes } from '@angular/router';

import { HomeComponent } from './components/home/home.component';
import { LoginComponent } from './components/login/login.component';
import { TicketListComponent } from './components/ticket-list/ticket-list.component';
import { EnsureAuthenticated } from './services/ensure-authenticated.service';
import { LoginRedirect } from './services/login-redirect.service';

const appRoutes: Routes = [
	{
        path:"",
        component: HomeComponent,
    },
    {
        path:"login",
        component: LoginComponent,
        canActivate: [LoginRedirect]
    },
    {
        path:"tickets",
        component: TicketListComponent,
        canActivate: [EnsureAuthenticated]
    }
]

@NgModule({
	imports: [
		RouterModule.forRoot(
			appRoutes
			)
	],
	exports: [
		RouterModule
	]
})

export class AppRoutingModule {}