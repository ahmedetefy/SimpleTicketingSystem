import {NgModule} 			   from '@angular/core';
import {RouterModule, Routes } from '@angular/router';

import { HomeComponent } from './components/home/home.component';
import { LoginComponent } from './components/login/login.component';

const appRoutes: Routes = [
	{
        path:"",
        component: HomeComponent,
    },
    {
        path:"login",
        component: LoginComponent,
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