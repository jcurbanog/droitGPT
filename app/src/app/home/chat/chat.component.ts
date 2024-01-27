import { CommonModule } from '@angular/common'
import { Component } from '@angular/core'
import { FormControl } from '@angular/forms'

import { Message, MessagesComponent } from './messages/messages.component'
import { InputMessageComponent } from './input-message/input-message.component'

import { ModelQueryService, Response } from '../../services/model-query.service'

@Component({
	selector: 'app-chat',
	standalone: true,
	templateUrl: './chat.component.html',
	styleUrl: './chat.component.scss',
	imports: [CommonModule, MessagesComponent, InputMessageComponent],
})
export class ChatComponent {
	protected inputForm = new FormControl<string | null>('')
	protected messages: Message[] = []

	constructor(private modelService: ModelQueryService) {}

	protected async sendMessage(): Promise<void> {
		const query = this.inputForm.value
		if (query) {
			this.inputForm.setValue('')
			this.messages.push({ text: query, speaker: 'user' })
			const response: Response = await this.modelService.singleResponse(query, this.messages.slice(0, -1))
			if (response.response.length) {
				this.messages.push({ text: response.response[0], speaker: 'bot' })
			}
		}
	}
}
