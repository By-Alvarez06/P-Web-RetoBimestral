import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { NavigationEnd, Router, RouterOutlet } from '@angular/router';
import { filter, map, startWith } from 'rxjs';
import { toSignal } from '@angular/core/rxjs-interop';
import { NavbarComponent } from './shared/components/navbar/navbar';
import { FooterComponent } from './shared/components/footer/footer';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, NavbarComponent, FooterComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  private readonly router = inject(Router);

  readonly showPublicLayout = toSignal(
    this.router.events.pipe(
      filter(e => e instanceof NavigationEnd),
      map(() => !this.router.url.startsWith('/dashboard')),
      startWith(!this.router.url.startsWith('/dashboard'))
    ),
    { initialValue: true }
  );
}
