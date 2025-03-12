import { Component, OnInit , Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-modal-window',
  templateUrl: './modal-window.component.html',
  styleUrls: ['./modal-window.component.scss']
})
export class ModalWindowComponent implements OnInit {

  constructor(private dialogRef: MatDialogRef<ModalWindowComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any) { }

    displayedColumns:any[]
  columnVisibility:any[]
  panelOpenState = false;
  ngOnInit(): void {
    this.displayedColumns = this.data.displayedColumns
    this.columnVisibility = this.data.columnVisibility
  }

  toggleColumnVisibility(column) {
    const columnDef = this.columnVisibility.find((col) => col.columnName === column);
    if (columnDef) {
      const index = this.displayedColumns.indexOf(columnDef.columnName);
      if (index !== -1) {
        // Remove the column if it exists in the displayedColumns array
        this.displayedColumns.splice(index, 1);
      } else {  
        // Insert the column at the desired position in the displayedColumns array
        const insertIndex = 2; // Specify the desired position here
        this.displayedColumns.splice(columnDef.where, 0, columnDef.columnName);
      }
    }
  }
    // Set a flag to control the visibility of the modal window
    isModalOpen: boolean = false;

    // Method to open the modal window
    openModal() {
      this.isModalOpen = true;
    }
  
    // Method to close the modal window
    closeModal() {
      this.isModalOpen = false;
    }

    d: any
    onSelect(): void {
      this.d={
        displayedColumns: this.displayedColumns,
        columnVisibility:this.columnVisibility
      }
      // Emit the selected item back to the parent component
      // (in this case, the DisplayComponent)
      this.dialogRef.close(this.d);
    }

}
