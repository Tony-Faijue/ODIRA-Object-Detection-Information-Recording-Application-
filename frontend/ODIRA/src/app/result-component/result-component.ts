import { Component, inject, computed } from '@angular/core';
import { ImageStateService } from '../image-state-service';

@Component({
  selector: 'app-result-component',
  imports: [],
  templateUrl: './result-component.html',
  styleUrl: './result-component.css',
})
export class ResultComponent {
  
  imageStateService = inject(ImageStateService);

  processedImageUrl = computed(() => this.imageStateService.processedImage()?.image_url || null);
  resultsList = computed(() => this.imageStateService.processedImage()?.results || []);
  
}
