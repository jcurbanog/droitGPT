import { Injectable } from '@angular/core'
import { HttpClient, HttpHeaders } from '@angular/common/http'

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

	public singleResponse(query: string): Promise<Response> {
		const body = { query: query }

		return new Promise<Response>((resolve) => {
			this.http
				.post<Response>(this.apiUrl, body, { headers: this.headers })
				.subscribe((answer: Response) => resolve(answer))
		})
	}
}
