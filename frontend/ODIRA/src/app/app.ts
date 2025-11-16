import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Odira } from './odira/odira';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Odira],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('ODIRA');
}
