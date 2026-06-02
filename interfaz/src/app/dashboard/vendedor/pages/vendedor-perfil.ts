import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../shared/services/auth.service';

@Component({
  selector: 'app-vendedor-perfil',
  imports: [FormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './vendedor-perfil.html',
  styles: [],
})
export class VendedorPerfilComponent {
  readonly auth = inject(AuthService);
}
