import { Component, Input } from '@angular/core'
import { CommonModule } from '@angular/common'

import { MessageComponent } from './message/message.component'

export interface Message {
	text: string[]
	speaker: 'user' | 'bot'
	index: number
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
