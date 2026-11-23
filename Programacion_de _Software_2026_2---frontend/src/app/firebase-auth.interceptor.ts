import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { from, switchMap } from 'rxjs';
import { FirebaseAuthService } from './firebase-auth.service';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const firebaseAuthInterceptor: HttpInterceptorFn = (request, next) => {
  if (!request.url.startsWith(API_BASE_URL)) {
    return next(request);
  }

  const auth = inject(FirebaseAuthService);
  return from(auth.getIdToken()).pipe(
    switchMap((token) =>
      next(
        token
          ? request.clone({ setHeaders: { Authorization: `Bearer ${token}` } })
          : request,
      ),
    ),
  );
};
