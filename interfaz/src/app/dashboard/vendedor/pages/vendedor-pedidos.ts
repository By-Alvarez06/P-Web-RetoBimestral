import { ChangeDetectionStrategy, Component, inject, signal, computed } from '@angular/core';
import { TitleCasePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { DashboardService, OrderStatus } from '../../../shared/services/dashboard.service';

@Component({
  selector: 'app-vendedor-pedidos',
  imports: [RouterLink, TitleCasePipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './vendedor-pedidos.html',
  styles: [],
})
export class VendedorPedidosComponent {
  readonly dash = inject(DashboardService);
  readonly filterStatus = signal<OrderStatus | ''>('');

  readonly orders = computed(() => {
    const f = this.filterStatus();
    const mine = this.dash.orders().filter(o => o.seller === 'Carlos Ramírez');
    return f ? mine.filter(o => o.status === f) : mine;
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
