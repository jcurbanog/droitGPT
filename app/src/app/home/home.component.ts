import { Component } from '@angular/core'

import { ChatComponent } from './chat/chat.component'
import { HeaderComponent, Mode } from './header/header.component'
import { FormControl, FormGroup } from '@angular/forms'

export interface QueryForm {
	mode: FormControl<Mode>
	input: FormControl<string | null>
}
@Component({
	selector: 'app-home',
	standalone: true,
	templateUrl: './home.component.html',
	styleUrl: './home.component.scss',
	imports: [ChatComponent, HeaderComponent],
})
export class HomeComponent {
	protected mode = new FormControl<Mode>('Single', { nonNullable: true })
	protected inputForm = new FormControl<string | null>('')

	protected form = new FormGroup({
		mode: this.mode,
		input: this.inputForm,
	})
}
