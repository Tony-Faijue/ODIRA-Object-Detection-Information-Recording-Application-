import { Injectable, signal } from '@angular/core';


export interface FileImage{
  image_file_id: string,
  content_type: string,
  file_name: string,
  results: {item:string; count:number; total_count_of_objects:number}[];
  image_url: string;
}

@Injectable({
  providedIn: 'root',
})

export class ImageStateService {
  
  /**
   * Stores the data of the processed image
   */

  processedImage = signal<FileImage | null>(null);

}
