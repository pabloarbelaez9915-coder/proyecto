import { HttpErrorResponse } from '@angular/common/http';
import { Component, computed, inject, signal } from '@angular/core';
import {
  FormControl,
  FormRecord,
  ReactiveFormsModule,
  ValidatorFn,
  Validators,
} from '@angular/forms';
import { firstValueFrom } from 'rxjs';
import { ApiService } from './api.service';
import { ENTITIES, EntityDefinition, FieldDefinition } from './entity.config';

type FormValue = string | number | boolean | null;
type RecordData = Record<string, unknown>;
type Notice = { kind: 'success' | 'error'; message: string };
type FormMode = 'create' | 'edit';

@Component({
  imports: [ReactiveFormsModule],
  selector: 'app-root',
  styleUrl: './app.css',
  templateUrl: './app.html',
})
export class App {
  private readonly api = inject(ApiService);

  readonly entities = ENTITIES;
  readonly selectedEntity = signal<EntityDefinition>(ENTITIES[3]);
  readonly records = signal<RecordData[]>([]);
  readonly loading = signal(false);
  readonly saving = signal(false);
  readonly sidebarCollapsed = signal(typeof window !== 'undefined' && window.innerWidth <= 760);
  readonly searchText = signal('');
  readonly notice = signal<Notice | null>(null);
  readonly formOpen = signal(false);
  readonly formMode = signal<FormMode>('create');
  readonly selectedRecord = signal<RecordData | null>(null);
  readonly detailRecord = signal<RecordData | null>(null);
  readonly form = new FormRecord<FormControl<FormValue>>({});

  readonly columns = computed(() => [
    this.selectedEntity().idField,
    ...this.selectedEntity().displayFields,
  ]);

  readonly visibleRecords = computed(() => {
    const query = this.searchText().trim().toLocaleLowerCase();
    if (!query) {
      return this.records();
    }

    return this.records().filter((record) =>
      this.columns().some((key) =>
        String(record[key] ?? '')
          .toLocaleLowerCase()
          .includes(query),
      ),
    );
  });

  constructor() {
    void this.loadRecords();
  }

  selectEntity(entity: EntityDefinition): void {
    this.selectedEntity.set(entity);
    this.searchText.set('');
    this.notice.set(null);
    this.formOpen.set(false);
    this.detailRecord.set(null);
    this.selectedRecord.set(null);
    void this.loadRecords();
  }

  toggleSidebar(): void {
    this.sidebarCollapsed.update((collapsed) => !collapsed);
  }

  updateSearch(event: Event): void {
    if (event.target instanceof HTMLInputElement) {
      this.searchText.set(event.target.value);
    }
  }

  async loadRecords(): Promise<void> {
    const endpoint = this.selectedEntity().endpoint;
    this.loading.set(true);
    try {
      const result = await firstValueFrom(this.api.list<RecordData>(endpoint));
      if (this.selectedEntity().endpoint === endpoint) {
        this.records.set(result);
      }
    } catch (error) {
      if (this.selectedEntity().endpoint === endpoint) {
        this.records.set([]);
        this.showError(error);
      }
    } finally {
      if (this.selectedEntity().endpoint === endpoint) {
        this.loading.set(false);
      }
    }
  }

  async lookupById(id: string): Promise<void> {
    const normalizedId = id.trim();
    if (!normalizedId) {
      return;
    }

    const entity = this.selectedEntity();
    try {
      const record = await firstValueFrom(this.api.get<RecordData>(entity.endpoint, normalizedId));
      if (this.selectedEntity().endpoint !== entity.endpoint) {
        return;
      }
      this.detailRecord.set(record);
      this.selectedRecord.set(record);
      this.formOpen.set(true);
      this.notice.set(null);
    } catch (error) {
      this.showError(error);
    }
  }

  openCreateForm(): void {
    this.formMode.set('create');
    this.selectedRecord.set(null);
    this.detailRecord.set(null);
    this.buildForm(null);
    this.formOpen.set(true);
  }

  async openDetails(record: RecordData): Promise<void> {
    const entity = this.selectedEntity();
    const id = String(record[entity.idField] ?? '');
    try {
      const freshRecord = await firstValueFrom(this.api.get<RecordData>(entity.endpoint, id));
      if (this.selectedEntity().endpoint !== entity.endpoint) {
        return;
      }
      this.selectedRecord.set(freshRecord);
      this.detailRecord.set(freshRecord);
      this.formOpen.set(true);
    } catch (error) {
      this.showError(error);
    }
  }

  async openEditForm(record: RecordData): Promise<void> {
    const entity = this.selectedEntity();
    const id = String(record[entity.idField] ?? '');
    try {
      const freshRecord = await firstValueFrom(this.api.get<RecordData>(entity.endpoint, id));
      if (this.selectedEntity().endpoint !== entity.endpoint) {
        return;
      }
      this.formMode.set('edit');
      this.selectedRecord.set(freshRecord);
      this.detailRecord.set(null);
      this.buildForm(freshRecord);
      this.formOpen.set(true);
    } catch (error) {
      this.showError(error);
    }
  }

