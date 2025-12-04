import { Component, inject } from '@angular/core';
import { WebcamService } from '../webcam-service';
import { ImageStateService, FileImage } from '../image-state-service';
import { ProcessImageService } from '../process-image-service';

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
  processimageService = inject(ProcessImageService);


  imageDataURL!: string;
  imageFileName!: string;


  getImagePreview(){
    this.imageDataURL = this.webcamService.previewImage();
    this.imageFileName = this.webcamService.imageFileName();
  }
  
  processImageResults() {
    this.getImagePreview();
    this.processimageService.uploadFileToServer(this.imageDataURL, this.imageFileName)
    .subscribe({
      next: (result: FileImage) => {
        console.log("Processing complete: ",result);
        //Store the result object in image state service
        this.imageStateService.processedImage.set(result);
      },
      error: (err) => {
        console.error('Upload failed', err);
      },
    });
  }

}
