import { ChangeDetectionStrategy, Component, inject, signal, computed } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { DashboardService } from '../../../shared/services/dashboard.service';

@Component({
  selector: 'app-com-productos',
  imports: [FormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './com-productos.html',
  styles: [],
})
export class ComProductosComponent {
  readonly dash = inject(DashboardService);
  readonly search = signal('');

  readonly filtered = computed(() => {
    const q = this.search().toLowerCase();
    return q ? this.dash.products().filter(p => p.name.toLowerCase().includes(q) || p.code.toLowerCase().includes(q)) : this.dash.products();
  });
}
