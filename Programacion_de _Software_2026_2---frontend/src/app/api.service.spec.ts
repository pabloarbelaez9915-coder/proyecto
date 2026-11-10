import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { ApiService } from './api.service';

describe('ApiService', () => {
  let api: ApiService;
  let httpTesting: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ApiService, provideHttpClient(), provideHttpClientTesting()],
    });
    api = TestBed.inject(ApiService);
    httpTesting = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTesting.verify();
  });

  it('uses the local API for collection, item, create, update and delete requests', () => {
    api.list('clientes').subscribe();
    const listRequest = httpTesting.expectOne('http://127.0.0.1:8000/api/v1/clientes/');
    expect(listRequest.request.method).toBe('GET');
    listRequest.flush([]);

    api.get('clientes', 'cliente-123').subscribe();
    const getRequest = httpTesting.expectOne('http://127.0.0.1:8000/api/v1/clientes/cliente-123');
    expect(getRequest.request.method).toBe('GET');
    getRequest.flush({ id_cliente: 'cliente-123' });

    const payload = { primer_nombre: 'Ana' };
    api.create('clientes', payload).subscribe();
    const createRequest = httpTesting.expectOne('http://127.0.0.1:8000/api/v1/clientes/');
    expect(createRequest.request.method).toBe('POST');
    expect(createRequest.request.body).toEqual(payload);
    createRequest.flush({ id_cliente: 'cliente-123' });

    api.update('clientes', 'cliente-123', payload).subscribe();
    const updateRequest = httpTesting.expectOne(
      'http://127.0.0.1:8000/api/v1/clientes/cliente-123',
    );
    expect(updateRequest.request.method).toBe('PUT');
    expect(updateRequest.request.body).toEqual(payload);
    updateRequest.flush({ id_cliente: 'cliente-123' });

    api.delete('clientes', 'cliente-123').subscribe();
    const deleteRequest = httpTesting.expectOne(
      'http://127.0.0.1:8000/api/v1/clientes/cliente-123',
    );
    expect(deleteRequest.request.method).toBe('DELETE');
    deleteRequest.flush(null, { status: 204, statusText: 'No Content' });
  });
});
