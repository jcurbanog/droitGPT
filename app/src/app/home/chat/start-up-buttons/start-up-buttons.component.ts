import { CommonModule } from '@angular/common'
import { Component, Input } from '@angular/core'

@Component({
	selector: 'app-start-up-buttons',
	standalone: true,
	imports: [CommonModule],
	templateUrl: './start-up-buttons.component.html',
	styleUrl: './start-up-buttons.component.scss',
})
export class StartUpButtonsComponent {
	@Input({ required: true }) public options!: string[]
}
