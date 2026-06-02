import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { DashboardService } from '../../../shared/services/dashboard.service';

@Component({
  selector: 'app-com-vendedores',
  imports: [DecimalPipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './com-vendedores.html',
  styles: [],
})
export class ComVendedoresComponent {
  readonly dash = inject(DashboardService);
  readonly sellers = this.dash.sellers();
}
