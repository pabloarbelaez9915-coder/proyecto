import { HttpClient, provideHttpClient, withInterceptors } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';
import { FirebaseAuthService } from './firebase-auth.service';
import { firebaseAuthInterceptor } from './firebase-auth.interceptor';

describe('firebaseAuthInterceptor', () => {
  let httpTesting: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(withInterceptors([firebaseAuthInterceptor])),
        provideHttpClientTesting(),
        {
          provide: FirebaseAuthService,
          useValue: { getIdToken: async () => 'firebase-id-token' },
        },
      ],
    });
    httpTesting = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTesting.verify();
  });

  it('adds the Firebase ID token to API requests', async () => {
    const result = firstValueFrom(
      TestBed.inject(HttpClient).get(
        'http://127.0.0.1:8000/api/v1/clientes/',
      ),
    );
    await Promise.resolve();

    const request = httpTesting.expectOne('http://127.0.0.1:8000/api/v1/clientes/');
    expect(request.request.headers.get('Authorization')).toBe('Bearer firebase-id-token');
    request.flush([]);
    await result;
  });
});
