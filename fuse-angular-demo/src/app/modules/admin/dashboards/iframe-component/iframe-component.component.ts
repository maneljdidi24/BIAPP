import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-iframe-component',
  templateUrl: './iframe-component.component.html',
  styleUrls: ['./iframe-component.component.scss']
})
export class IframeComponentComponent  {

  @Input() src: string;
  @Input() width: string;
  @Input() height: string;

}
