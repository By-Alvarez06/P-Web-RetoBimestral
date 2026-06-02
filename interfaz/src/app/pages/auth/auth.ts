import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../shared/services/auth.service';

type AuthTab = 'login' | 'register';
type AccountType = 'minorista' | 'mayorista' | 'vendedor';

@Component({
  selector: 'app-auth',
  imports: [RouterLink, FormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './auth.html',
  styleUrl: './auth.scss',
})
export class AuthComponent {
  private authService = inject(AuthService);
  private router = inject(Router);

  readonly activeTab = signal<AuthTab>('login');
  readonly accountType = signal<AccountType>('minorista');
  readonly showPassword = signal(false);
  readonly showConfirmPwd = signal(false);
  readonly loginRuc = signal('');
  readonly loginError = signal('');

  switchTab(tab: AuthTab): void {
    this.activeTab.set(tab);
    this.loginError.set('');
  }

  onLogin(): void {
    const ruc = this.loginRuc().trim();
    if (!ruc) {
      this.loginError.set('Ingresa tu RUC para continuar.');
      return;
    }
    const user = this.authService.login(ruc);
    if (user.role === 'vendedor') {
      this.router.navigate(['/dashboard/vendedor']);
    } else {
      this.router.navigate(['/dashboard/comercializadora']);
    }
  }
}
