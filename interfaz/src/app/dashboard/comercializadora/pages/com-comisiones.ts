import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { TitleCasePipe } from '@angular/common';
import { DashboardService } from '../../../shared/services/dashboard.service';

@Component({
  selector: 'app-com-comisiones',
  imports: [TitleCasePipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './com-comisiones.html',
  styles: [],
})
export class ComComisionesComponent {
  readonly dash = inject(DashboardService);
  readonly commissions = this.dash.commissions();
  readonly totalPagado   = this.commissions.filter(c => c.status === 'pagada').reduce((s,c) => s+c.amount,0);
  readonly totalPendiente = this.commissions.filter(c => c.status === 'pendiente').reduce((s,c) => s+c.amount,0);
}
