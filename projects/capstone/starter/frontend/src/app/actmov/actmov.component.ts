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
    today: String;

    //Error Display
    error:any={isError:false,errorMessage:''};
    isValidDate:any;

    constructor(
        private auth: AuthService,
        public aService: ActorService,
        private mvService: MovieService,
        private datePipe: DatePipe) { }

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
        this.stDateForValidation = this.datePipe.transform(this.model.start_date,"dd-MM-yyyy");
        this.endDateForValidation = this.datePipe.transform(this.model.end_date,"dd-MM-yyyy");

        this.isValidDate = this.validateDates(this.stDateForValidation, this.endDateForValidation);
        if(this.isValidDate){
            this.aService.addActmov(this.model);
        }
    }

    validateDates(sDate: String, npDate: String){
        this.isValidDate = true;
        this.today = this.datePipe.transform(Date.now(),"dd-MM-yyyy");
        if(sDate != null && this.today > (sDate)) {
            this.error={isError:true,errorMessage:'Start Date should be greater than today.'};
            this.isValidDate = false;
        }
        if(npDate != null && this.today > (npDate)) {
            this.error={isError:true,errorMessage:'End Date should be greater than today.'};
            this.isValidDate = false;
        }
        if((sDate != null && npDate !=null) && (npDate) < (sDate)){
          this.error={isError:true,errorMessage:'End date should be grater then start date.'};
          this.isValidDate = false;
        }

        return this.isValidDate;
    }
}
