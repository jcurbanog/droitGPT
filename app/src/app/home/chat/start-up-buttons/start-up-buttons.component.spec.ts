import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StartUpButtonsComponent } from './start-up-buttons.component';

describe('StartUpButtonsComponent', () => {
  let component: StartUpButtonsComponent;
  let fixture: ComponentFixture<StartUpButtonsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StartUpButtonsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(StartUpButtonsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
