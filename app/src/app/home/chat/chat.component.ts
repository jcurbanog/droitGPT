import { CommonModule } from '@angular/common'
import { Component, HostListener, Input } from '@angular/core'
import { FormGroup } from '@angular/forms'

import { Message, MessagesComponent } from './messages/messages.component'
import { InputMessageComponent } from './input-message/input-message.component'

import { ModelQueryService, Response } from '../../services/model-query.service'
import { QueryForm } from '../home.component'

@Component({
	selector: 'app-chat',
	standalone: true,
	templateUrl: './chat.component.html',
	styleUrl: './chat.component.scss',
	imports: [CommonModule, MessagesComponent, InputMessageComponent],
})
export class ChatComponent {
	@HostListener('keydown', ['$event'])
	protected async onKeyDown(event: KeyboardEvent): Promise<void> {
		if (event.code === 'Enter' && !event.shiftKey) {
			event.preventDefault()
			await this.sendMessage()
		}
	}

	@Input({ required: true }) public form!: FormGroup<QueryForm>

	protected messages: Message[] = []
	protected loading: boolean = false

	constructor(private modelService: ModelQueryService) {}

	protected async sendMessage(): Promise<void> {
		const query = this.form.controls.input.value
		if (query && !this.loading) {
			this.loading = true
			this.form.controls.input.setValue('')
			this.messages.push({ text: [query], speaker: 'user', index: 0 })
			const response: Response = await this.modelService.request(
				`${this.form.controls.mode.value.toLowerCase()}_response`,
				query,
				this.messages.slice(0, -1)
			)
			this.loading = false
			if (response.response.length) {
				this.messages.push({ text: response.response, speaker: 'bot', index: 0 })
			}
		}
	}
}
