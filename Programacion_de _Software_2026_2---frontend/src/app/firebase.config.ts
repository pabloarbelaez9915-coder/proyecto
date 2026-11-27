import { FirebaseOptions } from 'firebase/app';

export const FIREBASE_CONFIG: FirebaseOptions = {
  apiKey: 'AIzaSyAeBTR9-Qj4xwhzUdQ5XkCg8tJDneR_fhU',
  authDomain: 'gestion-gimnasio-7a516.firebaseapp.com',
  projectId: 'gestion-gimnasio-7a516',
  appId: '1:889107645386:web:0d2f3286dc04db1bba8533',
};

export function isFirebaseConfigured(): boolean {
  return Object.values(FIREBASE_CONFIG).every(
    (value) => typeof value === 'string' && value.length > 0 && !value.startsWith('REPLACE_'),
  );
}
