import { Component, OnInit } from '@angular/core';
import { Actmov } from '../classes/actmov';
import { AuthService } from '../services/auth.service';
import { ActorService } from '../services/actor.service';
import { MovieService } from '../services/movie.service';
import { Actor } from '../classes/actor';
import { Movie } from '../classes/movie';
import { Observable } from 'rxjs';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-actmov',
  templateUrl: './actmov.component.html',
  styleUrls: ['./actmov.component.css']
})
export class ActmovComponent implements OnInit {

    model = new Actmov();

    actors: Actor[];
    movies: Movie[];

    stDateForValidation: String;
    endDateForValidation: String;

    minToday: Date;
    maxDate: Date;

    //Error Display
    error:any={isError:false,errorMessage:''};
    isValidDate:any;
    submitted = false;

    constructor(
        private auth: AuthService,
        public aService: ActorService,
        private mvService: MovieService,
        private datePipe: DatePipe) {
            this.minToday = new Date();
            this.maxDate = new Date('2030-01-01');
         }

    ngOnInit() {
        this.aService.getActors()
            .subscribe( acts => {
                this.loadDataActors(acts)
            },(err) => {
        console.log(err);
        });
        this.mvService.getMovies()
            .subscribe( mvs => {
                this.loadDataMovies(mvs)
            },(err) => {
        console.log(err);
        });
    }

    public loadDataActors(acts):void{
        this.actors = acts.actors;
    }

    public loadDataMovies(mvs):void{
        this.movies = mvs.movies;
    }

    public addSchedule(){
        if(this.model.start_date == null) {
            this.error={isError:true,errorMessage:'Start Date is Required!!!'};
            return;
        }
        if (this.model.end_date == null) {
            this.error={isError:true,errorMessage:'End date is Required!!!'};
            return;
        }
        this.isValidDate = this.validateDates(new Date(this.model.start_date),
                                    new Date(this.model.end_date));
        if(this.isValidDate){
            this.submitted = true;
            this.aService.addActmov(this.model);
        }
    }

    validateDates(sDate: Date, npDate: Date){
        if(sDate != null && npDate != null && (sDate > npDate)){
          this.error={isError:true,errorMessage:'End date should be greater then start date.'};
          return false;
        }
        return true;
    }
}
