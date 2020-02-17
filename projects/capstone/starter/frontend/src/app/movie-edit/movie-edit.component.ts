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
    submitted = false;
    minToday: Date;
    maxDate: Date;
    error:any={isError:false,errorMessage:''};

    constructor(private router: Router,
          private route: ActivatedRoute,
          public mvService: MovieService) {
              this.minToday = new Date();
              this.maxDate = new Date('2030-01-01');
    }

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
      this.model.release_date = new Date(mvs.movies.release_date);
  }

  updateMovie() {
      if(this.model.release_date == null) {
          this.error={isError:true,errorMessage:'Release Date is Required!!!'};
          return;
      }
      this.submitted = true;
      this.mvService.updateMovie(this._id, this.model);
  }


}
