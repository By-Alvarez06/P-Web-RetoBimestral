import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { DashboardService } from '../../../shared/services/dashboard.service';

@Component({
  selector: 'app-com-inventario',
  imports: [],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './com-inventario.html',
  styles: [],
})
export class ComInventarioComponent {
  readonly dash = inject(DashboardService);
  readonly products = this.dash.products();
  readonly alerts = this.dash.inventoryAlerts();

  stockPct(stock: number, max = 200): number {
    return Math.min((stock / max) * 100, 100);
  }
}
