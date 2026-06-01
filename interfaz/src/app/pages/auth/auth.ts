import { ChangeDetectionStrategy, Component, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';

type AuthTab = 'login' | 'register';
type AccountType = 'minorista' | 'mayorista';

@Component({
  selector: 'app-auth',
  imports: [RouterLink, FormsModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './auth.html',
  styleUrl: './auth.scss',
})
export class AuthComponent {
  readonly activeTab = signal<AuthTab>('login');
  readonly accountType = signal<AccountType>('minorista');
  readonly showPassword = signal(false);
  readonly showConfirmPwd = signal(false);

  readonly loginForm = signal({ email: '', password: '' });
  readonly registerForm = signal({
    name: '', company: '', ruc: '', email: '',
    phone: '', password: '', confirmPassword: ''
  });

  switchTab(tab: AuthTab): void {
    this.activeTab.set(tab);
  }
}
