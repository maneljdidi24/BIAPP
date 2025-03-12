import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DisplayPlantsComponent } from './display-plants.component';

describe('DisplayPlantsComponent', () => {
  let component: DisplayPlantsComponent;
  let fixture: ComponentFixture<DisplayPlantsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DisplayPlantsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DisplayPlantsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
