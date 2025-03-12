import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { io,Socket } from 'socket.io-client';

@Injectable({
  providedIn: 'root'
})
export class SocketService {

  private socket: Socket;

  constructor() {
    this.socket = io('http://localhost:5000'); // Replace with your Flask backend URL
  }
  
  connect() {
    this.socket.connect();
  }

  disconnect() {
    this.socket.disconnect();
  }

  emitEvent(eventName: string, data: any) {
    this.socket.emit(eventName, data);
  }




  sendMessage(message: string): void {
    this.socket.emit('message', message);
  }

  onMessage(): Observable<any> {
    return new Observable((observer) => {
      this.socket.on('message', (data: any) => {
        observer.next(data);
      });
    });
  }
}



