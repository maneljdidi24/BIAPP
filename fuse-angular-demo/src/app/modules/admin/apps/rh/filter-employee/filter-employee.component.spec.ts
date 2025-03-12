import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FilterEmployeeComponent } from './filter-employee.component';

describe('FilterEmployeeComponent', () => {
  let component: FilterEmployeeComponent;
  let fixture: ComponentFixture<FilterEmployeeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FilterEmployeeComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FilterEmployeeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
