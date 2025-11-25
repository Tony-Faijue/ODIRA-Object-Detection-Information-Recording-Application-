import { Component, inject } from '@angular/core';
import { WebcamModule } from 'ngx-webcam';
import { WebcamService } from '../webcam-service';

@Component({
  selector: 'app-webcam-window',
  imports: [WebcamModule],
  templateUrl: './webcam-window.html',
  styleUrl: './webcam-window.css',
})
export class WebcamWindow{
  //Inject Webcam Service
  webcamService = inject(WebcamService);

  public toggleCamera(){
    this.webcamService.toggleWebCam();
    if(this.webcamService.showWebcam()){
      this.webcamService.initializeCameras();
    }
  }

}
