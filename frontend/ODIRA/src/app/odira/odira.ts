import { Component } from '@angular/core';
import { WebcamWindow } from "../webcam-window/webcam-window";
import { Settings } from "../settings/settings";

@Component({
  selector: 'app-odira',
  imports: [WebcamWindow, Settings],
  templateUrl: './odira.html',
  styleUrl: './odira.css',
})
export class Odira {

}
