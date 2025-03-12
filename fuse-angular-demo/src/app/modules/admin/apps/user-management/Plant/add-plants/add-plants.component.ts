import { Component, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'app-add-plants',
  templateUrl: './add-plants.component.html',
  styleUrls: ['./add-plants.component.scss']
})
export class AddPlantsComponent implements OnInit {

  composeForm: FormGroup;

  constructor() { }

  ngOnInit(): void {
  }

  saveAndClose(){

  }

  send() {
  }

  discard(){}
  toggleAllSelection(){}
}
