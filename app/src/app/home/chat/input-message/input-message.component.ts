import { Component, ElementRef, HostBinding, ViewChild } from '@angular/core'

@Component({
	selector: 'app-input-message',
	standalone: true,
	imports: [],
	templateUrl: './input-message.component.html',
	styleUrl: './input-message.component.scss',
})
export class InputMessageComponent {
	@ViewChild('inputContainer') private input?: ElementRef
	@HostBinding('style.--max-width-message-input') private maxInputWidth!: string

	public ngAfterViewInit(): void {
		this.maxInputWidth = `${this.input?.nativeElement.offsetWidth ?? 500}px`
	}
}
