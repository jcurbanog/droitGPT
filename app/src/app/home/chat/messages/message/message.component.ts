import { Component, EventEmitter, Input, Output } from '@angular/core'
import { Message } from '../messages.component'
import { CommonModule } from '@angular/common'

@Component({
	selector: 'app-message',
	standalone: true,
	imports: [CommonModule],
	templateUrl: './message.component.html',
	styleUrl: './message.component.scss',
})
export class MessageComponent {
	@Input({ required: true }) public message!: Message

	@Output() public regenerateResponse = new EventEmitter<void>()

	protected showMoreInfo = false

	protected increaseIndex(): void {
		if (this.message.index < this.message.text.length - 1) {
			this.message.index++
		}
	}

	protected decreaseIndex(): void {
		if (0 < this.message.index) {
			this.message.index--
		}
	}
}
