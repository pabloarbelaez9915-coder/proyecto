import { Component, inject, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { FirebaseAuthService } from './firebase-auth.service';

@Component({
  imports: [ReactiveFormsModule],
  selector: 'app-login',
  styleUrl: './login.component.css',
  templateUrl: './login.component.html',
})
export class LoginComponent {
  readonly auth = inject(FirebaseAuthService);

  readonly busy = signal(false);
  readonly errorMessage = signal('');
  readonly form = new FormGroup({
    email: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.email],
    }),
    password: new FormControl('', { nonNullable: true, validators: [Validators.required] }),
  });

  async submit(): Promise<void> {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.busy.set(true);
    this.errorMessage.set('');
    try {
      const { email, password } = this.form.getRawValue();
      await this.auth.signIn(email, password);
    } catch (error) {
      this.errorMessage.set(this.getErrorMessage(error));
    } finally {
      this.busy.set(false);
    }
  }

  private getErrorMessage(error: unknown): string {
    if (!FirebaseAuthService.isFirebaseError(error)) {
      return error instanceof Error ? error.message : 'No fue posible iniciar sesión.';
    }

    switch (error.code) {
      case 'auth/invalid-credential':
      case 'auth/user-not-found':
      case 'auth/wrong-password':
        return 'El correo o la contraseña no son correctos.';
      case 'auth/too-many-requests':
        return 'Se bloquearon temporalmente los intentos. Espera e inténtalo de nuevo.';
      case 'auth/network-request-failed':
        return 'No hay conexión con Firebase. Revisa tu conexión a internet.';
      default:
        return 'Firebase no pudo iniciar sesión. Verifica la configuración y vuelve a intentarlo.';
    }
  }
}
