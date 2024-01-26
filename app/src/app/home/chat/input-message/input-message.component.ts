import { Component, DestroyRef, ElementRef, HostBinding, inject, Input, ViewChild } from '@angular/core'
import { takeUntilDestroyed } from '@angular/core/rxjs-interop'
import { FormControl } from '@angular/forms'

@Component({
	selector: 'app-input-message',
	standalone: true,
	imports: [],
	templateUrl: './input-message.component.html',
	styleUrl: './input-message.component.scss',
})
export class InputMessageComponent {
	@ViewChild('inputContainer') private input?: ElementRef
	@ViewChild('wrapper') private wrapper?: ElementRef
	@ViewChild('textArea') private textArea?: ElementRef<HTMLTextAreaElement>

	@HostBinding('style.--max-width-message-input') private maxInputWidth!: string

	@Input({ required: true }) public inputForm!: FormControl<string | null>

	private destroyRef = inject(DestroyRef)

	public ngAfterViewInit(): void {
		this.maxInputWidth = `${this.input?.nativeElement.offsetWidth ?? 500}px`
		this.inputForm.valueChanges.pipe(takeUntilDestroyed(this.destroyRef)).subscribe((value) => {
			const newValue = value || ''
			if (this.wrapper) {
				this.wrapper.nativeElement.dataset.replicatedValue = newValue
			}
			if (this.textArea) {
				this.textArea.nativeElement.value = newValue
			}
		})
	}

	protected inputChanged(): void {
		console.log('inputChanged')
		const newValue = this.textArea?.nativeElement.value || ''
		this.inputForm.setValue(newValue, { emitEvent: false })
		if (this.wrapper) {
			this.wrapper.nativeElement.dataset.replicatedValue = newValue
		}
	}
}
