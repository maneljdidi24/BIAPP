import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AddPerformanceComponent } from './add-performance.component';
import { DataService } from 'app/service.service';
import { NotificationService } from 'app/services/notification.service';
import { FuseConfirmationService } from '@fuse/services/confirmation';
import { of } from 'rxjs';

describe('AddPerformanceComponent', () => {
  let component: AddPerformanceComponent;
  let fixture: ComponentFixture<AddPerformanceComponent>;
  let dataServiceSpy: jasmine.SpyObj<DataService>;
  let notificationServiceSpy: jasmine.SpyObj<NotificationService>;

  beforeEach(async () => {
    const dataServiceMock = jasmine.createSpyObj('DataService', ['LoadPerformances']);
    const notificationServiceMock = jasmine.createSpyObj('NotificationService', ['showAlert']);
    
    await TestBed.configureTestingModule({
      declarations: [AddPerformanceComponent],
      providers: [
        { provide: DataService, useValue: dataServiceMock },
        { provide: NotificationService, useValue: notificationServiceMock },
        FuseConfirmationService // Provide any additional services if needed
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(AddPerformanceComponent);
    component = fixture.componentInstance;

    dataServiceSpy = TestBed.inject(DataService) as jasmine.SpyObj<DataService>;
    notificationServiceSpy = TestBed.inject(NotificationService) as jasmine.SpyObj<NotificationService>;
    
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should call loaddata when all required fields are selected', () => {
    // Mock valid data
    component.month = 'January';
    component.year = 2024;
    component.plant = 'Plant1';
    component.topic = 'Topic1';

    spyOn(component, 'LoadPerformances');
    spyOn(component, 'transformDateFromMonthYear').and.returnValue('01-2024');

    component.loaddata();

    expect(component.functiondisplayfordescription).toHaveBeenCalled();
    expect(component.LoadPerformances).toHaveBeenCalledWith({
      date: '01-2024',
      ID_Target: 'Plant12024'
    });
  });

  it('should display alert when month, plant, or topic is missing', () => {
    // Mock data where some fields are missing
    component.month = null;
    component.year = 2024;
    component.plant = 'Plant1';
    component.topic = 'Topic1';

    component.loaddata();

    expect(notificationServiceSpy.error("error here in tresy")).toHaveBeenCalledWith(
      'info',
      'Please select all informations before proceeding.',
      'Missing Information'
    );
  });

  it('should reset data when data is already loaded', () => {
    component.loaded = true;
    spyOn(component, 'onCancelDataChange');

    component.loaddata();

    expect(component.onCancelDataChange).toHaveBeenCalled();
  });
});

