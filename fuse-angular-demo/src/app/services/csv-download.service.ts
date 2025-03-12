import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root' // This makes the service available application-wide
})
export class CsvDownloadService {
  
  downloadCsv(data: any[], filename: string): void {
    const csvString = this.convertToCsv(data);
    const blob = new Blob([csvString], { type: 'text/csv' });
    const link = document.createElement('a');
    link.style.display = 'none';
    link.href = window.URL.createObjectURL(blob);
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  private convertToCsv(data: any[]): string {
    const csvRows = [];
    const headers = Object.keys(data[0]);
    csvRows.push(headers.join(','));
    data.forEach(item => {
      const values = headers.map(header => this.escapeCsvValue(item[header]));
      csvRows.push(values.join(','));
    });
    return csvRows.join('\n');
  }

  private escapeCsvValue(value: any): string {
    if (/[",\n]/.test(value)) {
      return '"' + value.replace(/"/g, '""') + '"';
    }
    return value;
  }
}
