import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { WebcamService } from './webcam-service';
import { FileImage } from './image-state-service';
import { Observable } from 'rxjs';
import { SettingsData, SettingsService } from './settings-service';

@Injectable({
  providedIn: 'root',
})
export class ProcessImageService {
  //inject HTTPClient and Webcam Services
  http = inject(HttpClient);
  webcamService = inject(WebcamService);
  settingsService = inject(SettingsService);

  //Placeholder api endpoint
  private FILE_URL = "http://127.0.0.1:9998/api/process-image";


  /**
  *  Upload the file image to the POST URI endpoint, to process the image on the server
  * @param file 
  * @returns 
  */
  uploadFileToServer(dataUrl: string, filename: string): Observable<FileImage>{
    const file = this.dataURLToFile(dataUrl, filename);
    const formData = new FormData();
    formData.append('file', file, file.name);
    //Append the settings data to form data
    const currentSettings: SettingsData = this.settingsService.currentSettingsSnapshot();
    formData.append('settings', JSON.stringify(currentSettings));

    //Select the corresponding api url based of file or webcam image
    const url = this.FILE_URL;
    return this.http.post<FileImage>(url, formData);
 }

   /**
  * Function to convert image data url to a file object to be processed on the server
  * @param dataUrl 
  * @param filename 
  * @returns a file object
  */
 dataURLToFile(dataUrl: string, filename:string):File{
  // Sources Used to handle decoding base64 to binary string

  // https://www.geeksforgeeks.org/javascript/how-to-convert-base64-to-file-in-javascript/
  // https://www.digitalocean.com/community/tutorials/how-to-encode-and-decode-strings-with-base64-in-javascript


  //For the allowes file types
  const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png'];

  //Split data url into metadata
  const [header, base64] = dataUrl.split(",");
  //Extract MIME Type
  const mimeMatch = header.match(/data:(.+);base64/);
  const mime = mimeMatch ? mimeMatch[1] : '';

  //Validate against the allowed type
  if(!ALLOWED_MIME_TYPES.includes(mime)){
    throw new Error(`Unsupported MIME type: ${mime}`);
  }

  //Decode base64 to a binary string
  const binary = atob(base64);
  //Build Uint8Array for raw bytes
  const array = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++){
    array[i] = binary.charCodeAt(i);
  }

  //Add filename with extension if not included
  const ext = mime.split('/')[1];
  const validFileName = filename.includes('.') ? filename : `${filename}.${ext}`;
  
  //Return the file object
  return new File([array], validFileName, {type: mime});
 }
}
