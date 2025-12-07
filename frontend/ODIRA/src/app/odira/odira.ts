import { Component } from '@angular/core';
import { WebcamWindow } from "../webcam-window/webcam-window";
import { Settings } from "../settings/settings";
import { UploadImage } from "../upload-image/upload-image";
import { ImagePreview } from "../image-preview/image-preview";
import { ResultComponent } from '../result-component/result-component';
import { RouterLink } from "@angular/router";

@Component({
  selector: 'app-odira',
  imports: [WebcamWindow, Settings, UploadImage, ImagePreview, ResultComponent, RouterLink],
  templateUrl: './odira.html',
  styleUrl: './odira.css',
})
export class Odira {

}
