import { CommonModule } from '@angular/common'
import { Component, ElementRef, EventEmitter, HostListener, Input, Output, ViewChild } from '@angular/core'
import { FormGroup } from '@angular/forms'

import { Message, MessagesComponent } from './messages/messages.component'
import { InputMessageComponent } from './input-message/input-message.component'

import { ModelQueryService, Response } from '../../services/model-query.service'
import { QueryForm } from '../home.component'
import { StartUpButtonsComponent } from './start-up-buttons/start-up-buttons.component'

const DEFAULT_INPUTS = [
	"Qu'est-ce que la discrimination en milieu professionnel ?",
	"Qu'est-ce que le comité social et économique (CSE) ?",
	"Qui a la responsabilité de l'organisation et du fonctionnement des transports scolaires ?",
	'Les soldats de l’armée peuvent-ils voter ?',
]

@Component({
	selector: 'app-chat',
	standalone: true,
	templateUrl: './chat.component.html',
	styleUrl: './chat.component.scss',
	imports: [CommonModule, MessagesComponent, InputMessageComponent, StartUpButtonsComponent],
})
export class ChatComponent {
	@HostListener('keydown', ['$event'])
	protected async onKeyDown(event: KeyboardEvent): Promise<void> {
		if (event.code === 'Enter' && !event.shiftKey) {
			event.preventDefault()
			await this.sendMessage()
		}
	}

	@ViewChild('messagesWrapper') public messagesWrapper?: ElementRef

	@Input({ required: true }) public form!: FormGroup<QueryForm>
	@Input({ required: true }) public messages!: Message[]
	@Input({ required: true }) public loading!: boolean

	@Output() public loadingChange = new EventEmitter<boolean>()

	protected defaultInputs: string[] = DEFAULT_INPUTS

	constructor(private modelService: ModelQueryService) {}

	protected async sendMessage(): Promise<void> {
		const query = this.form.controls.input.value
		if (query && !this.loading) {
			this.loadingChange.emit(true)
			this.form.controls.input.setValue('')
			this.messages.push({ text: [query], speaker: 'user', index: 0, additionalInfo: [''] })
			this.scrollToLastMessage()
			const response: Response = await this.modelService.request(
				'single_response',
				query,
				this.messages.slice(0, -1)
			)
			this.loadingChange.emit(false)
			if (response.response.length) {
				this.messages.push({
					text: response.response,
					speaker: 'bot',
					index: 0,
					additionalInfo: [response.additional_info || ''],
				})
				this.scrollToLastMessage()
			}
		}
	}

	protected async onRegenerateResponse(index: number): Promise<void> {
		const query = this.messages[index - 1].text[0]
		if (query && !this.loading) {
			this.loadingChange.emit(true)
			const response: Response = await this.modelService.request(
				'single_response',
				query,
				this.messages.slice(0, index - 1)
			)
			this.loadingChange.emit(false)
			if (response.response.length) {
				this.messages[index].text.push(...response.response)
				this.messages[index].additionalInfo.push(response.additional_info || '')
				this.messages[index].index = this.messages[index].text.length - 1
			}
		}
	}

	protected async onQuickQuestion(query: string): Promise<void> {
		if (query && !this.loading) {
			this.loadingChange.emit(true)
			this.messages.push({ text: [query], speaker: 'user', index: 0, additionalInfo: [''] })
			this.scrollToLastMessage()
			const response: Response = await this.modelService.request(
				'single_response',
				query,
				this.messages.slice(0, -1)
			)
			this.loadingChange.emit(false)
			if (response.response.length) {
				this.messages.push({
					text: response.response,
					speaker: 'bot',
					index: 0,
					additionalInfo: [response.additional_info || ''],
				})
				this.scrollToLastMessage()
			}
		}
	}

	private scrollToLastMessage(): void {
		if (this.messagesWrapper) {
			setTimeout(() => {
				this.messagesWrapper!.nativeElement.scrollTo({ top: 99999, behavior: 'smooth' })
			}, 10)
		}
	}
}
