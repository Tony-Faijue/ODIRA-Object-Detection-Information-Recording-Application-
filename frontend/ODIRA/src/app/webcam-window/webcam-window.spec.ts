import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WebcamWindow } from './webcam-window';

describe('WebcamWindow', () => {
  let component: WebcamWindow;
  let fixture: ComponentFixture<WebcamWindow>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WebcamWindow]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WebcamWindow);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
