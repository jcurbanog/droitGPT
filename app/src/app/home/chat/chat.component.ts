import { CommonModule } from '@angular/common'
import { Component } from '@angular/core'

import { MessagesComponent } from './messages/messages.component'
import { InputMessageComponent } from './input-message/input-message.component'

@Component({
	selector: 'app-chat',
	standalone: true,
	templateUrl: './chat.component.html',
	styleUrl: './chat.component.scss',
	imports: [CommonModule, MessagesComponent, InputMessageComponent],
})
export class ChatComponent {}
