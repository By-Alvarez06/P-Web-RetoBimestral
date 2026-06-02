import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { DashboardService } from '../../../shared/services/dashboard.service';

@Component({
  selector: 'app-com-reportes',
  imports: [DecimalPipe],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './com-reportes.html',
  styles: [],
})
export class ComReportesComponent {
  readonly dash = inject(DashboardService);

  readonly chartMonthly = [
    { label:'Ene', value:4200 }, { label:'Feb', value:5800 }, { label:'Mar', value:5100 },
    { label:'Abr', value:6700 }, { label:'May', value:7200 }, { label:'Jun', value:8450 },
  ];
  readonly chartMax = Math.max(...this.chartMonthly.map(d => d.value));

  readonly byCategory = [
    { category:'Electrónica', amount:9450, pct:33 },
    { category:'Herramientas', amount:6200, pct:22 },
    { category:'Alimentos', amount:5100, pct:18 },
    { category:'Limpieza', amount:3900, pct:14 },
    { category:'Oficina', amount:2250, pct:8 },
    { category:'Ropa & Seg.', amount:1450, pct:5 },
  ];
}
