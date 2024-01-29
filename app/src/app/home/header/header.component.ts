import { Component, Input } from '@angular/core'
import { FormGroup, ReactiveFormsModule } from '@angular/forms'
import { QueryForm } from '../home.component'

export type Mode = 'Single' | 'Multiple' | 'Test'

@Component({
	selector: 'app-header',
	standalone: true,
	imports: [ReactiveFormsModule],
	templateUrl: './header.component.html',
	styleUrl: './header.component.scss',
})
export class HeaderComponent {
	@Input({ required: true }) public form!: FormGroup<QueryForm>

	protected options: Mode[] = ['Single', 'Multiple', 'Test']
}
