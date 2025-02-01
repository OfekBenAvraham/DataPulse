import { Injectable, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { io, Socket } from 'socket.io-client';

@Injectable({
  providedIn: 'root',
})
export class SocketService {
  private socket: Socket | undefined;
  private apiUrl = 'http://127.0.0.1:8001';

  constructor() {
    this.initializeSocket();
  }
  
  private initializeSocket(): void {
    if (this.socket && this.socket.connected) {
      console.log('Socket already initialized and connected:', this.socket);
      return;
    }
  
    try {
      this.socket = io(this.apiUrl, {
        transports: ['websocket', 'polling'], // Ensure proper transport
        reconnection: true, // Enable reconnection
      });
      console.log('Socket initialized successfully:', this.socket);
  
      this.socket.on('connect', () => {
        console.log('Socket connected');
      });
  
      this.socket.on('disconnect', () => {
        console.warn('Socket disconnected. Attempting to reconnect...');
      });
    } catch (error) {
      console.error('Error initializing socket:', error);
    }
  }

  listen(eventName: string): Observable<any> {
    return new Observable((subscriber) => {
      if (!this.socket) {
        console.error('Socket not initialized. Retrying...');
        this.initializeSocket(); // Attempt to reinitialize the socket
      }

      this.socket?.on(eventName, (data) => {
        console.log(`Received event ${eventName}:`, data);
        subscriber.next(data);
      });

      // Cleanup the subscription
      return () => {
        this.socket?.off(eventName);
      };
    });
  }

  emit(eventName: string, data: any): void {
    if (!this.socket) {
      console.error('Socket not initialized. Cannot emit events.');
      return;
    }
    this.socket.emit(eventName, data);
  }
}
