import { Component } from '@angular/core';

import { ChatComponent } from './chat/chat.component';
import { HeaderComponent } from './header/header.component';

@Component({
	selector: 'app-home',
	standalone: true,
	templateUrl: './home.component.html',
	styleUrl: './home.component.scss',
	imports: [ChatComponent, HeaderComponent],
})
export class HomeComponent {}
