import { Injectable } from '@angular/core'
import { HttpClient, HttpHeaders } from '@angular/common/http'

import { Message } from '../home/chat/messages/messages.component'

export interface Response {
	response: string[]
	additional_info: string
}

const DEFAULT_ERROR = "J'ai rencontré des difficultés techniques. Veuillez réessayer ultérieurement."

const PORT = process.env['PORT'] || 5000

@Injectable({
	providedIn: 'root',
})
export class ModelQueryService {
	private headers = new HttpHeaders({
		'Content-Type': 'application/json',
	})

	private apiUrl: string

	constructor(private http: HttpClient) {
		// Set apiUrl based on the host where the app is running
		const host = window.location.host.split(':')[0]
		this.apiUrl = `http://${host}:${PORT}/`
	}

	public request(endpoint: string, query: string, messages: Message[]): Promise<Response> {
		const url = `${this.apiUrl}${endpoint}`
		const conversation = messages.map((message) => ({
			text: message.text[message.index],
			speaker: message.speaker,
		}))
		const body = { input: query, conversation: conversation }
		const options = { headers: this.headers }

		return new Promise<Response>((resolve) => {
			this.http.post<Response>(url, body, options).subscribe({
				next: (answer: Response) => resolve(answer),
				error: () => resolve({ response: [DEFAULT_ERROR], additional_info: '' }),
			})
		})
	}
}
