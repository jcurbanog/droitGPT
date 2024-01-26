import { Component } from '@angular/core'

import { MessageComponent } from './message/message.component'

@Component({
	selector: 'app-messages',
	standalone: true,
	templateUrl: './messages.component.html',
	styleUrl: './messages.component.scss',
	imports: [MessageComponent],
})
export class MessagesComponent {}
