import { Component, OnInit } from '@angular/core';
import { Movie } from '../classes/movie';
import { Router, ActivatedRoute } from '@angular/router';
import { MovieService } from '../services/movie.service';

@Component({
  selector: 'app-movie-edit',
  templateUrl: './movie-edit.component.html',
  styleUrls: ['./movie-edit.component.css']
})
export class MovieEditComponent implements OnInit {

    model: Movie;
    _id:number;
    loading=true;
    genvals = ['Comedy', 'Thriller', 'Drama', 'Family', 'Action', 'SCIFI', 'Documentary'];

    constructor(private router: Router,
          private route: ActivatedRoute,
          public mvService: MovieService) { }

  ngOnInit() {
      this.getMovie(this.route.snapshot.params['id']);
  }

  getMovie(id) {
      this.mvService.getMovie(id).subscribe( mvs => {
          this.loadData(mvs);
          this.loading = false;
      },(err) => {
          console.log(err);
      });
  }

  public loadData(mvs):void{
      this._id = mvs.movies.id;
      this.model = mvs.movies;
  }

  updateMovie() {
      this.mvService.updateMovie(this._id, this.model);
  }


}
