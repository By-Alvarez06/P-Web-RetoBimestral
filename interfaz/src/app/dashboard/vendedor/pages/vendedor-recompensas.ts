import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { DashboardService } from '../../../shared/services/dashboard.service';

@Component({
  selector: 'app-vendedor-recompensas',
  imports: [],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './vendedor-recompensas.html',
  styles: [],
})
export class VendedorRecompensasComponent {
  readonly dash = inject(DashboardService);
  readonly campaigns = this.dash.campaigns();
  readonly active = this.campaigns.filter(c => c.active);
  readonly inactive = this.campaigns.filter(c => !c.active);
}
