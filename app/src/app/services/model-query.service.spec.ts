import { TestBed } from '@angular/core/testing';

import { ModelQueryService } from './model-query.service';

describe('ModelQueryService', () => {
  let service: ModelQueryService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ModelQueryService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
