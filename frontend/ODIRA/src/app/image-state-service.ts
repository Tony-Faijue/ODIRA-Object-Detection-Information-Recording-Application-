import { Injectable, signal } from '@angular/core';


export interface FileImage{
  image_file_id: number,
  content_type: string,
  file_name: string,
  results: Record<string, number>,
}

@Injectable({
  providedIn: 'root',
})

export class ImageStateService {
  
  /**
   * Stores the data of the processed image
   */

  processedImage = signal<FileImage>({
    image_file_id: 0,
    content_type: "",
    file_name: "",
    results: {},
  });

}
