import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { TitleCasePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { DashboardService } from '../../../shared/services/dashboard.service';

@Component({
  selector: 'app-com-inicio',
  imports: [RouterLink, TitleCasePipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './com-inicio.html',
  styles: [],
})
export class ComInicioComponent {
  readonly dash = inject(DashboardService);

  readonly totalSales = this.dash.orders()
    .filter(o => o.status === 'entregado')
    .reduce((s, o) => s + o.total, 0);

  readonly activeOrders = this.dash.orders()
    .filter(o => o.status !== 'cancelado' && o.status !== 'entregado').length;

  readonly criticalAlerts = this.dash.inventoryAlerts()
    .filter(a => a.status === 'critico').length;

  readonly recentOrders = this.dash.orders().slice(0, 6);
  readonly topProducts = this.dash.products().slice(0, 5);
  readonly alerts = this.dash.inventoryAlerts();

  readonly chartData = [
    { label:'Sem 1', value:60 }, { label:'Sem 2', value:85 }, { label:'Sem 3', value:72 },
    { label:'Sem 4', value:95 }, { label:'Sem 5', value:78 }, { label:'Sem 6', value:110 },
  ];
  readonly chartMax = Math.max(...this.chartData.map(d => d.value));
}
