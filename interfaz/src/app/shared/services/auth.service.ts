import { Injectable, computed, signal } from '@angular/core';

export type UserRole = 'vendedor' | 'comercializadora' | 'minorista';

export interface User {
  ruc: string;
  nombre: string;
  role: UserRole;
  empresa: string;
  email: string;
}

const DEMO_USERS: Record<string, User> = {
  '1768123456001': {
    ruc: '1768123456001', nombre: 'Carlos Ramírez', role: 'vendedor',
    empresa: 'ISBEN Solutions', email: 'carlos.ramirez@mail.com'
  },
  '1768654321001': {
    ruc: '1768654321001', nombre: 'Administrador General', role: 'comercializadora',
    empresa: 'ISBEN Solutions S.A.', email: 'admin@isbensolutions.ec'
  },
};

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly _user = signal<User | null>(null);

  readonly user = this._user.asReadonly();
  readonly isLoggedIn = computed(() => this._user() !== null);
  readonly role = computed(() => this._user()?.role ?? null);

  login(ruc: string): User {
    const existing = DEMO_USERS[ruc];
    if (existing) {
      this._user.set(existing);
      return existing;
    }
    const role: UserRole = ruc.endsWith('001') ? 'vendedor' : 'comercializadora';
    const demo: User = {
      ruc, nombre: 'Usuario Demo', role,
      empresa: 'ISBEN Solutions', email: 'demo@isbensolutions.ec'
    };
    this._user.set(demo);
    return demo;
  }

  logout(): void {
    this._user.set(null);
  }
}
