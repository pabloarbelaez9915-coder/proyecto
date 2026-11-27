import { Injectable, signal } from '@angular/core';
import { FirebaseError, getApp, getApps, initializeApp } from 'firebase/app';
import {
  getAuth,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signOut,
} from 'firebase/auth';
import type { Auth, User } from 'firebase/auth';
import { FIREBASE_CONFIG, isFirebaseConfigured } from './firebase.config';

let firebaseAuth: Auth | undefined;

function getFirebaseAuth(): Auth {
  if (!isFirebaseConfigured()) {
    throw new Error('Configura Firebase en src/app/firebase.config.ts antes de iniciar sesión.');
  }

  if (!firebaseAuth) {
    const app = getApps().length > 0 ? getApp() : initializeApp(FIREBASE_CONFIG);
    firebaseAuth = getAuth(app);
  }

  return firebaseAuth;
}

@Injectable({ providedIn: 'root' })
export class FirebaseAuthService {
  readonly user = signal<User | null>(null);
  readonly authReady = signal(false);
  readonly authError = signal('');

  constructor() {
    if (!isFirebaseConfigured()) {
      this.authReady.set(true);
      return;
    }

    onAuthStateChanged(
      getFirebaseAuth(),
      (user) => {
        this.user.set(user);
        this.authReady.set(true);
      },
      (error) => {
        this.user.set(null);
        this.authError.set(error.message);
        this.authReady.set(true);
      },
    );
  }

  isConfigured(): boolean {
    return isFirebaseConfigured();
  }

  async signIn(email: string, password: string): Promise<void> {
    await signInWithEmailAndPassword(getFirebaseAuth(), email, password);
  }

  async signOut(): Promise<void> {
    await signOut(getFirebaseAuth());
  }

  async getIdToken(): Promise<string | null> {
    const user = this.user();
    return user ? user.getIdToken() : null;
  }

  static isFirebaseError(error: unknown): error is FirebaseError {
    return error instanceof FirebaseError;
  }
}
