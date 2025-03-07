import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CommonModule, DatePipe, HashLocationStrategy, Location, LocationStrategy } from '@angular/common';
import { StorageService } from './services/storage.service';
import { RestService } from './services/rest.service';
import { JwtHelperService, JwtModule } from '@auth0/angular-jwt';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    HttpClientModule,
    CommonModule,
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    JwtModule.forRoot({
      config: {}
    })
  ],
  providers: [DatePipe, Location, RestService, JwtHelperService, StorageService, {provide: LocationStrategy, useClass: HashLocationStrategy}, ],
  bootstrap: [AppComponent]
})
export class AppModule { }
