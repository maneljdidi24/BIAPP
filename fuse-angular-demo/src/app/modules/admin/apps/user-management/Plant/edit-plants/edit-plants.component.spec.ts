import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditPlantsComponent } from './edit-plants.component';

describe('EditPlantsComponent', () => {
  let component: EditPlantsComponent;
  let fixture: ComponentFixture<EditPlantsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EditPlantsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EditPlantsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
