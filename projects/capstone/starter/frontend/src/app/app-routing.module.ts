import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ActorComponent } from './actor/actor.component';
import { MoviesComponent } from './movies/movies.component';
import { MovieformComponent } from './movieform/movieform.component';
import { ActorformComponent } from './actorform/actorform.component';
import { ActmovComponent } from './actmov/actmov.component';
import { ActorEditComponent } from './actor-edit/actor-edit.component';
import { MovieEditComponent } from './movie-edit/movie-edit.component';



const routes: Routes = [
  { path: 'actors', component: ActorComponent },
  { path: 'actors/addactors', component: ActorformComponent },
  { path: 'actor-edit/:id', component: ActorEditComponent, data: { title: 'Edit Actor' } },
  { path: 'movies', component: MoviesComponent },
  { path: 'movies/addmovies', component: MovieformComponent },
  { path: 'movie-edit/:id', component: MovieEditComponent, data: { title: 'Edit Movie' } },
  { path: 'actmov', component: ActmovComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
