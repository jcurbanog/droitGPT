import { Component, EventEmitter, Input, Output } from '@angular/core'
import { CommonModule } from '@angular/common'

import { MessageComponent } from './message/message.component'

export interface Message {
	text: string
	speaker: 'user' | 'bot'
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
	@Input({ required: true }) public cachedMessages!: Message[]

	@Output() public oneMoreAnswer = new EventEmitter<void>()
}
