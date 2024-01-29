import { Injectable, Inject } from '@angular/core'
import { HttpClient, HttpHeaders } from '@angular/common/http'

import { Message } from '../home/chat/messages/messages.component'

import { DOCUMENT } from '@angular/common';


export interface Response {
	response: string[]
}

@Injectable({
	providedIn: 'root',
})
export class ModelQueryService {

	private headers = new HttpHeaders({
		'Content-Type': 'application/json',
	})

	private apiUrl: string;
	constructor(private http: HttpClient, @Inject(DOCUMENT) private document: Document) {
		// Set apiUrl based on the host where the app is running
		const host = this.document.location.host.split(":")[0]
		this.apiUrl = `http://${host}:5000/`;
		console.log(this.apiUrl)
	}


	public request(endpoint: string, query: string, messages: Message[]): Promise<Response> {
		const url = `${this.apiUrl}${endpoint}`
		const body = { input: query, conversation: messages }
		const options = { headers: this.headers }

		return new Promise<Response>((resolve) => {
			this.http.post<Response>(url, body, options).subscribe((answer: Response) => resolve(answer))
		})
	}
}
