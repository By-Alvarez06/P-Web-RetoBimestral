import { ChangeDetectionStrategy, Component, inject, signal, computed } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DashboardService } from '../../../shared/services/dashboard.service';

@Component({
  selector: 'app-vendedor-catalogo',
  imports: [RouterLink, FormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './vendedor-catalogo.html',
  styles: [],
})
export class VendedorCatalogoComponent {
  readonly dash = inject(DashboardService);
  readonly search = signal('');

  readonly filtered = computed(() => {
    const q = this.search().toLowerCase();
    return this.dash.products().filter(p =>
      p.active && (p.name.toLowerCase().includes(q) || p.category.toLowerCase().includes(q))
    );
  });
}
