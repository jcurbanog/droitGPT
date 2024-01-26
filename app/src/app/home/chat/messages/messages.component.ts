import { Component, Input } from '@angular/core'
import { CommonModule } from '@angular/common'

import { MessageComponent } from './message/message.component'

export interface Message {
	content: string
	type: 'question' | 'answer'
}
@Component({
	selector: 'app-messages',
	standalone: true,
	templateUrl: './messages.component.html',
	styleUrl: './messages.component.scss',
	imports: [CommonModule, MessageComponent],
})
export class MessagesComponent {
	@Input({ required: true }) public messages!: Message[]
}
