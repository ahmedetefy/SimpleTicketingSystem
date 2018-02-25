import { Injectable } from '@angular/core';

@Injectable()
export class AuthService {

  constructor() { }

  test(): string {
  	return "It is working"
  }

}
