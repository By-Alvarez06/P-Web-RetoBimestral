import { ChangeDetectionStrategy, Component, inject, computed } from '@angular/core';
import { TitleCasePipe } from '@angular/common';
import { DashboardService } from '../../../shared/services/dashboard.service';

@Component({
  selector: 'app-vendedor-comisiones',
  imports: [TitleCasePipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './vendedor-comisiones.html',
  styles: [],
})
export class VendedorComisionesComponent {
  readonly dash = inject(DashboardService);
  readonly myComm = this.dash.commissions().filter(c => c.seller === 'Carlos Ramírez');

  readonly totalPagada  = this.myComm.filter(c => c.status === 'pagada').reduce((s,c) => s+c.amount,0);
  readonly totalPendiente = this.myComm.filter(c => c.status === 'pendiente').reduce((s,c) => s+c.amount,0);
}
