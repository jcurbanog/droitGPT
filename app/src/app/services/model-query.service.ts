import { Injectable } from '@angular/core'
import { HttpClient, HttpHeaders } from '@angular/common/http'

import { Message } from '../home/chat/messages/messages.component'

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
	private apiUrl = 'http://localhost:5000/'

	constructor(private http: HttpClient) {}

	public request(endpoint: string, query: string, messages: Message[]): Promise<Response> {
		const url = `${this.apiUrl}${endpoint}`
		const body = { input: query, conversation: messages }
		const options = { headers: this.headers }

		return new Promise<Response>((resolve) => {
			this.http.post<Response>(url, body, options).subscribe((answer: Response) => resolve(answer))
		})
	}
}
