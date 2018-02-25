import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';
import 'rxjs/add/operator/toPromise';

@Injectable()
export class AuthService {
	private BASE_URL: string = 'http://0.0.0.0:8000/auth';
  	private headers: Headers = new Headers({'Content-Type': 'application/json'});
	test(): string {
		return "working"
	}

    constructor(private http: Http) { }

    login(user): Promise<any> {
	    let url: string = `${this.BASE_URL}/login`;
	    return this.http.post(url, user, {headers: this.headers}).toPromise();
	}

	register(user): Promise<any> {
	    let url: string = `${this.BASE_URL}/register`;
	    return this.http.post(url, user, {headers: this.headers}).toPromise();
	}


}
