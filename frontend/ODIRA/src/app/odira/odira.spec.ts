import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Odira } from './odira';

describe('Odira', () => {
  let component: Odira;
  let fixture: ComponentFixture<Odira>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Odira]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Odira);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
