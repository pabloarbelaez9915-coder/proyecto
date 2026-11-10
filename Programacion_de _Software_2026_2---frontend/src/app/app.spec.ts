import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { App } from './app';

describe('App', () => {
  let httpTesting: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();
    httpTesting = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTesting.verify();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    httpTesting.expectOne('http://127.0.0.1:8000/api/v1/clientes/').flush([]);
    expect(fixture.componentInstance).toBeTruthy();
  });

  it('should render the customer module with a collapsible navigation', async () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    httpTesting.expectOne('http://127.0.0.1:8000/api/v1/clientes/').flush([]);
    await fixture.whenStable();
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('Clientes');
    expect(compiled.querySelectorAll('.nav-item').length).toBe(10);

    compiled.querySelector<HTMLButtonElement>('[aria-label="Contraer menú"]')?.click();
    fixture.detectChanges();
    expect(compiled.querySelector('.app-shell')?.classList.contains('is-collapsed')).toBe(true);

    const membershipsButton = compiled.querySelector<HTMLButtonElement>(
      '[aria-label="Membresías"]',
    );
    expect(membershipsButton?.textContent).not.toContain('Membresías');
    membershipsButton?.click();
    const membershipsRequest = httpTesting.expectOne('http://127.0.0.1:8000/api/v1/membresias/');
    membershipsRequest.flush([]);
    await fixture.whenStable();
    fixture.detectChanges();

    expect(compiled.querySelector('h1')?.textContent).toContain('Membresías');
    expect(compiled.querySelector('[aria-label="Membresías"]')?.getAttribute('aria-current')).toBe(
      'page',
    );
    expect(compiled.querySelector('.app-shell')?.classList.contains('is-collapsed')).toBe(true);

    const expandButton = compiled.querySelector<HTMLButtonElement>('[aria-label="Expandir menú"]');
    expect(expandButton).toBeTruthy();
    expandButton?.click();
    fixture.detectChanges();

    expect(compiled.querySelector('.app-shell')?.classList.contains('is-collapsed')).toBe(false);
    expect(compiled.querySelector('[aria-label="Membresías"] .nav-label')?.textContent).toContain(
      'Membresías',
    );
  });

  it('keeps the expand control available when the narrow layout starts collapsed', async () => {
    const originalWidth = Object.getOwnPropertyDescriptor(window, 'innerWidth');
    Object.defineProperty(window, 'innerWidth', { configurable: true, value: 390 });
    try {
      const fixture = TestBed.createComponent(App);
      fixture.detectChanges();
      httpTesting.expectOne('http://127.0.0.1:8000/api/v1/clientes/').flush([]);
      await fixture.whenStable();
      fixture.detectChanges();

      const compiled = fixture.nativeElement as HTMLElement;
      expect(compiled.querySelector('.app-shell')?.classList.contains('is-collapsed')).toBe(true);
      expect(compiled.querySelector('[aria-label="Expandir menú"]')).toBeTruthy();
      expect(compiled.querySelector('[aria-label="Clientes"]')?.classList.contains('active')).toBe(
        true,
      );
    } finally {
      if (originalWidth) {
        Object.defineProperty(window, 'innerWidth', originalWidth);
      }
    }
  });

  it('adds a created record from the API response without a second list request', async () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    httpTesting.expectOne('http://127.0.0.1:8000/api/v1/clientes/').flush([]);
    await fixture.whenStable();

    const app = fixture.componentInstance;
    app.openCreateForm();
    app.form.controls['primer_nombre'].setValue('Lucía');
    app.form.controls['primer_apellido'].setValue('Gómez');
    app.form.controls['correo'].setValue('lucia@example.com');
    app.form.controls['clave'].setValue('secreto');

    const savePromise = app.saveRecord();
    const createRequest = httpTesting.expectOne('http://127.0.0.1:8000/api/v1/clientes/');
    expect(createRequest.request.method).toBe('POST');
    createRequest.flush({
      id_cliente: 'cliente-456',
      primer_nombre: 'Lucía',
      primer_apellido: 'Gómez',
      correo: 'lucia@example.com',
      segundo_nombre: null,
      segundo_apellido: null,
      telefono: null,
      id_membresia: null,
      activo: true,
    });
    await savePromise;

    expect(app.records()).toHaveLength(1);
    expect(app.records()[0]['id_cliente']).toBe('cliente-456');
    expect(app.formOpen()).toBe(false);
  });
});
