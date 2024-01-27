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
	private apiUrl = 'http://localhost:5000/single_response'

	constructor(private http: HttpClient) {}

	public singleResponse(query: string, messages: Message[]): Promise<Response> {
		const body = { input: query, conversation: messages }
		const options = { headers: this.headers }

		return new Promise<Response>((resolve) => {
			this.http.post<Response>(this.apiUrl, body, options).subscribe((answer: Response) => resolve(answer))
		})
	}
}
