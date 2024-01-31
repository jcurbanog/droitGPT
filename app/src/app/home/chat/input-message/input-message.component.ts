import { Component, DestroyRef, ElementRef, inject, Input, ViewChild } from '@angular/core'
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
	@ViewChild('wrapper') private wrapper?: ElementRef
	@ViewChild('textArea') private textArea?: ElementRef<HTMLTextAreaElement>

	@Input({ required: true }) public inputForm!: FormControl<string | null>

	private destroyRef = inject(DestroyRef)

	public ngAfterViewInit(): void {
		this.setWrapperValue('')
		this.setTextAreaValue('')
		this.inputForm.valueChanges.pipe(takeUntilDestroyed(this.destroyRef)).subscribe((value) => {
			const newValue = value || ''
			this.setWrapperValue(newValue)
			this.setTextAreaValue(newValue)
		})
	}

	protected inputChanged(): void {
		const newValue = this.textArea?.nativeElement.value || ''
		this.inputForm.setValue(newValue, { emitEvent: false })
		this.setWrapperValue(newValue)
	}

	private setWrapperValue(val: string): void {
		if (this.wrapper) {
			this.wrapper.nativeElement.dataset.replicatedValue = val
		}
	}

	private setTextAreaValue(val: string): void {
		if (this.textArea) {
			this.textArea.nativeElement.value = val
		}
	}
}
