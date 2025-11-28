import { Component, inject } from '@angular/core';
import { WebcamService } from '../webcam-service';
import { ImageStateService } from '../image-state-service';

@Component({
  selector: 'app-image-preview',
  imports: [],
  templateUrl: './image-preview.html',
  styleUrl: './image-preview.css',
})
export class ImagePreview {

  //Services Injected
  webcamService = inject(WebcamService);
  imageStateService = inject(ImageStateService);

  imageDataURL!: string;
  imageFileName!: string;

  getImagePreview(){
    this.imageDataURL = this.webcamService.previewImage();
    this.imageFileName = this.webcamService.imageFileName();
  }
  
}
