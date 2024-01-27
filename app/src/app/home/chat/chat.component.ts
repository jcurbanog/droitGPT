import { CommonModule } from '@angular/common'
import { Component, Input } from '@angular/core'
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
	@Input({ required: true }) public form!: FormGroup<QueryForm>

	protected messages: Message[] = []

	constructor(private modelService: ModelQueryService) {}

	protected async sendMessage(): Promise<void> {
		const query = this.form.controls.input.value
		if (query) {
			this.form.controls.input.setValue('')
			this.messages.push({ text: query, speaker: 'user' })
			const response: Response = await this.modelService.request(
				`${this.form.controls.mode.value.toLowerCase()}_response`,
				query,
				this.messages.slice(0, -1)
			)
			if (response.response.length) {
				this.messages.push({ text: response.response[0], speaker: 'bot' })
			}
		}
	}
}
