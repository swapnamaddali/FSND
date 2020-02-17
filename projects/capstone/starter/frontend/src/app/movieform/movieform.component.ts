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
    submitted = false;
    minToday: Date;
    maxDate: Date;
    error:any={isError:false,errorMessage:''};

    constructor(public mvService: MovieService) {
        this.minToday = new Date();
        this.maxDate = new Date('2030-01-01');
    }

    public addMovie(){
        //console.log(this.model);
        if(this.model.release_date == null) {
            this.error={isError:true,errorMessage:'Release Date is Required!!!'};
            return;
        }
        this.submitted = true;
        this.mvService.addMovie(this.model);
    }
}
