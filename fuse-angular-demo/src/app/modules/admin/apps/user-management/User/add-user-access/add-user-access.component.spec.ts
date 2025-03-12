import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddUserAccessComponent } from './add-user-access.component';

describe('AddUserAccessComponent', () => {
  let component: AddUserAccessComponent;
  let fixture: ComponentFixture<AddUserAccessComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddUserAccessComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddUserAccessComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
