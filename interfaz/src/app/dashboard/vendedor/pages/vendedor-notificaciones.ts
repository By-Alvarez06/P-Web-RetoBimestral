import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { DashboardService } from '../../../shared/services/dashboard.service';

@Component({
  selector: 'app-vendedor-notificaciones',
  imports: [],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './vendedor-notificaciones.html',
  styles: [],
})
export class VendedorNotificacionesComponent {
  readonly dash = inject(DashboardService);
  readonly notifications = this.dash.notifications;

  markAllRead(): void { this.dash.markAllRead(); }
  markRead(id: string): void { this.dash.markNotificationRead(id); }

  typeLabel(type: string): string {
    const map: Record<string, string> = { pedido:'Pedido', inventario:'Inventario', campana:'Campaña', sistema:'Sistema' };
    return map[type] ?? type;
  }
}
