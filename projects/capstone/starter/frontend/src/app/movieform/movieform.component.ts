import { Component, OnInit } from '@angular/core';
import { Movie } from '../classes/movie';
import { MovieService } from '../services/movie.service';

@Component({
  selector: 'app-movieform',
  templateUrl: './movieform.component.html',
  styleUrls: ['./movieform.component.css']
})
export class MovieformComponent{

    genvals = ['Comedy', 'Thriller', 'Drama', 'Family', 'Action', 'SCIFI', 'Documentary'];
    model = new Movie();

    constructor(public mvService: MovieService) { }

    public addMovie(){
        //console.log(this.model);
        this.mvService.addMovie(this.model);
    }
}
