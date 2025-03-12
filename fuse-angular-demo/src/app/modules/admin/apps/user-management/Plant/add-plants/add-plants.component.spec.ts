import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddPlantsComponent } from './add-plants.component';

describe('AddPlantsComponent', () => {
  let component: AddPlantsComponent;
  let fixture: ComponentFixture<AddPlantsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddPlantsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddPlantsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