  async saveRecord(): Promise<void> {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.saving.set(true);
    const entity = this.selectedEntity();
    const formMode = this.formMode();
    const payload = this.buildPayload(entity.fields);
    try {
      let savedRecord: RecordData;
      if (formMode === 'create') {
        savedRecord = await firstValueFrom(this.api.create<RecordData>(entity.endpoint, payload));
      } else {
        const id = String(this.selectedRecord()?.[entity.idField] ?? '');
        savedRecord = await firstValueFrom(
          this.api.update<RecordData>(entity.endpoint, id, payload),
        );
      }

      if (this.selectedEntity().endpoint !== entity.endpoint) {
        return;
      }
      this.upsertRecord(entity, savedRecord);
      this.formOpen.set(false);
      this.notice.set({
        kind: 'success',
        message:
          formMode === 'create'
            ? `${entity.singular} creado correctamente.`
            : `${entity.singular} actualizado correctamente.`,
      });
    } catch (error) {
      this.showError(error);
    } finally {
      this.saving.set(false);
    }
  }

  async deleteRecord(record: RecordData): Promise<void> {
    const entity = this.selectedEntity();
    const id = String(record[entity.idField] ?? '');
    if (!window.confirm(`¿Eliminar este registro de ${entity.label.toLocaleLowerCase()}?`)) {
      return;
    }

    try {
      await firstValueFrom(this.api.delete(entity.endpoint, id));
      if (this.selectedEntity().endpoint !== entity.endpoint) {
        return;
      }
      this.records.update((records) =>
        records.filter((item) => String(item[entity.idField] ?? '') !== id),
      );
      this.notice.set({
        kind: 'success',
        message: `${entity.singular} eliminado correctamente.`,
      });
    } catch (error) {
      this.showError(error);
    }
  }

  closeDialog(): void {
    this.formOpen.set(false);
    this.detailRecord.set(null);
    this.selectedRecord.set(null);
  }

  switchDetailToEdit(): void {
    const record = this.selectedRecord();
    if (!record) {
      return;
    }

    this.formMode.set('edit');
    this.detailRecord.set(null);
    this.buildForm(record);
  }

  fieldLabel(key: string): string {
    if (key === this.selectedEntity().idField) {
      return 'ID del registro';
    }
    return this.selectedEntity().fields.find((field) => field.key === key)?.label ?? key;
  }

  fieldValue(record: RecordData, key: string): unknown {
    return record[key];
  }

  displayValue(value: unknown): string {
    if (value === null || value === undefined || value === '') {
      return '—';
    }
    if (typeof value === 'boolean') {
      return value ? 'Activo' : 'Inactivo';
    }
    return String(value);
  }

  isBooleanField(key: string): boolean {
    return this.selectedEntity().fields.find((field) => field.key === key)?.type === 'checkbox';
  }

  hasError(field: FieldDefinition): boolean {
    const control = this.form.controls[field.key];
    return Boolean(control && control.invalid && (control.touched || control.dirty));
  }

  private buildForm(record: RecordData | null): void {
    for (const key of Object.keys(this.form.controls)) {
      this.form.removeControl(key);
    }

    for (const field of this.selectedEntity().fields) {
      const recordValue = record?.[field.key];
      const initialValue =
        field.type === 'checkbox'
          ? (recordValue ?? true)
          : field.type === 'password'
            ? ''
            : (recordValue ?? '');
      const validators: ValidatorFn[] = [];
      const required =
        this.formMode() === 'create' ? field.required : (field.requiredOnEdit ?? field.required);
      if (required) {
        validators.push(Validators.required);
      }
      if (field.type === 'email') {
        validators.push(Validators.email);
      }
      if (field.maxLength) {
        validators.push(Validators.maxLength(field.maxLength));
      }
      this.form.addControl(
        field.key,
        new FormControl<FormValue>(this.toFormValue(initialValue), validators),
      );
    }
  }

  private buildPayload(fields: FieldDefinition[]): Record<string, unknown> {
    const payload: Record<string, unknown> = {};
    for (const field of fields) {
      const value = this.form.controls[field.key]?.value;
      if (value === '' || value === null || value === undefined) {
        if (this.formMode() === 'edit' && field.type === 'password') {
          continue;
        }
        if (field.omitWhenEmpty) {
          continue;
        }
        payload[field.key] = null;
        continue;
      }
      payload[field.key] = field.type === 'number' ? Number(value) : value;
    }
    return payload;
  }

  private toFormValue(value: unknown): FormValue {
    if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
      return value;
    }
    return null;
  }

  private upsertRecord(entity: EntityDefinition, savedRecord: RecordData): void {
    const savedId = String(savedRecord[entity.idField] ?? '');
    this.records.update((records) => {
      const index = records.findIndex((record) => String(record[entity.idField] ?? '') === savedId);
      if (index === -1) {
        return [...records, savedRecord];
      }
      return records.map((record, recordIndex) => (recordIndex === index ? savedRecord : record));
    });
  }

  private showError(error: unknown): void {
    let message = 'No fue posible completar la solicitud. Intenta de nuevo.';
    if (error instanceof HttpErrorResponse) {
      if (error.status === 0) {
        message =
          'No hay conexión con la API. Verifica que el backend esté ejecutándose en http://127.0.0.1:8000.';
      } else if (typeof error.error?.detail === 'string') {
        message = error.error.detail;
      } else if (error.status === 422) {
        message = 'Revisa los campos: algunos datos no cumplen con el formato esperado.';
      } else if (error.status === 409) {
        message =
          'El registro entra en conflicto con datos existentes o está relacionado con otros registros.';
      } else if (error.status === 404) {
        message = 'No se encontró el registro solicitado.';
      } else {
        message = `La API respondió con el código ${error.status}.`;
      }
    }

    this.notice.set({ kind: 'error', message });
  }
}
