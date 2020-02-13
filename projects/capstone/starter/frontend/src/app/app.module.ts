import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from  '@angular/common/http/';
import {
    MatDialogModule, MatFormFieldModule, MatButtonModule,
    MatInputModule, MatDatepickerModule,MatNativeDateModule
} from '@angular/material';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ActorComponent } from './actor/actor.component';
import { MoviesComponent } from './movies/movies.component';
import { MovieformComponent } from './movieform/movieform.component';

import { AuthService } from './services/auth.service';
import { ActorformComponent } from './actorform/actorform.component';
import { ActmovComponent } from './actmov/actmov.component';
import { ActorEditComponent } from './actor-edit/actor-edit.component';
import { MovieEditComponent } from './movie-edit/movie-edit.component';
import { MovieDialogComponent } from './movie-dialog/movie-dialog.component';
import { ActorDialogComponent } from './actor-dialog/actor-dialog.component';


@NgModule({
  declarations: [
    AppComponent,
    ActorComponent,
    MoviesComponent,
    MovieformComponent,
    ActorformComponent,
    ActmovComponent,
    ActorEditComponent,
    MovieEditComponent,
    MovieDialogComponent,
    ActorDialogComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    AppRoutingModule,
    MatDialogModule, MatFormFieldModule, MatButtonModule, MatInputModule,
    BrowserAnimationsModule,
    MatDatepickerModule,
    MatNativeDateModule
  ],
  providers: [
      AuthService,
      DatePipe
  ],
  bootstrap: [AppComponent],
  entryComponents: [ MovieDialogComponent, ActorDialogComponent ]
})
export class AppModule { }
