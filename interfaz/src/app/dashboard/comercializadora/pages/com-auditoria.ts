import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { DashboardService } from '../../../shared/services/dashboard.service';

@Component({
  selector: 'app-com-auditoria',
  imports: [],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './com-auditoria.html',
  styles: [],
})
export class ComAuditoriaComponent {
  readonly dash = inject(DashboardService);
  readonly log = this.dash.auditLog();
}
