import {NgModule} 			   from '@angular/core';
import {RouterModule, Routes } from '@angular/router';

import { HomeComponent } from './components/home/home.component';
import { LoginComponent } from './components/login/login.component';
import { TicketListComponent } from './components/ticket-list/ticket-list.component';

const appRoutes: Routes = [
	{
        path:"",
        component: HomeComponent,
    },
    {
        path:"login",
        component: LoginComponent,
    },
    {
        path:"tickets",
        component: TicketListComponent,
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