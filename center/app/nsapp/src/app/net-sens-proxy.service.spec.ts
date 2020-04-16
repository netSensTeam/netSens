import { TestBed } from '@angular/core/testing';

import { NetSensProxyService } from './net-sens-proxy.service';

describe('NetSensProxyService', () => {
  let service: NetSensProxyService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NetSensProxyService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
