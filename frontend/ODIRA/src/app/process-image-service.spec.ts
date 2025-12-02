import { TestBed } from '@angular/core/testing';

import { ProcessImageService } from './process-image-service';

describe('ProcessImageService', () => {
  let service: ProcessImageService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ProcessImageService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
