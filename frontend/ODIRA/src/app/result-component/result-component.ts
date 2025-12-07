import { Component, inject, computed } from '@angular/core';
import { ImageStateService } from '../image-state-service';
import { RouterLink } from "@angular/router";

@Component({
  selector: 'app-result-component',
  imports: [RouterLink],
  templateUrl: './result-component.html',
  styleUrl: './result-component.css',
})
export class ResultComponent {
  
  imageStateService = inject(ImageStateService);

  //Get data from image state service after processing the image on the server
  processedImageUrl = computed(() => this.imageStateService.processedImage()?.image_url || null);
  resultsList = computed(() => this.imageStateService.processedImage()?.results || []);
  
}
