import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { TitleCasePipe, DecimalPipe } from '@angular/common';
import { DashboardService } from '../../../shared/services/dashboard.service';

@Component({
  selector: 'app-vendedor-puntos',
  imports: [TitleCasePipe, DecimalPipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './vendedor-puntos.html',
  styles: [],
})
export class VendedorPuntosComponent {
  readonly dash = inject(DashboardService);
  readonly transactions = this.dash.pointTransactions();
  readonly totalPoints = 2340;
  readonly nextLevel = 3000;
  readonly progress = Math.round((this.totalPoints / this.nextLevel) * 100);
}
