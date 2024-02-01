import { CommonModule } from '@angular/common'
import { Component } from '@angular/core'
import { FormControl, FormGroup } from '@angular/forms'

import { ChatComponent } from './chat/chat.component'
import { HeaderComponent } from './header/header.component'
import { Message } from './chat/messages/messages.component'

export interface Chat {
	messages: Message[]
}

export interface QueryForm {
	input: FormControl<string | null>
}
@Component({
	selector: 'app-home',
	standalone: true,
	templateUrl: './home.component.html',
	styleUrl: './home.component.scss',
	imports: [ChatComponent, CommonModule, HeaderComponent],
})
export class HomeComponent {
	protected chats: Chat[] = [{ messages: [] }]
	protected chatIndex = 0
	protected inputForm = new FormControl<string | null>('')
	protected showMenu = false
	protected loading = false

	protected form = new FormGroup({
		input: this.inputForm,
	})

	protected createNewChat(): void {
		this.chats.push({ messages: [] })
		this.chatIndex = this.chats.length - 1
		this.closeMenu()
	}

	protected selectChat(index: number): void {
		this.chatIndex = index
		this.closeMenu()
	}

	protected closeMenu(): void {
		setTimeout(() => {
			this.showMenu = false
		}, 150)
	}
}
