import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-report-app-card',
  templateUrl: './report-app-card.component.html',
  styleUrls: ['./report-app-card.component.scss']
})
export class ReportAppCardComponent {
  @Input() title: string;
  @Input() description: string;
  @Input() icon: string;
  @Input() disabled: boolean;
  @Output() buttonClicked: EventEmitter<void> = new EventEmitter<void>();

  onClick(): void {
    if (!this.disabled) {
      this.buttonClicked.emit();
    }
  }
}