import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';

// Components
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { DocumentUploadComponent } from './components/document-upload/document-upload.component';
import { QueryInterfaceComponent } from './components/query-interface/query-interface.component';
import { AnalyticsComponent } from './components/analytics/analytics.component';
import { AgentsComponent } from './components/agents/agents.component';
import { SettingsComponent } from './components/settings/settings.component';
import { LoginComponent } from './components/auth/login/login.component';
import { SignupComponent } from './components/auth/signup/signup.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
  { path: 'upload', component: DocumentUploadComponent, canActivate: [AuthGuard] },
  { path: 'query', component: QueryInterfaceComponent, canActivate: [AuthGuard] },
  { path: 'agents', component: AgentsComponent, canActivate: [AuthGuard] },
  { path: 'analytics', component: AnalyticsComponent, canActivate: [AuthGuard] },
  { path: 'settings', component: SettingsComponent, canActivate: [AuthGuard] },
  { path: '**', redirectTo: '/dashboard' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
