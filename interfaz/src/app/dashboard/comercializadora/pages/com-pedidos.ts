import { ChangeDetectionStrategy, Component, inject, signal, computed } from '@angular/core';
import { TitleCasePipe } from '@angular/common';
import { DashboardService, OrderStatus } from '../../../shared/services/dashboard.service';

@Component({
  selector: 'app-com-pedidos',
  imports: [TitleCasePipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './com-pedidos.html',
  styles: [],
})
export class ComPedidosComponent {
  readonly dash = inject(DashboardService);
  readonly filterStatus = signal<OrderStatus | ''>('');

  readonly orders = computed(() => {
    const f = this.filterStatus();
    return f ? this.dash.orders().filter(o => o.status === f) : this.dash.orders();
  });

  readonly statuses: { value: OrderStatus | ''; label: string }[] = [
    { value: '', label: 'Todos' },
    { value: 'pendiente', label: 'Pendiente' },
    { value: 'confirmado', label: 'Confirmado' },
    { value: 'en_proceso', label: 'En proceso' },
    { value: 'entregado', label: 'Entregado' },
    { value: 'cancelado', label: 'Cancelado' },
  ];
}
