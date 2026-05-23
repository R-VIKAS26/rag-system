import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NgxLoadingModule } from 'ngx-loading';
import { ToastrModule } from 'ngx-toastr';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

// Components
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { DocumentUploadComponent } from './components/document-upload/document-upload.component';
import { QueryInterfaceComponent } from './components/query-interface/query-interface.component';
import { AnalyticsComponent } from './components/analytics/analytics.component';
import { AgentsComponent } from './components/agents/agents.component';
import { SettingsComponent } from './components/settings/settings.component';
import { LoginComponent } from './components/auth/login/login.component';
import { SignupComponent } from './components/auth/signup/signup.component';

// Services
import { AuthService } from './services/auth.service';
import { DocumentService } from './services/document.service';
import { RagService } from './services/rag.service';
import { AgentService } from './services/agent.service';
import { AnalyticsService } from './services/analytics.service';
import { AuthInterceptor } from './interceptors/auth.interceptor';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    DocumentUploadComponent,
    QueryInterfaceComponent,
    AnalyticsComponent,
    AgentsComponent,
    SettingsComponent,
    LoginComponent,
    SignupComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    NgbModule,
    NgxLoadingModule.forRoot({}),
    ToastrModule.forRoot()
  ],
  providers: [
    AuthService,
    DocumentService,
    RagService,
    AgentService,
    AnalyticsService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
