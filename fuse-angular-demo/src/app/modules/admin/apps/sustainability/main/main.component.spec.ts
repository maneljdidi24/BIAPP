import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { MainComponent } from './main.component';

class MockRouter {
  navigateByUrl(url: string): Promise<boolean> {
    // Mock implementation of navigateByUrl that returns a resolved Promise
    return Promise.resolve(true);
  }
}

describe('MainComponent', () => {
  let component: MainComponent;
  let fixture: ComponentFixture<MainComponent>;
  let mockRouter: MockRouter;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MainComponent ],
      providers: [{ provide: Router, useClass: MockRouter }] // Provide the mock router
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MainComponent);
    component = fixture.componentInstance;
    mockRouter = TestBed.inject(Router); // Inject the mock router
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should navigate to the correct URL when click is called', () => {
    spyOn(mockRouter, 'navigateByUrl').and.callThrough(); // Spy on the navigateByUrl method

    component.click(0);
    expect(mockRouter.navigateByUrl).toHaveBeenCalledWith('/sustainability/main/addP');

    component.click(1);
    expect(mockRouter.navigateByUrl).toHaveBeenCalledWith('/sustainability/main/performance');

    component.click(2);
    // Testing the Power BI opening logic
    const url = component.Sutainability; // Access the URL
    const windowOpenSpy = spyOn(window, 'open').and.callThrough();
    component.openPowerBi('Sutainability');

    expect(windowOpenSpy).toHaveBeenCalledWith(url, `powerbi_Sutainability`);
  });

  it('should handle invalid project names in openPowerBi', () => {
    const consoleErrorSpy = spyOn(console, 'error'); // Spy on console.error

    component.openPowerBi('InvalidProject'); // Call with an invalid project name

    expect(consoleErrorSpy).toHaveBeenCalledWith('Invalid project name'); // Check for error
  });
});
