import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportAppCardComponent } from './report-app-card.component';

describe('ReportAppCardComponent', () => {
  let component: ReportAppCardComponent;
  let fixture: ComponentFixture<ReportAppCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ReportAppCardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ReportAppCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
