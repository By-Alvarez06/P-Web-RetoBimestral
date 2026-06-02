import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { TitleCasePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../../shared/services/auth.service';
import { DashboardService } from '../../../shared/services/dashboard.service';

@Component({
  selector: 'app-vendedor-inicio',
  imports: [RouterLink, TitleCasePipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './vendedor-inicio.html',
  styles: [],
})
export class VendedorInicioComponent {
  readonly auth = inject(AuthService);
  readonly dash = inject(DashboardService);

  readonly myOrders = this.dash.orders().filter(o => o.seller === 'Carlos Ramírez');
  readonly myCommissions = this.dash.commissions().filter(c => c.seller === 'Carlos Ramírez');

  readonly totalSales = this.myOrders
    .filter(o => o.status === 'entregado')
    .reduce((s, o) => s + o.total, 0);

  readonly totalCommission = this.myCommissions
    .filter(c => c.status !== 'pagada')
    .reduce((s, c) => s + c.amount, 0);

  readonly pending = this.myOrders.filter(o => o.status === 'pendiente' || o.status === 'confirmado').length;

  readonly activeCampaigns = this.dash.campaigns().filter(c => c.active);

  readonly chartData = [
    { label:'Ene', value:40 }, { label:'Feb', value:65 }, { label:'Mar', value:48 },
    { label:'Abr', value:80 }, { label:'May', value:72 }, { label:'Jun', value:95 },
  ];
  readonly chartMax = Math.max(...this.chartData.map(d => d.value));
}
